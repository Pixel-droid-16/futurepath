<<<<<<< HEAD
"""Saved people. Each person who goes through Start gets their own profile id.

/api/profile is the original shared 'demo' profile (kept for compatibility); /api/profiles/{id} are saved people.
There are no user accounts: everyone using this server can see the list, so use fictional CVs.
"""
import secrets
from datetime import datetime,timezone
from fastapi import APIRouter,HTTPException
from ..catalog import SKILL_INDEX
from ..interests import QUESTIONS,LIKERT,TYPES,TYPE_NAMES,TYPE_BLURBS,score_quiz,riasec_code
from ..schemas import ProfilePayload
from ..storage import get_profile,save_profile,list_profiles,delete_profile
router=APIRouter(prefix='/api',tags=['profiles'])

def build_payload(pid,value:ProfilePayload,created_at=None):
    for sid,level in value.skills.items():
        if sid not in SKILL_INDEX or level<0 or level>5:raise HTTPException(400,f'Invalid skill/level: {sid}')
    if value.user_type not in ('student','professional'):raise HTTPException(400,'Invalid user type')
    if value.quiz_answers and any(q not in {x[0] for x in QUESTIONS} or not 1<=a<=5 for q,a in value.quiz_answers.items()):
        raise HTTPException(400,'Invalid quiz answer')
    now=datetime.now(timezone.utc).isoformat(timespec='seconds')
    payload={'id':pid,**value.model_dump(),'created_at':created_at or now,'updated_at':now}
    # The interest profile is computed here from the answers, never accepted from the client.
    payload['riasec']=score_quiz(value.quiz_answers) if value.quiz_answers else None
    payload['riasec_code']=riasec_code(payload['riasec']) if payload['riasec'] else None
    return payload

@router.get('/profile')
def profile():return get_profile()

@router.put('/profile')
def update_profile(value:ProfilePayload):
    payload=build_payload('demo',value,get_profile().get('created_at'))
    save_profile('demo',payload)
    return payload

@router.get('/profiles')
def profiles():
    return [{'id':p['id'],'name':p['name'],'headline':p.get('headline',''),'skills':len(p.get('skills',{})),
             'has_quiz':bool(p.get('riasec')),'updated_at':p.get('updated_at','')} for p in list_profiles()]

@router.post('/profiles',status_code=201)
def create_profile(value:ProfilePayload):
    pid=secrets.token_urlsafe(6)
    payload=build_payload(pid,value)
    save_profile(pid,payload)
    return payload

@router.get('/profiles/{pid}')
def saved_profile(pid:str):return get_profile(pid)

@router.put('/profiles/{pid}')
def update_saved_profile(pid:str,value:ProfilePayload):
    payload=build_payload(pid,value,get_profile(pid).get('created_at'))  # 404 if the person doesn't exist
    save_profile(pid,payload)
    return payload

@router.delete('/profiles/{pid}',status_code=204)
def remove_saved_profile(pid:str):
    delete_profile(pid)

@router.get('/interest-quiz')
def interest_quiz():
    return {'questions':[{'id':i,'type':t,'text':text} for i,t,text in QUESTIONS],'likert':[{'value':v,'label':l} for v,l in LIKERT],
            'types':[{'type':t,'name':TYPE_NAMES[t],'blurb':TYPE_BLURBS[t]} for t in TYPES]}
=======
"""Saved people. Each person who goes through Start gets their own profile id.

/api/profile is the original shared 'demo' profile (kept for compatibility); /api/profiles/{id} are saved people.
There are no user accounts: everyone using this server can see the list, so use fictional CVs.
"""
import secrets
from datetime import datetime,timezone
from fastapi import APIRouter,HTTPException
from ..catalog import SKILL_INDEX
from ..interests import QUESTIONS,LIKERT,TYPES,TYPE_NAMES,TYPE_BLURBS,score_quiz,riasec_code
from ..schemas import ProfilePayload
from ..storage import get_profile,save_profile,list_profiles,delete_profile
router=APIRouter(prefix='/api',tags=['profiles'])

def build_payload(pid,value:ProfilePayload,created_at=None):
    for sid,level in value.skills.items():
        if sid not in SKILL_INDEX or level<0 or level>5:raise HTTPException(400,f'Invalid skill/level: {sid}')
    if value.user_type not in ('student','professional'):raise HTTPException(400,'Invalid user type')
    if value.quiz_answers and any(q not in {x[0] for x in QUESTIONS} or not 1<=a<=5 for q,a in value.quiz_answers.items()):
        raise HTTPException(400,'Invalid quiz answer')
    now=datetime.now(timezone.utc).isoformat(timespec='seconds')
    payload={'id':pid,**value.model_dump(),'created_at':created_at or now,'updated_at':now}
    # The interest profile is computed here from the answers, never accepted from the client.
    payload['riasec']=score_quiz(value.quiz_answers) if value.quiz_answers else None
    payload['riasec_code']=riasec_code(payload['riasec']) if payload['riasec'] else None
    return payload

@router.get('/profile')
def profile():return get_profile()

@router.put('/profile')
def update_profile(value:ProfilePayload):
    payload=build_payload('demo',value,get_profile().get('created_at'))
    save_profile('demo',payload)
    return payload

@router.get('/profiles')
def profiles():
    return [{'id':p['id'],'name':p['name'],'headline':p.get('headline',''),'skills':len(p.get('skills',{})),
             'has_quiz':bool(p.get('riasec')),'updated_at':p.get('updated_at','')} for p in list_profiles()]

@router.post('/profiles',status_code=201)
def create_profile(value:ProfilePayload):
    pid=secrets.token_urlsafe(6)
    payload=build_payload(pid,value)
    save_profile(pid,payload)
    return payload

@router.get('/profiles/{pid}')
def saved_profile(pid:str):return get_profile(pid)

@router.put('/profiles/{pid}')
def update_saved_profile(pid:str,value:ProfilePayload):
    payload=build_payload(pid,value,get_profile(pid).get('created_at'))  # 404 if the person doesn't exist
    save_profile(pid,payload)
    return payload

@router.delete('/profiles/{pid}',status_code=204)
def remove_saved_profile(pid:str):
    delete_profile(pid)

@router.get('/interest-quiz')
def interest_quiz():
    return {'questions':[{'id':i,'type':t,'text':text} for i,t,text in QUESTIONS],'likert':[{'value':v,'label':l} for v,l in LIKERT],
            'types':[{'type':t,'name':TYPE_NAMES[t],'blurb':TYPE_BLURBS[t]} for t in TYPES]}
>>>>>>> da0787dab49148d066631b796b12e2b882c85231
