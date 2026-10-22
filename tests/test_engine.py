import json
from pathlib import Path
from backend.engine import recommend
ROOT=Path(__file__).resolve().parents[1]
def data(f):return json.loads((ROOT/'data'/f).read_text(encoding='utf8'))
def setup():
 skills=data('skills.json');return data('roles.json'),data('demo_profile.json'),data('snapshots.json'),{s['id']:s for s in skills},data('learning_resources.json')
def test_catalogue_and_role_skills():
 roles,_,_,skills,resources=setup()
 assert len(roles)==12
 assert len(set(r['sector'] for r in roles))==6
 assert all(8<=len(r['skills'])<=10 for r in roles)
 assert all(a['skill_id'] in skills for r in roles for a in r['skills'])
 assert len(resources)==30

def test_deterministic():
 roles,p,s,skills,res=setup()
 x=recommend(roles,p,s[0],skills,res)
 y=recommend(roles,p,s[0],skills,res)
 assert x==y

def test_no_unconfirmed_skill_is_counted():
 roles,p,s,skills,res=setup()
 p['skills']={}
 x=recommend(roles,p,s[0],skills,res,selected_role='data-analyst')[0]
 assert x['readiness'] is None
 assert x['completeness']==0
 assert x['provisional'] is True
 assert all(g['status']=='unknown' for g in x['gaps'])

def test_snapshot_updates_do_not_change_user_skills():
 roles,p,s,skills,res=setup()
 a=recommend(roles,p,s[0],skills,res,selected_role='data-analyst')[0]
 b=recommend(roles,p,s[1],skills,res,selected_role='data-analyst')[0]
 assert a['gaps']==b['gaps']
 assert a['readiness']==b['readiness']
 assert b['components']['trends']!=a['components']['trends']

def test_scenarios_keep_readiness():
 roles,p,s,skills,res=setup()
 a=recommend(roles,p,s[0],skills,res,'moderate',selected_role='data-analyst')[0]
 b=recommend(roles,p,s[0],skills,res,'rapid',selected_role='data-analyst')[0]
 assert a['readiness']==b['readiness']
 assert a['gaps']==b['gaps']
