<<<<<<< HEAD
"""Start flow backend: interest quiz, profile fields and the screenshot scoring formula."""
from fastapi.testclient import TestClient
from backend import storage
from backend.app import app
from backend.interests import score_quiz,interest_fit,riasec_code

def test_quiz_scoring_matches_laluanku():
    assert score_quiz({})=={t:0.5 for t in 'RIASEC'}  # unanswered items count as neutral
    investigative={i:(5 if t=='I' else 1) for i,t in [(q,'RIASEC'[(q-1)%6]) for q in range(1,19)]}
    scores=score_quiz(investigative)
    assert scores['I']==1 and scores['R']==0 and riasec_code(scores)[0]=='I'
    data_scientist={"R":0.19,"I":1,"A":0.27,"S":0.11,"E":0.12,"C":0.73}
    assert interest_fit(scores,data_scientist)>0.8 and interest_fit(score_quiz({}),data_scientist)==0.5

def test_profile_quiz_and_score_formula(tmp_path,monkeypatch):
    monkeypatch.setattr(storage,'DB',tmp_path/'profile.sqlite3');storage.init()
    api=TestClient(app)
    quiz=api.get('/api/interest-quiz').json()
    assert len(quiz['questions'])==18 and len(quiz['likert'])==5
    base={'skills':{'SK001':4,'SK002':3},'name':'Test','study_hours':10,'current_role':'Operations Associate',
          'qualification':'Malaysian Certificate of Education (SPM)','industry':'Business Operations','interests':['AI Automation','Sustainable Energy'],
          'ai_comfort':'Intermediate','work_arrangement':'Remote','career_motivation':'Explore a different career direction'}
    saved=api.put('/api/profile',json=base).json()
    assert saved['riasec'] is None and saved['name']=='Test'
    assert saved['current_role']=='Operations Associate' and saved['industry']=='Business Operations'
    assert saved['qualification']=='Malaysian Certificate of Education (SPM)' and saved['interests']==['AI Automation','Sustainable Energy']
    assert saved['ai_comfort']=='Intermediate' and saved['work_arrangement']=='Remote'
    assert saved['career_motivation']=='Explore a different career direction'
    m=next(r for r in api.get('/api/matches').json() if r['role_id']=='data-analyst')['match']
    assert m['interest'] is None and m['weights']['skill']==0.55 and m['formula'].startswith('0.55 × ')
    assert m['low']<=m['score']<=m['high']
    answers={q['id']:(5 if q['type'] in 'IC' else 1) for q in quiz['questions']}
    saved=api.put('/api/profile',json={**base,'quiz_answers':answers}).json()
    assert saved['riasec_code'][:2] in ('IC','CI') and 'riasec' in saved
    m=next(r for r in api.get('/api/matches').json() if r['role_id']=='data-analyst')['match']
    assert m['interest']>70 and m['weights']['interest']==0.2 and ' + 0.2 × ' in m['formula']
    assert api.put('/api/profile',json={**base,'quiz_answers':{'99':3}}).status_code==400

def test_pathway_uses_every_checked_course(tmp_path,monkeypatch):
    monkeypatch.setattr(storage,'DB',tmp_path/'courses.sqlite3');storage.init()
    api=TestClient(app)
    # An old saved profile may still carry a "budget"; it is ignored and never filters courses.
    api.put('/api/profile',json={'skills':{},'budget':'free'})
    steps=[p for r in api.get('/api/matches').json() for p in r['pathway']]
    costs={c['cost'] for p in steps for c in p['resources'] if c.get('url')}
    assert {'Free','Low cost (paid certificate)'}<=costs and any(c.startswith('HRD Corp') for c in costs)
    assert max(len(p['resources']) for p in steps)==3  # main course plus up to two alternatives
    order=['Free','Low cost (paid certificate)']
    for p in steps:  # cheapest first
        ranks=[order.index(c['cost']) if c['cost'] in order else 2 for c in p['resources'] if c.get('url')]
        assert ranks==sorted(ranks)

def test_saved_people_keep_separate_results(tmp_path,monkeypatch):
    monkeypatch.setattr(storage,'DB',tmp_path/'people.sqlite3');storage.init()
    api=TestClient(app)
    one=api.post('/api/profiles',json={'name':'Person 1','skills':{'SK010':4,'SK011':4,'SK012':4}}).json()
    two=api.post('/api/profiles',json={'name':'Person 2','skills':{'SK001':4,'SK002':3,'SK003':4}}).json()
    assert one['id']!=two['id'] and {p['name'] for p in api.get('/api/profiles').json()}=={'Person 1','Person 2'}
    top=lambda pid:api.get('/api/matches',params={'profile':pid}).json()[0]['role_id']
    assert top(one['id'])=='cybersecurity-analyst' and top(two['id'])=='data-analyst'
    # Updating Person 2 leaves Person 1 untouched, and the shared demo profile is separate from both.
    api.put(f"/api/profiles/{two['id']}",json={'name':'Person 2','skills':{'SK001':1}})
    assert api.get(f"/api/profiles/{one['id']}").json()['skills']=={'SK010':4,'SK011':4,'SK012':4}
    assert api.get('/api/profile').json()['id']=='demo'
    assert api.get('/api/scenarios/data-analyst',params={'profile':one['id']}).status_code==200
    assert api.get('/api/what-changed',params={'profile':one['id']}).status_code==200
    assert api.get('/api/profiles/nobody').status_code==404 and api.get('/api/matches',params={'profile':'nobody'}).status_code==404

def test_delete_saved_person(tmp_path,monkeypatch):
    monkeypatch.setattr(storage,'DB',tmp_path/'delete.sqlite3');storage.init()
    api=TestClient(app)
    one=api.post('/api/profiles',json={'name':'Person 1','skills':{'SK001':3}}).json()
    api.put('/api/profile',json={'name':'Shared','skills':{'SK002':3}})
    assert {p['name'] for p in api.get('/api/profiles').json()}=={'Person 1','Shared'}
    assert api.delete(f"/api/profiles/{one['id']}").status_code==204
    assert api.get(f"/api/profiles/{one['id']}").status_code==404
    # The shared demo profile is reset, not removed, so the app keeps a default profile.
    assert api.delete('/api/profiles/demo').status_code==204
    assert api.get('/api/profiles').json()==[] and api.get('/api/profile').status_code==200
    assert api.delete('/api/profiles/nobody').status_code==404
=======
"""Start flow backend: interest quiz, profile fields and the screenshot scoring formula."""
from fastapi.testclient import TestClient
from backend import storage
from backend.app import app
from backend.interests import score_quiz,interest_fit,riasec_code

def test_quiz_scoring_matches_laluanku():
    assert score_quiz({})=={t:0.5 for t in 'RIASEC'}  # unanswered items count as neutral
    investigative={i:(5 if t=='I' else 1) for i,t in [(q,'RIASEC'[(q-1)%6]) for q in range(1,19)]}
    scores=score_quiz(investigative)
    assert scores['I']==1 and scores['R']==0 and riasec_code(scores)[0]=='I'
    data_scientist={"R":0.19,"I":1,"A":0.27,"S":0.11,"E":0.12,"C":0.73}
    assert interest_fit(scores,data_scientist)>0.8 and interest_fit(score_quiz({}),data_scientist)==0.5

def test_profile_quiz_and_score_formula(tmp_path,monkeypatch):
    monkeypatch.setattr(storage,'DB',tmp_path/'profile.sqlite3');storage.init()
    api=TestClient(app)
    quiz=api.get('/api/interest-quiz').json()
    assert len(quiz['questions'])==18 and len(quiz['likert'])==5
    base={'skills':{'SK001':4,'SK002':3},'name':'Test','study_hours':10}
    saved=api.put('/api/profile',json=base).json()
    assert saved['riasec'] is None and saved['name']=='Test'
    m=next(r for r in api.get('/api/matches').json() if r['role_id']=='data-analyst')['match']
    assert m['interest'] is None and m['weights']['skill']==0.55 and m['formula'].startswith('0.55 × ')
    assert m['low']<=m['score']<=m['high']
    answers={q['id']:(5 if q['type'] in 'IC' else 1) for q in quiz['questions']}
    saved=api.put('/api/profile',json={**base,'quiz_answers':answers}).json()
    assert saved['riasec_code'][:2] in ('IC','CI') and 'riasec' in saved
    m=next(r for r in api.get('/api/matches').json() if r['role_id']=='data-analyst')['match']
    assert m['interest']>70 and m['weights']['interest']==0.2 and ' + 0.2 × ' in m['formula']
    assert api.put('/api/profile',json={**base,'quiz_answers':{'99':3}}).status_code==400

def test_pathway_uses_every_checked_course(tmp_path,monkeypatch):
    monkeypatch.setattr(storage,'DB',tmp_path/'courses.sqlite3');storage.init()
    api=TestClient(app)
    # An old saved profile may still carry a "budget"; it is ignored and never filters courses.
    api.put('/api/profile',json={'skills':{},'budget':'free'})
    steps=[p for r in api.get('/api/matches').json() for p in r['pathway']]
    costs={c['cost'] for p in steps for c in p['resources'] if c.get('url')}
    assert {'Free','Low cost (paid certificate)'}<=costs and any(c.startswith('HRD Corp') for c in costs)
    assert max(len(p['resources']) for p in steps)==3  # main course plus up to two alternatives
    order=['Free','Low cost (paid certificate)']
    for p in steps:  # cheapest first
        ranks=[order.index(c['cost']) if c['cost'] in order else 2 for c in p['resources'] if c.get('url')]
        assert ranks==sorted(ranks)

def test_saved_people_keep_separate_results(tmp_path,monkeypatch):
    monkeypatch.setattr(storage,'DB',tmp_path/'people.sqlite3');storage.init()
    api=TestClient(app)
    one=api.post('/api/profiles',json={'name':'Person 1','skills':{'SK010':4,'SK011':4,'SK012':4}}).json()
    two=api.post('/api/profiles',json={'name':'Person 2','skills':{'SK001':4,'SK002':3,'SK003':4}}).json()
    assert one['id']!=two['id'] and {p['name'] for p in api.get('/api/profiles').json()}=={'Person 1','Person 2'}
    top=lambda pid:api.get('/api/matches',params={'profile':pid}).json()[0]['role_id']
    assert top(one['id'])=='cybersecurity-analyst' and top(two['id'])=='data-analyst'
    # Updating Person 2 leaves Person 1 untouched, and the shared demo profile is separate from both.
    api.put(f"/api/profiles/{two['id']}",json={'name':'Person 2','skills':{'SK001':1}})
    assert api.get(f"/api/profiles/{one['id']}").json()['skills']=={'SK010':4,'SK011':4,'SK012':4}
    assert api.get('/api/profile').json()['id']=='demo'
    assert api.get('/api/scenarios/data-analyst',params={'profile':one['id']}).status_code==200
    assert api.get('/api/what-changed',params={'profile':one['id']}).status_code==200
    assert api.get('/api/profiles/nobody').status_code==404 and api.get('/api/matches',params={'profile':'nobody'}).status_code==404

def test_delete_saved_person(tmp_path,monkeypatch):
    monkeypatch.setattr(storage,'DB',tmp_path/'delete.sqlite3');storage.init()
    api=TestClient(app)
    one=api.post('/api/profiles',json={'name':'Person 1','skills':{'SK001':3}}).json()
    api.put('/api/profile',json={'name':'Shared','skills':{'SK002':3}})
    assert {p['name'] for p in api.get('/api/profiles').json()}=={'Person 1','Shared'}
    assert api.delete(f"/api/profiles/{one['id']}").status_code==204
    assert api.get(f"/api/profiles/{one['id']}").status_code==404
    # The shared demo profile is reset, not removed, so the app keeps a default profile.
    assert api.delete('/api/profiles/demo').status_code==204
    assert api.get('/api/profiles').json()==[] and api.get('/api/profile').status_code==200
    assert api.delete('/api/profiles/nobody').status_code==404
>>>>>>> da0787dab49148d066631b796b12e2b882c85231
