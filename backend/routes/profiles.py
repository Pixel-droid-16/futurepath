"""One shared demo profile: replace with per-user storage before deployment."""
import json
from fastapi import APIRouter,HTTPException
from ..catalog import SKILL_INDEX
from ..schemas import ProfilePayload
from ..storage import connection,get_profile
router=APIRouter(prefix='/api',tags=['profiles'])
@router.get('/profile')
def profile():return get_profile()
@router.put('/profile')
def update_profile(value:ProfilePayload):
    for sid,level in value.skills.items():
        if sid not in SKILL_INDEX or level<0 or level>5:raise HTTPException(400,f'Invalid skill/level: {sid}')
    if value.user_type not in ('student','professional'):raise HTTPException(400,'Invalid user type')
    payload={'id':'demo',**value.model_dump()}
    with connection() as c:c.execute('UPDATE profiles SET payload=? WHERE id=?',(json.dumps(payload),'demo'))
    return payload
