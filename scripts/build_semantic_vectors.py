"""Rebuild data/semantic_vectors.json with all-MiniLM-L6-v2.

Run from the repository root:

    python scripts/build_semantic_vectors.py

This is the only step that downloads/loads the sentence-transformer model. The app itself reads the
cached vectors, so normal scoring works offline. Re-run after editing roles.json or skills.json.
"""
from datetime import datetime,timezone
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from backend.catalog import ROLES,SKILLS
from backend.semantic import MODEL_NAME,CACHE_PATH,role_text,skill_text

def main():
    from fastembed import TextEmbedding
    model=TextEmbedding(model_name=MODEL_NAME)
    role_ids=[r['id'] for r in ROLES]
    skill_ids=[s['id'] for s in SKILLS]
    role_vectors=list(model.embed([role_text(r) for r in ROLES]))
    skill_vectors=list(model.embed([skill_text(s) for s in SKILLS]))
    data={'model':MODEL_NAME,'dim':len(role_vectors[0]),'generated_at':datetime.now(timezone.utc).isoformat(timespec='seconds'),
          'roles':{rid:[round(float(x),6) for x in vec] for rid,vec in zip(role_ids,role_vectors)},
          'skills':{sid:[round(float(x),6) for x in vec] for sid,vec in zip(skill_ids,skill_vectors)}}
    CACHE_PATH.write_text(json.dumps(data,separators=(',',':')),encoding='utf8')
    print(f'wrote {CACHE_PATH.relative_to(ROOT)} with {len(role_ids)} roles and {len(skill_ids)} skills ({data["dim"]} dims)')

if __name__=='__main__':main()
