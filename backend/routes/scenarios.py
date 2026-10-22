"""Moderate AI vs Rapid AI side-by-side. Assumptions in backend/scenarios.py."""
from fastapi import APIRouter
from ..services.recommendations import result
router=APIRouter(prefix='/api',tags=['scenarios'])
@router.get('/scenarios/{role_id}')
def scenario_comparison(role_id:str,profile:str|None=None):
    return {'moderate':result(scenario='moderate',role_id=role_id,profile_id=profile)[0],
            'rapid':result(scenario='rapid',role_id=role_id,profile_id=profile)[0],
            'notice':'Synthetic hypothetical scenarios; not labour-market predictions.'}
