from backend.app import app
from fastapi.testclient import TestClient
from backend.scenarios import scenario_details
from backend.engine import recommend
from backend.app import ROLES, SKILL_INDEX, RESOURCES, load

client=TestClient(app)
def test_scenario_comparison_has_distinct_tasks_and_priorities():
    a=client.get('/api/scenarios/data-analyst')
    assert a.status_code==200
    d=a.json()
    assert d['moderate']['scenario_details']['tasks'][0]['adoption_impact']!=d['rapid']['scenario_details']['tasks'][0]['adoption_impact']
    assert d['moderate']['pathway'][:5]!=d['rapid']['pathway'][:5]
    assert d['moderate']['readiness']==d['rapid']['readiness']
    assert d['moderate']['completeness']==d['rapid']['completeness']
def test_user_skills_do_not_change_between_scenarios():
    p=load('demo_profile.json');s=load('snapshots.json')[0]
    before=dict(p['skills'])
    a=recommend(ROLES,p,s,SKILL_INDEX,RESOURCES,'moderate','data-analyst')[0]
    b=recommend(ROLES,p,s,SKILL_INDEX,RESOURCES,'rapid','data-analyst')[0]
    assert p['skills']==before
    assert a['components']['skills']==b['components']['skills']
def test_unknowns_are_not_assumed_zero():
    p={'skills':{},'interests':[]}
    r=recommend(ROLES,p,load('snapshots.json')[0],SKILL_INDEX,RESOURCES,'rapid','data-analyst')[0]
    assert r['readiness'] is None
    assert all(g['gap'] is None for g in r['gaps'])
def test_integrations_not_reveal_secrets():
    r=client.get('/api/integrations')
    assert r.status_code==200
    assert 'api_key' not in str(r.json()).lower()
