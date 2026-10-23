<<<<<<< HEAD
"""Deterministic ranked career matching. Formula in backend/engine.py."""
from fastapi import APIRouter
from ..services.recommendations import result
router=APIRouter(prefix='/api',tags=['matches'])
@router.get('/matches')
def matches(scenario:str='moderate',role_id:str|None=None,profile:str|None=None):
    return result(scenario=scenario,role_id=role_id,profile_id=profile)
=======
"""Deterministic ranked career matching. Formula in backend/engine.py."""
from fastapi import APIRouter
from ..services.recommendations import result
router=APIRouter(prefix='/api',tags=['matches'])
@router.get('/matches')
def matches(scenario:str='moderate',role_id:str|None=None,profile:str|None=None):
    return result(scenario=scenario,role_id=role_id,profile_id=profile)
>>>>>>> da0787dab49148d066631b796b12e2b882c85231
