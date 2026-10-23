"""Regression checks for the module layout and preservation of v2 design."""
from pathlib import Path
from fastapi.testclient import TestClient
from backend.app import app
from scripts.build_frontend import assemble_home

ROOT=Path(__file__).resolve().parents[1]

def test_results_layout_compiles_from_editable_v2_source():
    html=assemble_home()
    assert html==(ROOT/'frontend'/'index.html').read_text(encoding='utf8')
    assert 'AI disruption scenario' in html and 'What do you enjoy? (optional)' in html
    assert 'The world of work is changing.' in html
    assert 'SAMPLE SIGNAL FEED' in html

def test_backend_endpoint_compatibility():
    api=TestClient(app)
    paths={path for path in api.get('/openapi.json').json()['paths']}
    expected={'/','/api/meta','/api/skills','/api/roles','/api/resources',
        '/api/profile','/api/matches','/api/scenarios/{role_id}', '/api/radar',
        '/api/snapshots','/api/curator/approve/{sid}', '/api/history',
        '/api/history/{history_id}', '/api/compare', '/api/extract',
        '/api/integrations', '/api/ai/skills','/support.js','/image-slot.js'}
    assert expected.issubset(paths)
    assert api.get('/').status_code==200
    assert api.get('/ai-lab').status_code==404  # the AI Lab page was removed
    assert api.get('/api/skills').status_code==200
    assert api.get('/api/scenarios/data-analyst').status_code==200

def test_start_flow_pages():
    html=assemble_home()
    for screen in ('Home','Start','Results','Pathway','Signals','About'):
        assert f'data-screen-label="{screen}"' in html
    for removed in ('Intake','Confirm','Login'):
        assert f'data-screen-label="{removed}"' not in html
    api=TestClient(app)
    for path in ('/start','/results','/pathway','/signals','/about'):
        resp=api.get(path)
        assert resp.status_code==200 and 'data-screen-label="Start"' in resp.text
    assert api.get('/confirm').status_code==404

def test_cv_upload_can_use_ai_provider_chain(monkeypatch):
    for name in ('ANTHROPIC_API_KEY','RUNPOD_API_KEY','RUNPOD_ENDPOINT_ID','RUNPOD_ENDPOINT_URL'):
        monkeypatch.delenv(name,raising=False)
    api=TestClient(app)
    cv=('cv.txt',b'I wrote SQL queries and Python scripts.','text/plain')
    legacy=api.post('/api/extract',files={'file':cv}).json()
    assert legacy['provider']=='dictionary' and legacy['candidates']
    auto=api.post('/api/extract',files={'file':cv},data={'provider':'auto'}).json()
    assert auto['provider']=='dictionary' and auto['requires_confirmation'] is True and auto['stored'] is False

def test_dictionary_and_profile_contract():
    client=TestClient(app)
    resp=client.post('/api/ai/skills',json={'text':'I used SQL queries with a team.','provider':'dictionary'})
    assert resp.status_code==200
    assert resp.json()['requires_confirmation'] is True
    assert resp.json()['stored'] is False
    assert client.get('/api/profile').status_code==200
