"""Reproducible educational scoring rules, intentionally separate from the language model."""
from .scenarios import scenario_details, TASKS

def rank_role(role, profile, snapshot, skill_index, resources, scenario='moderate'):
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
    interest=90 if role['sector'] in profile.get('interests',[]) else 45
    base_trend=snapshot['role_trend'].get(role['id'],50)
    # SCENARIO EFFECTS: explicit illustrative policy changes trend factor AND task and skill priorities.
    # Cap numerical change to avoid interpreting assumptions as observed occupational forecasts.
    exposed=sum(t[1] for t in TASKS[role['id']])/3
    adoption_shift=(round((exposed-50)*.22,1) if scenario=='rapid' else 0)
    trend=max(0,min(100,base_trend+adoption_shift))
    unknowns=sum(g['status']=='unknown' for g in gaps)
    partial=sum(g['status']=='partial' for g in gaps)
    feasibility=round(max(0,100-30*partial/len(gaps)-45*unknowns/len(gaps)),1)
    weighted_skill=readiness or 0
    suitability=round(.45*weighted_skill+.20*interest+.20*trend+.15*feasibility,1)
    essential=[g for g in gaps if g['category']=='essential']
    provisional=completeness<60 or any(g['status']=='unknown' for g in essential)
    priorities=[]
    for g in gaps:
        if g['status']=='satisfied':continue
        factor=(2.6 if g['category']=='emerging' else 1.3 if g['category']=='supporting' else 1.05) if scenario=='rapid' else (1.05 if g['category']=='emerging' else 1.4 if g['category']=='essential' else 1)
        urgency=g['gap']/g['required'] if g['gap'] is not None else .6
        priority=round(g['importance']*urgency*factor,2)
        priorities.append({'skill':g['name'],'skill_id':g['skill_id'],'status':g['status'],'priority':priority,'why':('Assess this skill before claiming a gap' if g['status']=='unknown' else f"Required {g['required']}/5, confirmed {g['confirmed']}/5")+('; accelerated adoption raises AI-related urgency' if scenario=='rapid' and g['category']=='emerging' else ''),'resources':[r for r in resources if r['skill_id']==g['skill_id']][:2],'category':g['category']})
    priorities.sort(key=lambda p:-p['priority'])
    details=scenario_details(role['id'],scenario)
    return {'role_id':role['id'],'title':role['title'],'sector':role['sector'],'suitability':suitability,'readiness':readiness,'completeness':completeness,'provisional':provisional,'components':{'skills':weighted_skill,'interests':interest,'trends':round(trend,1),'feasibility':feasibility},'gaps':gaps,'pathway':priorities,'sdgs':role['sdgs'],'sdg_justification':role['sdg_justification'],'qualification_note':role['qualification_note'],'snapshot_id':snapshot['id'],'scenario':scenario,'scenario_details':details,'assumption_shift':adoption_shift}

def recommend(roles,profile,snapshot,skill_index,resources,scenario='moderate',selected_role=None):
    chosen=[r for r in roles if r['id']==selected_role] if selected_role else roles
    return sorted([rank_role(r,profile,snapshot,skill_index,resources,scenario) for r in chosen],key=lambda x:-x['suitability'])
