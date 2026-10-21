"""Versioned recommendation save, preview and deletion."""
import json
from datetime import datetime,timezone
from fastapi import APIRouter,HTTPException
from ..schemas import SavePayload,ComparePayload
from ..storage import connection,get_profile,get_snapshot
from ..services.recommendations import result
router=APIRouter(prefix='/api',tags=['history'])
@router.get('/history')
def history():
    with connection() as c:
        return [dict(id=r['id'],created_at=r['created_at'],**json.loads(r['payload'])) for r in c.execute('SELECT * FROM history WHERE profile_id=? ORDER BY id DESC',('demo',)).fetchall()]
@router.post('/history')
def save(payload:SavePayload):
    snap=get_snapshot(payload.snapshot_id)
    if snap['status']!='published':raise HTTPException(400,'Only approved/published snapshot can be saved')
    profile=get_profile()
    rec=result(profile,snap,payload.scenario,payload.role_id)[0]
    envelope={'role_id':payload.role_id,'snapshot_id':snap['id'],'scenario':payload.scenario,'profile':profile,'matching_version':'mvp-rule-v1','taxonomy_version':'skills-demo-v1','result':rec}
    with connection() as c:
        cur=c.execute('INSERT INTO history(profile_id,created_at,payload) VALUES(?,?,?)',('demo',datetime.now(timezone.utc).isoformat(),json.dumps(envelope)))
        record_id=cur.lastrowid
    return {'id':record_id,**envelope}
@router.delete('/history/{history_id}')
def delete_history(history_id:int):
    with connection() as c:
        cur=c.execute('DELETE FROM history WHERE id=? AND profile_id=?',(history_id,'demo'))
    if not cur.rowcount:raise HTTPException(404,'Version not found')
    return {'deleted':history_id}
@router.post('/compare')
def compare(payload:ComparePayload):
    with connection() as c:
        r=c.execute('SELECT * FROM history WHERE id=? AND profile_id=?',(payload.history_id,'demo')).fetchone()
    if not r:raise HTTPException(404,'Saved version not found')
    old=json.loads(r['payload'])
    new=result(old['profile'],get_snapshot(),old['scenario'],old['role_id'])[0]
    prior=old['result']
    return {'old':prior,'new':new,'change':round(new['suitability']-prior['suitability'],1),
            'old_snapshot':old['snapshot_id'],'new_snapshot':new['snapshot_id'],
            'profile_unchanged':True,'scoring_model_unchanged':True,
            'is_material':abs(new['suitability']-prior['suitability'])>=5}
