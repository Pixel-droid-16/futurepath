"""Facade for scoring: the formula itself remains in backend/engine.py."""
from fastapi import HTTPException
from ..engine import recommend
from ..catalog import ROLES, SKILL_INDEX, RESOURCES
from ..storage import get_profile,get_snapshot

def result(profile=None,snapshot=None,scenario='moderate',role_id=None):
    if scenario not in ('moderate','rapid'):raise HTTPException(400,'Invalid scenario')
    if role_id and not any(r['id']==role_id for r in ROLES):raise HTTPException(404,'Career not found')
    return recommend(ROLES,profile or get_profile(),snapshot or get_snapshot(),SKILL_INDEX,RESOURCES,scenario,role_id)
