"""Local offline suggestion fallback. Suggestions never imply proficiency."""
import re
from ..catalog import SKILLS

def suggest(text,excerpt_before=35,excerpt_after=45):
    candidates=[]
    for skill in SKILLS:
        for alias in [skill['name']]+skill.get('aliases',[]):
            hit=re.search(r'(?<!\w)'+re.escape(alias)+r'(?!\w)',text,re.I)
            if hit:
                candidates.append({'skill_id':skill['id'],'name':skill['name'],
                    'excerpt':text[max(0,hit.start()-excerpt_before):min(len(text),hit.end()+excerpt_after)].strip(),
                    'method':'dictionary suggestion','proficiency':None})
                break
    return candidates
