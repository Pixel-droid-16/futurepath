"""Published and staged evidence snapshot metadata."""
import json
from fastapi import APIRouter
from ..storage import connection
router=APIRouter(prefix='/api',tags=['snapshots'])
@router.get('/snapshots')
def snapshots():
    with connection() as c:
        return [dict(json.loads(x['payload']),status=x['status']) for x in c.execute('SELECT * FROM snapshots ORDER BY id').fetchall()]
