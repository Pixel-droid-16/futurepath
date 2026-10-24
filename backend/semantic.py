"""Optional local sentence-transformer layer.

Role and skill vectors are precomputed with `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions,
via fastembed/ONNX) and stored in data/semantic_vectors.json. Regenerate them with:

    python scripts/build_semantic_vectors.py

At runtime the app uses the cached role/skill vectors and only needs the model to embed a person's
free text (current role, headline, goals). If fastembed or the model is unavailable, scoring falls back
to backend/text_match.py, so the demo still works offline.

Embeddings are a supporting signal, never a replacement for exact catalogue skills. A curated
data/skill_relations.json file resolves known related skills and blocks known false friends.
"""
from functools import lru_cache
import importlib.util
import json

from .catalog import ROOT, ROLES, SKILL_INDEX
from .scenarios import TASKS
from .text_match import keyword_fit

MODEL_NAME='sentence-transformers/all-MiniLM-L6-v2'
CACHE_PATH=ROOT/'data'/'semantic_vectors.json'
RELATIONS_PATH=ROOT/'data'/'skill_relations.json'

# Open embedding pairs below this cosine are treated as unrelated. Curated pairs bypass this threshold.
SKILL_SIM_THRESHOLD=0.70
SKILL_SIM_MAX_CREDIT=0.60
# Calibration for short profile/role text. MiniLM cosines for unrelated short texts sit near 0.20;
# a clear role match is around 0.60-0.68. This maps that range onto 0-100 without pretending it is a probability.
TEXT_COS_FLOOR=0.20
TEXT_COS_CEIL=0.65

ROLE_INDEX={r['id']:r for r in ROLES}

try:
    import numpy as np
except ImportError:  # pragma: no cover - requirements include numpy, but the fallback keeps the app usable
    np=None

def _pair(a,b):
    return '|'.join(sorted((a,b)))

@lru_cache(maxsize=1)
def _relations():
    try:
        data=json.loads(RELATIONS_PATH.read_text(encoding='utf8'))
    except (OSError,ValueError):
        return {},{}
    pairs={_pair(*k.split('|')):float(v) for k,v in (data.get('pairs') or {}).items() if '|' in k}
    blocked={_pair(*k.split('|')) for k in (data.get('blocked') or []) if '|' in k}
    return pairs,blocked

@lru_cache(maxsize=1)
def _cache():
    """Normalised role/skill vectors, or None when the cached file is missing/unreadable."""
    if np is None or not CACHE_PATH.exists():return None
    try:
        data=json.loads(CACHE_PATH.read_text(encoding='utf8'))
        if data.get('model')!=MODEL_NAME:return None
        out={}
        for kind in ('roles','skills'):
            vectors={}
            for key,values in (data.get(kind) or {}).items():
                vector=np.asarray(values,dtype=np.float32)
                norm=float(np.linalg.norm(vector))
                if norm>0:vectors[key]=vector/norm
            out[kind]=vectors
        return out
    except (OSError,ValueError,TypeError):
        return None

def role_text(role):
    """Stable text used to embed a career. Keep this in sync with scripts/build_semantic_vectors.py."""
    skills=', '.join(SKILL_INDEX[s['skill_id']]['name'] for s in role.get('skills',[]) if s['skill_id'] in SKILL_INDEX)
    tasks=', '.join(t[0] for t in TASKS.get(role['id'],[]))
    text=f"{role['title']}. Sector: {role['sector']}. {role.get('description','')} Skills: {skills}."
    if tasks:text+=f' Example tasks: {tasks}.'
    return text

def skill_text(skill):
    aliases=', '.join(skill.get('aliases',[]))
    text=f"{skill['name']}. Category: {skill['category']}."
    if aliases:text+=f' Also called: {aliases}.'
    return text

def curated_similarity(a,b):
    """A human-reviewed pair value, 0 for blocked pairs, or None when the pair is not curated."""
    pairs,blocked=_relations()
    key=_pair(a,b)
    if key in blocked:return 0.0
    return pairs.get(key)

def skill_similarity(a,b):
    """Cosine similarity between two catalogue skills, 0 when vectors are unavailable."""
    if a==b:return 1.0
    curated=curated_similarity(a,b)
    if curated is not None:return curated
    cache=_cache()
    if not cache:return 0.0
    va=cache['skills'].get(a);vb=cache['skills'].get(b)
    if va is None or vb is None:return 0.0
    return float(va@vb)

def transfer_similarity(target_id,source_id):
    """How much a confirmed source skill can count towards a missing target skill (0-0.6).

    Curated pairs work across categories. Automatic embedding pairs are restricted to the same
    non-transferable category and a high threshold, because generic words like "design" or
    "compliance" otherwise create false credit.
    """
    if target_id==source_id:return 0.0
    curated=curated_similarity(target_id,source_id)
    if curated is not None:return min(SKILL_SIM_MAX_CREDIT,curated)
    target=SKILL_INDEX.get(target_id);source=SKILL_INDEX.get(source_id)
    if not target or not source:return 0.0
    if target['category']!=source['category']:return 0.0
    if target['category']=='transferable' or source['category']=='transferable':return 0.0
    cosine=skill_similarity(target_id,source_id)
    if cosine<SKILL_SIM_THRESHOLD:return 0.0
    return min(SKILL_SIM_MAX_CREDIT,(cosine-SKILL_SIM_THRESHOLD)/(1.0-SKILL_SIM_THRESHOLD)*0.8)

@lru_cache(maxsize=1)
def _model():
    """Load the local fastembed model once; return None when it cannot be loaded."""
    try:
        from fastembed import TextEmbedding
        return TextEmbedding(model_name=MODEL_NAME)
    except Exception:
        return None

@lru_cache(maxsize=256)
def _embed(text):
    """Embed one string with the local MiniLM model, or return None if the runtime/model is unavailable."""
    if np is None:return None
    model=_model()
    if model is None:return None
    try:
        vector=np.asarray(next(model.embed([text])),dtype=np.float32)
        norm=float(np.linalg.norm(vector))
        return vector/norm if norm>0 else None
    except Exception:
        return None

def _semantic_score(text,role_id):
    cache=_cache()
    if not cache:return None
    role_vector=cache['roles'].get(role_id)
    if role_vector is None:return None
    vector=_embed(text)
    if vector is None:return None
    cosine=float(vector@role_vector)
    score=100.0*(cosine-TEXT_COS_FLOOR)/(TEXT_COS_CEIL-TEXT_COS_FLOOR)
    return round(max(0.0,min(100.0,score)),1)

def text_fit(text,role_id):
    """Return (score 0-100, source label) for profile free text against one career, or (None,None)."""
    if not text:return None,None
    role=ROLE_INDEX.get(role_id)
    if role is None:return None,None
    keywords=keyword_fit(text,role)
    semantic=_semantic_score(text,role_id)
    if semantic is None:
        return (keywords,'keywords') if keywords else (None,None)
    # Keyword overlap can rescue an exact job title that a general sentence model undervalues, but it
    # cannot dominate the semantic score.
    blended=max(semantic,min(100.0,keywords*0.75))
    source='semantic' if semantic>=keywords*0.75 else 'semantic+keywords'
    return round(blended,1),source

def suggest_skills(text,limit=8):
    """Semantic candidates for CV text. Used only as a recall helper; the caller must still ask the person to confirm."""
    cache=_cache()
    if not cache or not text:return []
    vector=_embed(text)
    if vector is None:return []
    scored=[(float(vector@v),sid) for sid,v in cache['skills'].items()]
    scored.sort(reverse=True)
    return [{'skill_id':sid,'name':SKILL_INDEX[sid]['name'],'similarity':round(score,3)}
            for score,sid in scored[:limit] if score>=0.40 and sid in SKILL_INDEX]

def status():
    cache=_cache()
    return {'model':MODEL_NAME,'vectors_cached':cache is not None,
            'role_vectors':len(cache['roles']) if cache else 0,'skill_vectors':len(cache['skills']) if cache else 0,
            'runtime_available':importlib.util.find_spec('fastembed') is not None,
            'note':'Embeddings add related-skill and profile-text signals; exact catalogue skills still score highest.'}
