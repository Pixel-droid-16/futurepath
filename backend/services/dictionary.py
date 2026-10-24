"""Local offline suggestion fallback. Suggestions never imply proficiency."""
import re
from ..catalog import SKILLS

def suggest(text,excerpt_before=35,excerpt_after=45):
    candidates=[]
    for skill in SKILLS:
        for alias in [skill['name']]+skill.get('aliases',[]):
            hit=re.search(r'(?<!\w)'+re.escape(alias)+r'(?!\w)',text,re.I)
            if hit:
                start = max(0, hit.start() - excerpt_before)
                end = min(len(text), hit.end() + excerpt_after)

                # Avoid cutting evidence excerpts in the middle of words.
                while start > 0 and text[start - 1].isalnum():
                    start -= 1
                while end < len(text) and text[end].isalnum():
                    end += 1

                excerpt = text[start:end].strip()

                candidates.append({'skill_id':skill['id'],'name':skill['name'],
                    'excerpt':excerpt,
                    'method':'dictionary suggestion','proficiency':None})
                break
    return candidates
