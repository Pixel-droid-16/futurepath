"""Trend signals: list, refresh from feeds (admin), refresh audit trail and "What changed"."""
import json,os,secrets
from datetime import date
from fastapi import APIRouter,HTTPException,Request
from ..catalog import ROLES,SKILL_INDEX
from ..signals.demand import recency_decay
from ..storage import connection,get_signals
from ..services.recommendations import result
from ..signals.refresh import refresh_signals,RefreshInProgress
from ..signals.schedule import interval_hours,last_runs,next_due
router=APIRouter(prefix='/api',tags=['signals'])
LOCAL_HOSTS={'127.0.0.1','::1','localhost','testclient'}
ROLE_TITLES={r['id']:r['title'] for r in ROLES}

@router.get('/signals')
def signals(direction:str|None=None,limit:int=200):
    rows=[s for s in get_signals() if direction in (None,s['direction'])][:max(1,min(limit,500))]
    for s in rows:s['role_titles']=[ROLE_TITLES[r] for r in s['role_ids'] if r in ROLE_TITLES]
    return rows

@router.get('/skill-outlook')
def skill_outlook():
    """Net outlook per skill from the signals that name it (+/-strength x recency decay): Home's rising/fading radar."""
    today=date.today();net={}
    for s in get_signals():
        v=(1 if s['direction']=='emerging' else -1)*s['strength']*recency_decay(s['published_date'],today)
        for k in s['skill_ids']:net[k]=net.get(k,0)+v
    top=max((abs(v) for v in net.values()),default=1) or 1
    row=lambda k,v:{'skill_id':k,'name':SKILL_INDEX[k]['name'],'value':round(v,2),'width':round(100*abs(v)/top)}
    updated,_=last_runs();due=next_due()
    return {'rising':[row(k,v) for k,v in sorted(net.items(),key=lambda x:-x[1]) if v>0][:5],
            'declining':[row(k,v) for k,v in sorted(net.items(),key=lambda x:x[1]) if v<0][:4],
            # When feeds were last pulled (None before the first refresh: curated reports only), and the automatic schedule.
            'updated_at':updated.isoformat() if updated else None,'auto_refresh_hours':interval_hours(),
            'next_refresh_at':due.isoformat(timespec='seconds') if due else None}

def run_row(r):return {**dict(r),'feeds':json.loads(r['feeds'] or '[]')}

@router.get('/signals/runs')
def runs(limit:int=5):
    with connection() as c:
        return [run_row(r) for r in c.execute('SELECT * FROM refresh_runs ORDER BY id DESC LIMIT ?',(max(1,min(limit,50)),))]

def authorise(request:Request):
    """With ADMIN_TOKEN set, a matching bearer token is required. Without it, only this computer may refresh."""
    token=os.getenv('ADMIN_TOKEN')
    if token:
        given=request.headers.get('authorization','').removeprefix('Bearer ').strip()
        if not secrets.compare_digest(given,token):raise HTTPException(401,'Admin token required to refresh signals')
    elif (request.client.host if request.client else '') not in LOCAL_HOSTS:
        raise HTTPException(403,'Set ADMIN_TOKEN to allow refreshing signals from other machines')

@router.post('/signals/refresh')
async def refresh(request:Request):
    authorise(request)
    try:return await refresh_signals()
    except RefreshInProgress as e:raise HTTPException(409,str(e))

@router.get('/what-changed')
def what_changed(profile:str|None=None):
    """How the latest refresh moved the current profile's ranking: score with and without that run's new signals."""
    with connection() as c:
        run=c.execute("SELECT * FROM refresh_runs WHERE accepted>0 AND status!='running' ORDER BY id DESC LIMIT 1").fetchone()
        last=c.execute("SELECT * FROM refresh_runs WHERE status!='running' ORDER BY id DESC LIMIT 1").fetchone()
    if not run:return {'has_change':False,'last_refresh':run_row(last) if last else None}
    every=get_signals();new=[s for s in every if s['run_id']==run['id']]
    before={r['role_id']:(i+1,r) for i,r in enumerate(result(signals=[s for s in every if s['run_id']!=run['id']],profile_id=profile))}
    after={r['role_id']:(i+1,r) for i,r in enumerate(result(signals=every,profile_id=profile))}
    moves=[]
    for rid,(rank,rec) in after.items():
        old_rank,old=before[rid]
        linked=[s for s in new if rid in s['role_ids'] or set(s['skill_ids'])&{g['skill_id'] for g in rec['gaps']}]
        if rank!=old_rank or rec['components']['trends']!=old['components']['trends']:
            moves.append({'role_id':rid,'title':rec['title'],'before_rank':old_rank,'after_rank':rank,
                          'before_trend':old['components']['trends'],'after_trend':rec['components']['trends'],'new_signals':len(linked)})
    moves.sort(key=lambda m:(-abs(m['before_rank']-m['after_rank']),-abs(m['after_trend']-m['before_trend'])))
    return {'has_change':True,'run':run_row(run),'new_signal_count':len(new),'new_signals':[{'title':s['title'],'source':s['source_name'],
            'date':s['published_date'],'direction':s['direction'],'url':s['url']} for s in new[:5]],'moves':moves,'last_refresh':run_row(last)}
