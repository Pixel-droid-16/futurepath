import os
from pathlib import Path
os.environ['FUTUREPATH_DB']='/tmp/futurepath_test_api.sqlite3'
from fastapi.testclient import TestClient
from backend.app import app
c=TestClient(app)
def test_demo_flow():
 # Restore synthetic baseline on each run, so repeated test runs are deterministic.
 assert c.post('/api/curator/approve/S1').status_code==200
 roles=c.get('/api/roles').json()
 assert len(roles)==44
 assert c.get('/api/meta').json()['ai_status'].startswith('manual')
 original=c.get('/api/radar').json()['snapshot']['id']
 assert original=='S1'
 record=c.post('/api/history',json={'role_id':'data-analyst'}).json()
 assert record['snapshot_id']=='S1'
 assert c.post('/api/curator/approve/S2').status_code==200
 assert c.get('/api/radar').json()['snapshot']['id']=='S2'
 compare=c.post('/api/compare',json={'history_id':record['id']}).json()
 assert compare['old_snapshot']=='S1'
 assert compare['new_snapshot']=='S2'
 assert compare['profile_unchanged']
 assert c.delete('/api/history/'+str(record['id'])).status_code==200
 assert all(r['id']!=record['id'] for r in c.get('/api/history').json())
