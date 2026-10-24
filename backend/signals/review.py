"""Read-only access to historical review records; manual publication is retired."""
import json
from fastapi import HTTPException
from ..storage import connection
from ..demo_security import public_demo


def review_items(status='pending',limit=200):
    if status not in ('pending','approved','rejected','all'):
        raise HTTPException(400,'Unknown review status')
    clause,args=('',()) if status=='all' else (' WHERE status=?',(status,))
    with connection() as c:
        total=c.execute('SELECT COUNT(*) FROM signal_review'+clause,args).fetchone()[0]
        rows=c.execute('SELECT * FROM signal_review'+clause+' ORDER BY id DESC LIMIT ?',
                       (*args,max(1,min(limit,200)))).fetchall()
    return {'total':total,'items':[
        {**{k:r[k] for k in ('id','status','created_at','reviewed_at','decision_reason','signal_id')},
         'signal':json.loads(r['signal']),'validation_notes':r['validation_notes']}
        for r in rows]}


def decide(review_id,action,reason=''):
    if public_demo():
        raise HTTPException(403,'Evidence mutations are disabled in public demo mode')
    raise HTTPException(410,'Manual evidence approval is retired; only AI-validated ingestion may publish')
