"""Reproducible educational scoring rules, intentionally separate from the language model.

score = weighted mean of skill match, signal-driven demand and (after the quiz) interest fit, as shown on each card:
  without the quiz  0.55 x skills + 0.45 x demand
  with the quiz     0.45 x skills + 0.35 x demand + 0.20 x interest
Skill match is the importance-weighted share of the career's required skills the person has (partial credit below the
required level; unassessed skills count as missing). The +/- range comes from how much the demand signals agree.
"""
from .scenarios import scenario_details, TASKS
from .interests import interest_fit, shared_top_types, TYPE_NAMES

DEFAULT_WEIGHTS={'with_interest':{'skill':0.45,'demand':0.35,'interest':0.20},'without_interest':{'skill':0.55,'demand':0.45,'interest':0}}
DEMAND_BAND={'high':5,'medium':10,'low':18}  # half-width of the demand range (0-100) by signal confidence

def fmt(x):return f'{x:g}'

def rank_role(role, profile, snapshot, skill_index, resources, scenario='moderate', demand=None):
    known=profile.get('skills',{})
    gaps=[]; assessed=earned=weight_total=0
    for item in role['skills']:
        sid=item['skill_id']; req=item['required']; weight=item['importance']; val=known.get(sid)
        weight_total+=weight
        if val is None: status='unknown'; gap=None
        else:
            assessed+=weight; ratio=min(int(val)/req,1); earned+=ratio*weight
            status='satisfied' if ratio==1 else ('no_proficiency' if val==0 else 'partial')
            gap=max(req-int(val),0)
        gaps.append({'skill_id':sid,'name':skill_index[sid]['name'],'required':req,'confirmed':val,'importance':weight,'category':item['category'],'status':status,'gap':gap})
    readiness=round(100*earned/assessed,1) if assessed else None
    completeness=round(100*assessed/weight_total,1) if weight_total else 0
    skill_match=round(100*earned/weight_total,1) if weight_total else 0
    # TRENDS: signal-driven demand (backend/signals/demand.py) when given; else the synthetic snapshot value.
    base_trend=demand['score'] if demand else snapshot['role_trend'].get(role['id'],50)
    # SCENARIO EFFECTS: explicit illustrative policy changes trend factor AND task and skill priorities.
    # Cap numerical change to avoid interpreting assumptions as observed occupational forecasts.
    # Roles without curated scenario tasks keep their snapshot trend: no fabricated exposure data.
    tasks=TASKS.get(role['id'])
    exposed=sum(t[1] for t in tasks)/3 if tasks else None
    adoption_shift=(round((exposed-50)*.22,1) if scenario=='rapid' and exposed is not None else 0)
    trend=round(max(0,min(100,base_trend+adoption_shift)),1)
    user_riasec=profile.get('riasec')
    interest=round(100*interest_fit(user_riasec,role['riasec']),1) if user_riasec and role.get('riasec') else None
    w=DEFAULT_WEIGHTS['with_interest' if interest is not None else 'without_interest']
    total=w['skill']+w['demand']+w['interest']
    score=(w['skill']*skill_match+w['demand']*trend+w['interest']*(interest or 0))/total
    band=DEMAND_BAND[demand['confidence']] if demand else DEMAND_BAND['low']
    spread=w['demand']*band/total
    terms=[f"{fmt(w['skill'])} × {round(skill_match)}",f"{fmt(w['demand'])} × {round(trend)}"]+([f"{fmt(w['interest'])} × {round(interest)}"] if interest is not None else [])
    shared=[TYPE_NAMES[t] for t in shared_top_types(user_riasec,role['riasec'])] if interest is not None else []
    match={'skill':skill_match,'demand':trend,'interest':interest,'weights':w,'score':round(score,1),'low':round(max(0,score-spread)),
           'high':round(min(100,score+spread)),'demand_band':band,'formula':' + '.join(terms)+f' = {round(score)}',
           'interest_why':(f"You share {', '.join(shared)} interests with this career." if shared else 'Your strongest interests differ from this career’s.') if interest is not None else 'Take the interest quiz to add interest fit.'}
    unknowns=sum(g['status']=='unknown' for g in gaps)
    partial=sum(g['status']=='partial' for g in gaps)
    feasibility=round(max(0,100-30*partial/len(gaps)-45*unknowns/len(gaps)),1)
    essential=[g for g in gaps if g['category']=='essential']
    provisional=completeness<60 or any(g['status']=='unknown' for g in essential)
    priorities=[]
    for g in gaps:
        if g['status']=='satisfied':continue
        factor=(2.6 if g['category']=='emerging' else 1.3 if g['category']=='supporting' else 1.05) if scenario=='rapid' else (1.05 if g['category']=='emerging' else 1.4 if g['category']=='essential' else 1)
        urgency=g['gap']/g['required'] if g['gap'] is not None else .6
        priority=round(g['importance']*urgency*factor,2)
        priorities.append({'skill':g['name'],'skill_id':g['skill_id'],'status':g['status'],'priority':priority,'why':('Assess this skill before claiming a gap' if g['status']=='unknown' else f"Required {g['required']}/5, confirmed {g['confirmed']}/5")+('; accelerated adoption raises AI-related urgency' if scenario=='rapid' and g['category']=='emerging' else ''),'resources':[r for r in resources if r['skill_id']==g['skill_id']][:3],'category':g['category']})
    priorities.sort(key=lambda p:-p['priority'])
    details=scenario_details(role['id'],scenario)
    return {'role_id':role['id'],'title':role['title'],'sector':role['sector'],'suitability':round(score,1),'readiness':readiness,'completeness':completeness,'provisional':provisional,
            'components':{'skills':skill_match,'interests':interest,'trends':trend,'feasibility':feasibility},'match':match,'gaps':gaps,'pathway':priorities,
            'sdgs':role['sdgs'],'sdg_justification':role['sdg_justification'],'qualification_note':role['qualification_note'],'snapshot_id':snapshot['id'],'scenario':scenario,'scenario_details':details,'assumption_shift':adoption_shift,
            'trend_source':'signals' if demand else 'snapshot','signals':{k:demand[k] for k in ('signal_count','confidence','cited')} if demand else None}

def recommend(roles,profile,snapshot,skill_index,resources,scenario='moderate',selected_role=None,demand=None):
    chosen=[r for r in roles if r['id']==selected_role] if selected_role else roles
    return sorted([rank_role(r,profile,snapshot,skill_index,resources,scenario,(demand or {}).get(r['id'])) for r in chosen],key=lambda x:-x['suitability'])
