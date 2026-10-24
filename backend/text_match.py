"""Small, dependency-free text matcher used when the sentence-transformer layer is unavailable.

It is deliberately simple: profile free text (current role, headline, goals, qualification) is compared
with the words already in a career profile (title, sector, description, skills, example tasks). It never
reads the CV itself and it never invents a skill. The semantic layer in backend/semantic.py replaces this
with all-MiniLM-L6-v2 vectors when the model is available.
"""
import re
from functools import lru_cache
from .catalog import ROLES, SKILL_INDEX
from .scenarios import TASKS

STOPWORDS={
    'the','and','for','with','from','that','this','have','has','had','are','was','were','will','would','can','could',
    'want','wants','wanted','like','likes','looking','look','move','moving','work','working','role','roles','job','jobs',
    'career','careers','into','about','their','there','they','you','your','our','its','also','more','most','some','any',
    'use','using','used','help','helping','make','making','build','building','learn','learning','new','next','good','great',
    'years','year','experience','experienced','strong','able','ability','understand','understanding','knowledge','skills',
    'skill','professional','student','graduate','people','team','teams','company','companies','sector','sectors','malaysia',
}

def tokens(text):
    """Lowercase word tokens, keeping short but meaningful terms such as SQL, UX, AI, EV and PLC."""
    words=re.findall(r'[a-z0-9+#.]+',(text or '').lower())
    out=set()
    for w in words:
        w=w.strip('.')
        if not w:continue
        if len(w)<3 and w not in {'sql','ux','ai','ev','plc','bi','5g','qa','esg','h2','r'}:
            continue
        if w in STOPWORDS:continue
        out.add(w)
    return out

def profile_text(profile):
    """Only the free-text fields a person chose to provide, never a raw CV or their skill list.

    A CV-only run has no narrative text, so the semantic profile-fit component is skipped and exact /
    related skills carry the match. That keeps the published base formula unchanged for those profiles.
    """
    parts=[]
    for key,label in (('current_role','Current role'),('headline','Headline'),('goals','Goal'),('qualification','Qualification')):
        value=(profile.get(key) or '').strip()
        if value:parts.append(f'{label}: {value}')
    years=profile.get('years_experience')
    if isinstance(years,int) and years>0:parts.append(f'Experience: {years} years')
    text='. '.join(parts).strip()
    return text if len(text)>=12 else None

@lru_cache(maxsize=64)
def _role_terms(role_id):
    role=next((r for r in ROLES if r['id']==role_id),None)
    if role is None:return {}
    weights={}
    def add(text,weight):
        for token in tokens(text):
            weights[token]=max(weights.get(token,0),weight)
    add(role['title'],3)
    add(role['sector'],2)
    add(role.get('description',''),1)
    for item in role.get('skills',[]):
        skill=SKILL_INDEX.get(item['skill_id'])
        if skill:
            add(skill['name'],2)
            for alias in skill.get('aliases',[]):add(alias,2)
    for task in TASKS.get(role_id,[]):add(task[0],1.5)
    return weights

def keyword_fit(text, role):
    """0-100 overlap score. `text` is profile_text(); `role` is a role dict."""
    if not text:return 0.0
    profile_tokens=tokens(text)
    if not profile_tokens:return 0.0
    terms=_role_terms(role['id'])
    if not terms:return 0.0
    matched=sum(terms.get(token,0) for token in profile_tokens)
    if not matched:return 0.0
    title=role['title'].lower()
    if title in text.lower():matched+=8
    elif all(token in profile_tokens for token in tokens(role['title'])):matched+=4
    return round(min(100.0,100.0*matched/(matched+6.0)),1)
