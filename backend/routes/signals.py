"""Trend signals: list, refresh from feeds (admin), refresh audit trail and "What changed"."""
import json,os,secrets
from datetime import date
from fastapi import APIRouter,HTTPException,Request
from pydantic import BaseModel,Field
from ..catalog import ROLES,SKILL_INDEX,load
from ..demo_security import public_demo
from ..signals.demand import recency_decay
from ..storage import connection,get_signals
from ..services.recommendations import result
from ..signals.refresh import refresh_signals,RefreshInProgress,automatic_ai_allowed
from ..signals.schedule import interval_hours,last_runs,next_due
from ..signals.review import review_items,decide
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

DECLINING_JOBS=load('declining_jobs.json')

TREND_MONTHS=36  # the sparkline window

def months_back(today,n):
    """First day of each of the last n months, oldest first (YYYY-MM-01)."""
    y,m=today.year,today.month;out=[]
    for _ in range(n):
        out.append(f'{y:04d}-{m:02d}-01');m-=1
        if not m:y,m=y-1,12
    return out[::-1]

def card(title,found,today,months,kind,extra=None,lead=None):
    """One trend card: signal count, net weight (strength x recency), the source to show (lead, else the newest),
    and a monthly cumulative line."""
    sign=lambda g:1 if g['direction']=='emerging' else -1
    newest=lead or max(found,key=lambda g:g['published_date'])
    line=[sum(sign(g)*g['strength'] for g in found if g['published_date']<(months[i+1] if i+1<len(months) else '9999')) for i in range(len(months))]
    return {'title':title,'kind':kind,'signal_count':len(found),
            'net':round(sum(sign(g)*g['strength']*recency_decay(g['published_date'],today) for g in found),2),
            'latest':{'title':newest['title'],'source':newest['source_name'],'date':newest['published_date'],'url':newest['url']},
            'line':line,**(extra or {})}

@router.get('/skill-trends')
def skill_trends():
    """Signals page cards. Rising: catalogue skills whose signals are net rising. Declining: skills whose signals are net
    falling, plus jobs that dated reports name as declining (data/declining_jobs.json; they are not catalogue careers).
    Every number comes from stored, dated signals; the line is the cumulative signed strength per month."""
    signals=get_signals();today=date.today();months=months_back(today,TREND_MONTHS)
    by_skill={}
    for g in signals:
        for k in g['skill_ids']:by_skill.setdefault(k,[]).append(g)
    skills=[card(SKILL_INDEX[k]['name'],found,today,months,'skill',{'skill_id':k,'category':SKILL_INDEX[k]['category'],
                 'sdgs':SKILL_INDEX[k].get('sdgs',[])}) for k,found in by_skill.items() if k in SKILL_INDEX]
    by_id={g['external_id']:g for g in signals}
    jobs=[]
    for job in DECLINING_JOBS:
        found=[by_id[i] for i in job['signal_ids'] if i in by_id and by_id[i]['direction']=='declining']
        # Lead with the report that names this job specifically (listed first in declining_jobs.json).
        if found:jobs.append(card(job['title'],found,today,months,'job',{'id':job['id'],'category':'job','sdgs':[]},lead=found[0]))
    rising=sorted((c for c in skills if c['net']>0),key=lambda c:(-c['net'],c['title']))
    declining=sorted([c for c in skills if c['net']<0]+jobs,key=lambda c:(c['net'],c['title']))
    return {'rising':rising,'declining':declining,'months':months,'as_of':today.isoformat()}

def run_row(r):return {**dict(r),'feeds':json.loads(r['feeds'] or '[]')}

@router.get('/signals/runs')
def runs(limit:int=5):
    with connection() as c:
        return [run_row(r) for r in c.execute('SELECT * FROM refresh_runs ORDER BY id DESC LIMIT ?',(max(1,min(limit,50)),))]

def refresh_mode(request:Request):
    """Report available refresh controls; the POST still checks authorization."""
    if public_demo():
        return 'demo'
    if os.getenv('ADMIN_TOKEN'):
        return 'admin'
    return 'local' if (request.client.host if request.client else '') in LOCAL_HOSTS else 'local_only'

@router.get('/signals/refresh-access')
def refresh_access(request:Request):
    """Read-only refresh policy for the UI; never return secret values."""
    mode=refresh_mode(request)
    messages={
        'demo': 'Live-feed refresh is disabled in this public synthetic-data demo. Existing stored signals remain available.',
        'admin': 'Live-feed refresh is administrator-only. Enter ADMIN_TOKEN only when prompted; it is not saved in the browser.',
        'local': 'Live-feed refresh is available in local development.',
        'local_only': 'Hosted live-feed refresh requires an ADMIN_TOKEN Replit Secret and a server restart. Existing curated signals remain available.',
    }
    return {'mode':mode,'can_refresh':mode in ('admin','local'),
            'requires_token':mode=='admin','message':messages[mode]}

def authorise_review(request:Request):
    """Review has no localhost exemption, and is forbidden in public demos."""
    if public_demo():
        raise HTTPException(403,'Evidence review is disabled in public demo mode')
    token=os.getenv('ADMIN_TOKEN')
    if not token:
        raise HTTPException(503,'Administrator review is not configured')
    scheme,_,supplied=request.headers.get('authorization','').partition(' ')
    if scheme.lower()!='bearer' or not secrets.compare_digest(supplied,token):
        raise HTTPException(401,'Administrator bearer authorization required')

@router.get('/signals/status')
def signal_status():
    """Public metadata only: no fetch, review authorization, or scheduler mutation."""
    with connection() as c:
        row=c.execute('SELECT * FROM refresh_runs ORDER BY id DESC LIMIT 1').fetchone()
        pending=c.execute("SELECT COUNT(*) FROM signal_review WHERE status='pending'").fetchone()[0]
        approved=c.execute("SELECT MAX(reviewed_at) FROM signal_review WHERE status='approved'").fetchone()[0]
        success=c.execute("SELECT finished_at FROM refresh_runs WHERE status IN ('ok','partial') AND finished_at IS NOT NULL ORDER BY id DESC LIMIT 1").fetchone()
    due=next_due()
    return {'enabled':bool(interval_hours()),'interval_hours':interval_hours(),
            'next_due':due.isoformat() if due else None,
            'last_checked':(row['finished_at'] or row['started_at']) if row else None,
            'last_successful_at':success[0] if success else None,
            'status':row['status'] if row else 'not_checked','pending_count':pending,
            'last_approved_at':approved,'automatic_tagger':'claude' if automatic_ai_allowed() else 'keywords',
            'automatic_ai_enabled':automatic_ai_allowed(),
            'public_demo':public_demo(),'best_effort':True}

@router.get('/signals/review')
def list_review(request:Request,status:str='pending',limit:int=200):
    authorise_review(request)
    return review_items(status,limit)

class ReviewDecision(BaseModel):
    reason:str=Field(default='',max_length=500)

@router.post('/signals/review/{review_id}/approve')
def approve_review(review_id:int,request:Request,payload:ReviewDecision|None=None):
    authorise_review(request)
    return decide(review_id,'approved',(payload.reason if payload else '').strip())

@router.post('/signals/review/{review_id}/reject')
def reject_review(review_id:int,request:Request,payload:ReviewDecision|None=None):
    authorise_review(request)
    return decide(review_id,'rejected',(payload.reason if payload else '').strip())

def authorise(request:Request):
    """In public demo mode refresh is disabled; otherwise require admin token or local host."""
    if public_demo():
        raise HTTPException(403,'Manual signal refresh is disabled in public demo mode')
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
        approval=c.execute("SELECT run_id FROM signal_review WHERE status='approved' ORDER BY reviewed_at DESC,id DESC LIMIT 1").fetchone()
        run=(c.execute('SELECT * FROM refresh_runs WHERE id=?',(approval[0],)).fetchone() if approval else
             c.execute("SELECT * FROM refresh_runs WHERE accepted>0 AND status!='running' ORDER BY id DESC LIMIT 1").fetchone())
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
