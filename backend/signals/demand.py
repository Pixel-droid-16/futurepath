"""Signal-driven demand: the Trends score for each career. Constants are modelling choices, not facts.

contribution = +/-strength x 0.5^(age in days / 365). A signal counts in full when it names the career, and at
0.5 x importance/3 through the most important required skill it names otherwise. Skill-path signals add at most
+/-2 to a career and feed signals naming it at most +/-3, so a burst of similar news can't outweigh curated reports.
Trends = 100 x (0.5 + 0.5 x tanh(raw / 5)), so 50 means no net signal.

Rapid AI scenario: after the caps, every AI-related signal (its headline or summary mentions AI, automation, machine
learning, generative AI, robots...) counts RAPID_AI_WEIGHT times, in whichever direction it points. Other signals are
unchanged, so careers whose evidence is mostly about AI move furthest and careers with no AI evidence don't move.
"""
import math
import re
from datetime import date

RECENCY_HALF_LIFE_DAYS=365
SKILL_SIGNAL_FACTOR=0.5
SKILL_PATH_CAP=2
FEED_PATH_CAP=3
DEMAND_SQUASH_K=5
CONFIDENCE={'high':(4,0.7),'medium':(2,0.4)}  # (minimum signals, minimum agreement)
RAPID_AI_WEIGHT=2
AI_TERMS=re.compile(r'(?-i:\bA\.?I\b)|\b(?:artificial intelligence|generative|machine learning|deep learning|llms?|'
                    r'large language models?|chatgpt|copilot|chatbots?|automation|automated|automating|robots?|robotics)\b',re.I)

def is_ai_related(signal):
    """Keyword rule, so anyone can check which signals the Rapid scenario weights up."""
    return bool(AI_TERMS.search(signal['title']+' '+(signal.get('summary') or '')))

def recency_decay(published,as_of):
    """0.5^(age / half-life). Future-dated signals count as new."""
    age=max(0,(as_of-date.fromisoformat(published)).days)
    return 0.5**(age/RECENCY_HALF_LIFE_DAYS)

def cap_group(group,cap):
    total=sum(abs(c['value']) for c in group)
    if total>cap:
        for c in group:c['value']*=cap/total

def contributions(role,signals,as_of):
    importance={s['skill_id']:s['importance'] for s in role['skills']}
    out=[]
    for s in signals:
        sign=1 if s['direction']=='emerging' else -1
        decay=recency_decay(s['published_date'],as_of)
        base={'signal':s,'decay':decay,'from_feed':s['tagged_by']!='curated'}
        if role['id'] in s['role_ids']:
            out.append({**base,'value':sign*s['strength']*decay,'via':'direct'});continue
        best=max((k for k in s['skill_ids'] if k in importance),key=lambda k:importance[k],default=None)
        if best:out.append({**base,'value':sign*s['strength']*decay*SKILL_SIGNAL_FACTOR*importance[best]/3,'via':best})
    cap_group([c for c in out if c['via']!='direct'],SKILL_PATH_CAP)
    cap_group([c for c in out if c['via']=='direct' and c['from_feed']],FEED_PATH_CAP)
    return sorted(out,key=lambda c:-abs(c['value']))

def confidence_of(contribs):
    total=sum(abs(c['value']) for c in contribs)
    agreement=abs(sum(c['value'] for c in contribs))/total if total else 0
    for level,(n,a) in CONFIDENCE.items():
        if len(contribs)>=n and agreement>=a:return level
    return 'low'

def squash(raw):return round(100*(0.5+0.5*math.tanh(raw/DEMAND_SQUASH_K)),1)

def role_demand(role,signals,as_of=None,skill_names=None,scenario='moderate'):
    """Trends score (0-100) for one career under a scenario, with the signals behind it (source and date) for the UI.
    baseline_score is the Moderate score, so the UI can show what the scenario changed."""
    as_of=as_of or date.today()
    contribs=contributions(role,signals,as_of)
    baseline=sum(c['value'] for c in contribs)
    # Confidence is how much the evidence agrees, so it comes from the unweighted signals and is the same in every scenario.
    confidence=confidence_of(contribs)
    for c in contribs:
        c['ai']=is_ai_related(c['signal'])
        if scenario=='rapid' and c['ai']:c['value']*=RAPID_AI_WEIGHT
    contribs.sort(key=lambda c:-abs(c['value']))
    raw=sum(c['value'] for c in contribs)
    cited=[{'title':c['signal']['title'],'source':c['signal']['source_name'],'date':c['signal']['published_date'],'url':c['signal']['url'],
            'direction':c['signal']['direction'],'tagged_by':c['signal']['tagged_by'],'ai_related':c['ai'],
            'via':'names this career' if c['via']=='direct' else 'via '+(skill_names or {}).get(c['via'],c['via'])} for c in contribs[:3]]
    return {'score':squash(raw),'baseline_score':squash(baseline),'raw':round(raw,3),'signal_count':len(contribs),
            'ai_signal_count':sum(c['ai'] for c in contribs),'confidence':confidence,'cited':cited}

def demand_map(roles,signals,as_of=None,skill_names=None,scenario='moderate'):
    return {r['id']:role_demand(r,signals,as_of,skill_names,scenario) for r in roles}
