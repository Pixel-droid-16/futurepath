"""Enforces the "never invent" rules on a tagger proposal before anything is saved."""
import re

# Ingested items are single news/research items, so they never outweigh curated reports (strength up to 5).
MAX_INGESTED_STRENGTH=3
MAX_SUMMARY=400

def numbers_in(value):return re.findall(r'\d+(?:\.\d+)?',re.sub(r'(\d),(\d)',r'\1\2',value))

def apply_guardrails(item,proposal,role_ids,skill_ids):
    """Returns (accepted proposal, notes) or (None, rejection reason).

    - only career/skill IDs that exist in our catalogue are kept;
    - an item with no valid catalogue link is rejected;
    - a summary containing a number not in the source text is replaced by the headline;
    - strength is clamped to 1..MAX_INGESTED_STRENGTH.
    """
    if not proposal['relevant']:return None,proposal.get('reason') or 'not relevant to jobs or skills'
    roles=list(dict.fromkeys(r for r in proposal['role_ids'] if r in role_ids))
    skills=list(dict.fromkeys(s for s in proposal['skill_ids'] if s in skill_ids))
    notes=[]
    dropped=len(proposal['role_ids'])+len(proposal['skill_ids'])-len(roles)-len(skills)
    if dropped>0:notes.append(f'dropped {dropped} unknown catalogue id(s)')
    if not roles and not skills:return None,'no matching careers or skills in the catalogue'
    source_numbers=set(numbers_in(f"{item['title']} {item['snippet']}"))
    summary=(proposal.get('summary') or '').strip()[:MAX_SUMMARY]
    invented=[n for n in numbers_in(summary) if n not in source_numbers]
    if not summary or invented:
        if invented:notes.append(f"summary had numbers not in the source ({', '.join(invented)}); used the headline instead")
        summary=item['title']
    strength=min(MAX_INGESTED_STRENGTH,max(1,round(proposal.get('strength',1))))
    direction='declining' if proposal.get('direction')=='declining' else 'emerging'
    return {**proposal,'role_ids':roles,'skill_ids':skills,'summary':summary,'strength':strength,'direction':direction},notes
