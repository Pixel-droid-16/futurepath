"""Danger: demo curator approval is unauthenticated. DO NOT publicly deploy."""
import json
from fastapi import APIRouter,HTTPException
from ..demo_security import public_demo
from ..storage import connection
router=APIRouter(prefix='/api',tags=['curator-demo'])
@router.post('/curator/approve/{sid}')
def approve(sid:str):
    if public_demo():
        raise HTTPException(403,'Curator approval is disabled in public demo mode')
    with connection() as c:
        row=c.execute('SELECT * FROM snapshots WHERE id=?',(sid,)).fetchone()
        if not row:raise HTTPException(404,'Unknown snapshot')
        s=json.loads(row['payload'])
        if not s['source'].startswith('SYNTHETIC ONLY'):raise HTTPException(400,'This demo only approves synthetic snapshots')
        c.execute("UPDATE snapshots SET status='superseded' WHERE status='published'")
        c.execute("UPDATE snapshots SET status='published' WHERE id=?",(sid,))
    return {'approved':sid,'warning':'Demo curator endpoint is unauthenticated. Add role-based authentication in production.'}
