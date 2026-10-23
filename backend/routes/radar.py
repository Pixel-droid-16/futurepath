"""Skills Radar reading the currently approved evidence snapshot."""
from fastapi import APIRouter
from ..storage import get_snapshot
router=APIRouter(prefix='/api',tags=['radar'])
@router.get('/radar')
def radar():return {'snapshot':get_snapshot(),'warning':'SYNTHETIC DEMO DATA — not real workforce evidence'}
