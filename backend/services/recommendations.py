"""Facade for scoring: the formula itself remains in backend/engine.py."""
from fastapi import HTTPException
from ..engine import recommend
from ..catalog import ROLES, SKILL_INDEX, RESOURCES
from ..storage import get_profile,get_snapshot,get_signals
from ..signals.demand import demand_map

def result(profile=None,snapshot=None,scenario='moderate',role_id=None,signals=None,profile_id=None):
    """Trends come from stored trend signals (curated + refreshed feeds). Pass `signals` to score against a subset,
    and `profile_id` to score a saved person instead of the shared demo profile."""
    if scenario not in ('moderate','rapid'):raise HTTPException(400,'Invalid scenario')
    if role_id and not any(r['id']==role_id for r in ROLES):raise HTTPException(404,'Career not found')
    names={k:v['name'] for k,v in SKILL_INDEX.items()}
    demand=demand_map(ROLES,get_signals() if signals is None else signals,skill_names=names)
    return recommend(ROLES,profile or get_profile(profile_id or 'demo'),snapshot or get_snapshot(),SKILL_INDEX,RESOURCES,scenario,role_id,demand)
