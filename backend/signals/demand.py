"""Signal-driven demand: the Trends score for each career. Constants are modelling choices, not facts.

contribution = +/-strength x 0.5^(age in days / 365). A signal counts in full when it names the career, and at
0.5 x importance/3 through the most important required skill it names otherwise. Skill-path signals add at most
+/-2 to a career and feed signals naming it at most +/-3, so a burst of similar news can't outweigh curated reports.
Trends = 100 x (0.5 + 0.5 x tanh(raw / 5)), so 50 means no net signal.
"""
import math
from datetime import date

RECENCY_HALF_LIFE_DAYS=365
SKILL_SIGNAL_FACTOR=0.5
SKILL_PATH_CAP=2
FEED_PATH_CAP=3
DEMAND_SQUASH_K=5
CONFIDENCE={'high':(4,0.7),'medium':(2,0.4)}  # (minimum signals, minimum agreement)

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

def role_demand(role,signals,as_of=None,skill_names=None):
    """Trends score (0-100) for one career, with the signals behind it (source and date) for the UI."""
    as_of=as_of or date.today()
    contribs=contributions(role,signals,as_of)
    raw=sum(c['value'] for c in contribs)
    cited=[{'title':c['signal']['title'],'source':c['signal']['source_name'],'date':c['signal']['published_date'],'url':c['signal']['url'],
            'direction':c['signal']['direction'],'tagged_by':c['signal']['tagged_by'],
            'via':'names this career' if c['via']=='direct' else 'via '+(skill_names or {}).get(c['via'],c['via'])} for c in contribs[:3]]
    return {'score':round(100*(0.5+0.5*math.tanh(raw/DEMAND_SQUASH_K)),1),'raw':round(raw,3),'signal_count':len(contribs),
            'confidence':confidence_of(contribs),'cited':cited}

def demand_map(roles,signals,as_of=None,skill_names=None):
    return {r['id']:role_demand(r,signals,as_of,skill_names) for r in roles}
