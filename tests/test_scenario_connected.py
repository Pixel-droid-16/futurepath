"""Acceptance contract for the live v2 scenario connection (synthetic evidence)."""
from pathlib import Path
from fastapi.testclient import TestClient
from backend.app import app

ROOT=Path(__file__).resolve().parents[1]

def test_all_careers_from_backend_have_two_real_scenarios():
    client=TestClient(app)
    m=client.get('/api/matches?scenario=moderate').json()
    r=client.get('/api/matches?scenario=rapid').json()
    assert len(m)==44==len(r)
    by_m={x['role_id']:x for x in m};by_r={x['role_id']:x for x in r}
    assert by_m.keys()==by_r.keys()
    for key in by_m:
        assert by_m[key]['snapshot_id']==by_r[key]['snapshot_id']
        assert by_m[key]['gaps']==by_r[key]['gaps']  # Confirmed proficiency must not change
        assert by_m[key]['scenario']=='moderate'
        assert by_r[key]['scenario']=='rapid'
    assert any([p['skill'] for p in by_m[k]['pathway'][:4]] != [p['skill'] for p in by_r[k]['pathway'][:4]] for k in by_m)

def test_rapid_scenario_moves_demand_and_ranking_through_ai_signals():
    from backend.catalog import load
    from backend.services.recommendations import result
    signals=load('signals.json')  # curated baseline only, so the test doesn't depend on refreshed feeds
    m=result(scenario='moderate',signals=signals);r=result(scenario='rapid',signals=signals)
    assert [x['role_id'] for x in m]!=[x['role_id'] for x in r]  # the order of careers changes
    by_m={x['role_id']:x for x in m}
    for x in r:
        mod=by_m[x['role_id']]
        assert x['assumption_shift']==round(x['match']['demand']-mod['match']['demand'],1)
        assert x['match']['skill']==mod['match']['skill']  # only demand moves; skill match never does
        if x['signals']['ai_signal_count']==0:assert x['match']['demand']==mod['match']['demand']
    assert max(abs(x['assumption_shift']) for x in r)>=5

def test_task_impacts_and_priorities_are_exposed_by_api_and_original_v2_ui():
    client=TestClient(app)
    obj=client.get('/api/scenarios/data-analyst').json()
    assert 'hypothetical' in obj['notice'].lower()
    assert obj['moderate']['scenario_details']['tasks'][0]['adoption_impact'] != obj['rapid']['scenario_details']['tasks'][0]['adoption_impact']
    assert obj['moderate']['scenario_details']['recommended_action'] != obj['rapid']['scenario_details']['recommended_action']
    original=(ROOT/'frontend'/'index.html').read_text(encoding='utf8')
    assert 'Fast AI disruption' in original and '{{ setFast }}' in original  # the results scenario toggle
    assert 'The world of work is changing.' in original
