"""Reproducible educational scoring rules, intentionally separate from the language model.

score = weighted mean of exact skill match, related-skill credit, signal-driven demand, optional profile
free-text fit, optional sector interest and (after the quiz) interest fit:
  without quiz  0.55 x skills + 0.45 x demand
  with quiz     0.45 x skills + 0.35 x demand + 0.20 x interest
When a person gives a current role, headline or goal, 0.15 is reserved for a profile-text fit; when
they choose career sectors, 0.05 is reserved for a sector prior. The remaining skills/demand weights
are renormalised, so every published formula still sums to 1.

Skill match is the importance-weighted share of the career's required skills the person has. Exact
catalogue skills score highest; a curated/embedding-derived related skill can add partial credit
(capped at 60%), but readiness stays exact-only. Unassessed skills count as missing. The +/- range
comes from how much the demand signals agree, and thin evidence is pulled toward neutral.

Ranking adds a small diversity step: careers with near-identical skill sets are spread out instead of
filling the first results with the same job under two titles.
"""
from .scenarios import scenario_details, TASKS
from .interests import interest_fit, shared_top_types, TYPE_NAMES
from .text_match import profile_text as build_profile_text
from . import semantic

DEFAULT_WEIGHTS={'with_interest':{'skill':0.45,'demand':0.35,'interest':0.20},'without_interest':{'skill':0.55,'demand':0.45,'interest':0}}
TEXT_WEIGHT=0.15
SECTOR_WEIGHT=0.05
TRANSFER_CAP=0.60
DIVERSITY_PENALTY=4.0
NEAR_DUPLICATE=0.85
DEMAND_BAND={'high':5,'medium':10,'low':18}  # half-width of the demand range (0-100) by signal confidence

def fmt(x):return f'{x:g}'

def _active_weights(has_interest,has_text,has_sector):
    """Base skill/demand share, then reserve fixed weights for interest, text and sector."""
    base=DEFAULT_WEIGHTS['with_interest' if has_interest else 'without_interest']
    fixed=base.get('interest',0.0)+(TEXT_WEIGHT if has_text else 0.0)+(SECTOR_WEIGHT if has_sector else 0.0)
    remaining=max(0.0,1.0-fixed)
    skill_demand=base['skill']+base['demand']
    weights={'skill':remaining*base['skill']/skill_demand,'demand':remaining*base['demand']/skill_demand}
    if has_interest:weights['interest']=base['interest']
    if has_text:weights['text']=TEXT_WEIGHT
    if has_sector:weights['sector']=SECTOR_WEIGHT
    return weights

def _match_skills(role,known,skill_index):
    """Exact skill score plus capped related-skill credit. Readiness remains exact-only."""
    gaps=[];assessed=earned_exact=earned_transfer=weight_total=0.0;transfer_notes=[]
    for item in role['skills']:
        sid=item['skill_id'];req=max(1,int(item['required']));weight=item['importance'];val=known.get(sid)
        weight_total+=weight
        exact_ratio=0.0
        if val is not None:
            assessed+=weight
            exact_ratio=min(max(int(val),0)/req,1.0)
            earned_exact+=exact_ratio*weight
        best_credit=0.0;best_source=None;best_similarity=0.0
        for source_id,source_val in known.items():
            if source_id==sid or source_val is None:continue
            similarity=semantic.transfer_similarity(sid,source_id)
            if similarity<=0:continue
            source_ratio=min(max(int(source_val),0)/req,1.0)
            credit=min(TRANSFER_CAP,source_ratio*similarity)
            if credit>best_credit:
                best_credit=credit;best_source=source_id;best_similarity=similarity
        extra=max(0.0,best_credit-exact_ratio)
        if extra>0:
            earned_transfer+=extra*weight
            if len(transfer_notes)<3:
                transfer_notes.append({'skill':skill_index[sid]['name'],'from':skill_index[best_source]['name'],
                                       'credit':round(100*extra,1),'similarity':round(best_similarity,2)})
        if val is None:
            status='unknown';gap=None
        else:
            status='satisfied' if exact_ratio>=1 else ('no_proficiency' if int(val)<=0 else 'partial')
            gap=max(req-int(val),0)
        gaps.append({'skill_id':sid,'name':skill_index[sid]['name'],'required':req,'confirmed':val,'importance':weight,
                     'category':item['category'],'status':status,'gap':gap,'effective_ratio':round(max(exact_ratio,best_credit),3),
                     'transfer_from':skill_index[best_source]['name'] if extra>0 and best_source else None,
                     'transfer_credit':round(100*extra,1) if extra>0 else 0,
                     'transfer_similarity':round(best_similarity,3) if extra>0 else None})
    readiness=round(100*earned_exact/assessed,1) if assessed else None
    completeness=round(100*assessed/weight_total,1) if weight_total else 0
    exact_skill=round(100*earned_exact/weight_total,1) if weight_total else 0
    transfer_skill=round(100*earned_transfer/weight_total,1) if weight_total else 0
    skill_match=round(exact_skill+transfer_skill,1)
    return {'gaps':gaps,'readiness':readiness,'completeness':completeness,'skill_match':skill_match,
            'exact_skill':exact_skill,'transfer_skill':transfer_skill,'transfer_notes':transfer_notes}

def _sector_score(profile,role):
    interests=[str(x).strip().lower() for x in (profile.get('interests') or []) if str(x).strip()]
    if not interests:return None
    return 100.0 if role['sector'].strip().lower() in interests else 0.0

def _skill_jaccard(a,b):
    left={x['skill_id'] for x in a.get('skills',[])};right={x['skill_id'] for x in b.get('skills',[])}
    union=left|right
    return len(left&right)/len(union) if union else 0.0

def _diversity_order(rows,roles):
    """Greedy rerank that defers near-duplicate career profiles, keeping every career in the list."""
    by_id={r['id']:r for r in roles}
    remaining=sorted(rows,key=lambda x:(-x['suitability'],x['role_id']));chosen=[];deferred=[]
    while remaining:
        pick=None;pick_key=None
        for row in remaining:
            similarity=max((_skill_jaccard(by_id[row['role_id']],by_id[c['role_id']]) for c in chosen),default=0.0)
            if similarity>=NEAR_DUPLICATE:continue
            adjusted=row['suitability']-DIVERSITY_PENALTY*max(0.0,similarity-0.5)
            key=(adjusted,row['suitability'],row['role_id'])
            if pick is None or key>pick_key:pick=row;pick_key=key
        if pick is None:
            deferred.extend(remaining);break
        remaining.remove(pick);chosen.append(pick)
    deferred.sort(key=lambda x:(-x['suitability'],x['role_id']))
    return chosen+deferred

def rank_role(role,profile,snapshot,skill_index,resources,scenario='moderate',demand=None,profile_text=None):
    known=profile.get('skills',{})
    skill_data=_match_skills(role,known,skill_index)
    gaps=skill_data['gaps'];readiness=skill_data['readiness'];completeness=skill_data['completeness']
    skill_match=skill_data['skill_match'];exact_skill=skill_data['exact_skill'];transfer_skill=skill_data['transfer_skill']
    # TRENDS: signal-driven demand (backend/signals/demand.py) when given; else the synthetic snapshot value.
    if demand:
        raw_trend=demand['score'];reliability=demand.get('reliability',0.5)
        base_trend=50+(raw_trend-50)*reliability
    else:
        raw_trend=snapshot['role_trend'].get(role['id'],50);reliability=None;base_trend=raw_trend
    # SCENARIO EFFECTS: explicit illustrative policy changes trend factor AND task and skill priorities.
    # Cap numerical change to avoid interpreting assumptions as observed occupational forecasts.
    # Roles without curated scenario tasks keep their snapshot trend: no fabricated exposure data.
    tasks=TASKS.get(role['id'])
    exposed=sum(t[1] for t in tasks)/3 if tasks else None
    adoption_shift=(round((exposed-50)*.22,1) if scenario=='rapid' and exposed is not None else 0)
    trend=round(max(0,min(100,base_trend+adoption_shift)),1)
    user_riasec=profile.get('riasec')
    interest=round(100*interest_fit(user_riasec,role['riasec']),1) if user_riasec and role.get('riasec') else None
    text_fit,text_source=(None,None)
    if profile_text:
        text_fit,text_source=semantic.text_fit(profile_text,role['id'])
    sector_fit=_sector_score(profile,role)
    w=_active_weights(interest is not None,text_fit is not None,sector_fit is not None)
    values={'skill':skill_match,'demand':trend}
    if interest is not None:values['interest']=interest
    if text_fit is not None:values['text']=text_fit
    if sector_fit is not None:values['sector']=sector_fit
    score=sum(w[k]*values[k] for k in w)
    band=DEMAND_BAND[demand['confidence']] if demand else DEMAND_BAND['low']
    spread=w['demand']*band
    terms=[f"{fmt(w['skill'])} × {round(skill_match)}",f"{fmt(w['demand'])} × {round(trend)}"]
    if interest is not None:terms.append(f"{fmt(w['interest'])} × {round(interest)}")
    if text_fit is not None:terms.append(f"{fmt(w['text'])} × {round(text_fit)}")
    if sector_fit is not None:terms.append(f"{fmt(w['sector'])} × {round(sector_fit)}")
    shared=[TYPE_NAMES[t] for t in shared_top_types(user_riasec,role['riasec'])] if interest is not None else []
    transfer_why=('Partial credit from related skills: '+'; '.join(f"{n['from']} → {n['skill']} ({n['credit']}%)" for n in skill_data['transfer_notes'])) if skill_data['transfer_notes'] else ''
    skill_why=(f"Exact catalogue skills {exact_skill} · related-skill credit {transfer_skill}" if transfer_skill else f"Exact catalogue skills {exact_skill}")
    if text_fit is None:
        text_why='Add a current role, headline or goal to personalise this match.'
    elif text_source=='keywords':
        text_why=f"Your stated role and goals share {round(text_fit)}/100 of this career’s key terms (offline keyword match)."
    else:
        text_why=f"Your stated role and goals match this career’s profile at {round(text_fit)}/100 (sentence-transformer similarity)."
    match={'skill':skill_match,'exact_skill':exact_skill,'transfer_skill':transfer_skill,
           'demand':trend,'demand_raw':raw_trend,'demand_reliability':reliability,
           'interest':interest,'text_fit':text_fit,'text_source':text_source,'sector':sector_fit,
           'weights':w,'score':round(score,1),'low':round(max(0,score-spread)),'high':round(min(100,score+spread)),
           'demand_band':band,'formula':' + '.join(terms)+f' = {round(score)}','interest_why':(f"You share {', '.join(shared)} interests with this career." if shared else 'Your strongest interests differ from this career’s.') if interest is not None else 'Take the interest quiz to add interest fit.',
           'text_why':text_why,'transfer_why':transfer_why,'skill_why':skill_why}
    partial=sum(g['status']=='partial' for g in gaps)
    unknown_effective=sum(max(0.0,1-(g['transfer_credit']/100)*0.5) for g in gaps if g['status']=='unknown')
    feasibility=round(max(0,100-30*partial/len(gaps)-45*unknown_effective/len(gaps)),1) if gaps else 0.0
    essential=[g for g in gaps if g['category']=='essential']
    provisional=completeness<60 or any(g['status']=='unknown' for g in essential)
    priorities=[]
    for g in gaps:
        if g['status']=='satisfied':continue
        factor=(2.6 if g['category']=='emerging' else 1.3 if g['category']=='supporting' else 1.05) if scenario=='rapid' else (1.05 if g['category']=='emerging' else 1.4 if g['category']=='essential' else 1)
        urgency=g['gap']/g['required'] if g['gap'] is not None else .6
        if g['transfer_credit']:urgency*=max(.35,1-g['transfer_credit']/100)
        priority=round(g['importance']*urgency*factor,2)
        priorities.append({'skill':g['name'],'skill_id':g['skill_id'],'status':g['status'],'priority':priority,'why':('Assess this skill before claiming a gap' if g['status']=='unknown' else f"Required {g['required']}/5, confirmed {g['confirmed']}/5")+('; accelerated adoption raises AI-related urgency' if scenario=='rapid' and g['category']=='emerging' else ''),'resources':[r for r in resources if r['skill_id']==g['skill_id']][:3],'category':g['category']})
    priorities.sort(key=lambda p:-p['priority'])
    details=scenario_details(role['id'],scenario)
    return {'role_id':role['id'],'title':role['title'],'sector':role['sector'],'suitability':round(score,1),'readiness':readiness,'completeness':completeness,'provisional':provisional,
            'components':{'skills':skill_match,'exact_skills':exact_skill,'transfer_skills':transfer_skill,'interests':interest,'trends':trend,'text':text_fit,'sector':sector_fit,'feasibility':feasibility},'match':match,'gaps':gaps,'pathway':priorities,
            'sdgs':role['sdgs'],'sdg_justification':role['sdg_justification'],'qualification_note':role['qualification_note'],'snapshot_id':snapshot['id'],'scenario':scenario,'scenario_details':details,'assumption_shift':adoption_shift,
            'trend_source':'signals' if demand else 'snapshot','signals':{k:demand.get(k) for k in ('signal_count','confidence','reliability','cited')} if demand else None}

def recommend(roles,profile,snapshot,skill_index,resources,scenario='moderate',selected_role=None,demand=None):
    chosen=[r for r in roles if r['id']==selected_role] if selected_role else roles
    text=build_profile_text(profile)
    rows=[rank_role(r,profile,snapshot,skill_index,resources,scenario,(demand or {}).get(r['id']),profile_text=text) for r in chosen]
    if selected_role:return sorted(rows,key=lambda x:(-x['suitability'],x['role_id']))
    return _diversity_order(rows,roles)
