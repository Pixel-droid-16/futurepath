"""Regression checks for the module layout and preservation of v2 design."""
import hashlib,json
from pathlib import Path
from fastapi.testclient import TestClient
from backend.app import app
from scripts.build_frontend import assemble_home,assemble_ai_lab

ROOT=Path(__file__).resolve().parents[1]
BASELINE=json.loads((ROOT/'docs'/'ORIGINAL_FILE_HASHES.json').read_text())

def test_results_layout_compiles_from_editable_v2_source():
    html=assemble_home()
    assert html==(ROOT/'frontend'/'index.html').read_text()
    assert 'SCENARIO LAB · BACKEND CONNECTED' in html
    assert 'The world of work is changing.' in html
    assert 'LIVE SIGNAL FEED' not in html  # Sample signals must be explicitly labelled

def test_original_ai_lab_layout_identical():
    html=assemble_ai_lab()
    assert html==(ROOT/'frontend'/'ai-lab.html').read_text()
    assert hashlib.sha256(html.encode()).hexdigest()==BASELINE['frontend/ai-lab.html']

def test_backend_endpoint_compatibility():
    api=TestClient(app)
    paths={path for path in api.get('/openapi.json').json()['paths']}
    expected={'/','/ai-lab','/api/meta','/api/skills','/api/roles','/api/resources',
        '/api/profile','/api/matches','/api/scenarios/{role_id}', '/api/radar',
        '/api/snapshots','/api/curator/approve/{sid}', '/api/history',
        '/api/history/{history_id}', '/api/compare', '/api/extract',
        '/api/integrations', '/api/ai/skills','/support.js','/image-slot.js'}
    assert expected.issubset(paths)
    assert api.get('/').status_code==200
    assert api.get('/ai-lab').status_code==200
    assert api.get('/api/skills').status_code==200
    assert api.get('/api/scenarios/data-analyst').status_code==200

def test_dictionary_and_profile_contract():
    client=TestClient(app)
    resp=client.post('/api/ai/skills',json={'text':'I used SQL queries with a team.','provider':'dictionary'})
    assert resp.status_code==200
    assert resp.json()['requires_confirmation'] is True
    assert resp.json()['stored'] is False
    assert client.get('/api/profile').status_code==200
