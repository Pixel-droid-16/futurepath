"""Refresh pipeline: fetch feeds, drop seen items and near-duplicates, tag, apply guardrails, store, audit."""
import asyncio,json,re
from datetime import datetime,timedelta,timezone
import httpx
from ..catalog import ROLES,SKILLS
from ..storage import connection
from ..demo_security import public_demo
from .feeds import FEEDS
from .fetch import fetch_feed
from .guardrails import apply_guardrails,source_error
from .tagging import default_tagger,KeywordTagger

MAX_NEW_ITEMS_PER_RUN=40
STALE_RUN_MINUTES=15
STOPWORDS={'the','and','for','with','from','says','said','its','into','over','will','has','have','are','was'}

class RefreshInProgress(Exception):
    def __init__(self):super().__init__('A signal refresh is already running. Try again in a few minutes.')

def now():return datetime.now(timezone.utc).isoformat(timespec='seconds')

def title_tokens(title):
    return {w for w in re.sub(r'[^a-z0-9\s]',' ',title.lower()).split() if len(w)>2 and w not in STOPWORDS}

def near_duplicate(a,b):
    """The same story often arrives from several outlets with reworded headlines."""
    smaller=min(len(a),len(b))
    return smaller>=4 and len(a&b)/smaller>=0.6

def record_item(c,it,run_id,status,reason,signal_id=None):
    c.execute('''INSERT INTO feed_items(external_id,feed_key,title,url,published_date,run_id,status,reason,signal_id,seen_at) VALUES(?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(external_id) DO UPDATE SET run_id=excluded.run_id,status=excluded.status,reason=excluded.reason,signal_id=excluded.signal_id,seen_at=excluded.seen_at''',
        (it['external_id'],it['feed_key'],it['title'],it['url'],it['published_date'],run_id,status,reason[:500],signal_id,now()))

async def refresh_signals(feeds=None,tagger=None,client=None,automatic=False):
    """Validate and stage evidence. Only a separate authenticated approval makes it active."""
    if public_demo():
        raise RuntimeError('External refresh is disabled in public demo mode')
    feeds=FEEDS if feeds is None else feeds
    tagger=KeywordTagger() if automatic else (tagger or default_tagger())
    with connection() as c:
        c.execute('BEGIN IMMEDIATE')
        cutoff=(datetime.now(timezone.utc)-timedelta(minutes=STALE_RUN_MINUTES)).isoformat(timespec='seconds')
        if c.execute("SELECT 1 FROM refresh_runs WHERE status='running' AND started_at>?",(cutoff,)).fetchone():raise RefreshInProgress()
        run_id=c.execute("INSERT INTO refresh_runs(started_at,status,tagger,model,trigger) VALUES(?,?,?,?,?)",(now(),'running',tagger.name,tagger.model,'automatic' if automatic else 'manual')).lastrowid
    try:
        own=client is None
        client=client or httpx.AsyncClient()
        try:settled=await asyncio.gather(*(fetch_feed(client,f) for f in feeds),return_exceptions=True)
        finally:
            if own:await client.aclose()
        feed_results=[{'key':f['key'],'name':f['name'],'ok':not isinstance(r,BaseException),'items':0 if isinstance(r,BaseException) else len(r),
                       **({'error':str(r)[:300]} if isinstance(r,BaseException) else {})} for f,r in zip(feeds,settled)]
        fetched=list({i['external_id']:i for r in settled if not isinstance(r,BaseException) for i in r}.values())

        with connection() as c:
            ids=[i['external_id'] for i in fetched]
            marks=','.join('?'*len(ids)) or "''"
            seen={r[0] for r in c.execute(f"SELECT external_id FROM feed_items WHERE status IN ('accepted','approved','pending','rejected') AND external_id IN ({marks})",ids)}
            seen|={r[0] for r in c.execute(f'SELECT external_id FROM signals WHERE external_id IN ({marks})',ids)}
            since=(datetime.now(timezone.utc)-timedelta(days=90)).date().isoformat()
            known=[(t,title_tokens(t)) for (t,) in c.execute('SELECT title FROM signals WHERE published_date>=?',(since,))]
            known += [(json.loads(r[0])['title'],title_tokens(json.loads(r[0])['title']))
                      for r in c.execute('SELECT signal FROM signal_review')]
        candidates=sorted((i for i in fetched if i['external_id'] not in seen),key=lambda i:i['published_date'],reverse=True)
        fresh,duplicates,invalid=[],[],[]
        feed_map={f['key']:f for f in feeds}
        for it in candidates:
            error=source_error(it,feed_map.get(it['feed_key']))
            if it['feed_key'] not in feed_map:error='Unconfigured feed source'
            if error:invalid.append((it,error));continue
            tokens=title_tokens(it['title'])
            # Dataset releases are keyed by their release folder; their titles differ only by date.
            match=None if it['source_type']=='dataset' else next((t for t,k in known if near_duplicate(tokens,k)),None)
            if match:duplicates.append((it,match))
            elif len(fresh)<MAX_NEW_ITEMS_PER_RUN:fresh.append(it);known.append((it['title'],tokens))

        catalog={'roles':ROLES,'skills':SKILLS}
        outcomes=await tagger.tag(fresh,catalog) if fresh else []
        role_ids={r['id'] for r in ROLES};skill_ids={s['id'] for s in SKILLS}
        pending=rejected=failed=0
        with connection() as c:
            for it,reason in invalid+[(it,f'near-duplicate of "{of}"') for it,of in duplicates]:
                rejected+=1;record_item(c,it,run_id,'rejected',reason)
            for it,outcome in zip(fresh,outcomes+[{'ok':False,'error':'no tagger result'}]*(len(fresh)-len(outcomes))):
                if not outcome['ok']:failed+=1;record_item(c,it,run_id,'failed',outcome['error']);continue
                proposal,notes=apply_guardrails(it,outcome['proposal'],role_ids,skill_ids)
                if proposal is None:rejected+=1;record_item(c,it,run_id,'rejected',notes);continue
                signal={'external_id':it['external_id'],'title':it['title'],'source_name':it['source_name'],'source_type':it['source_type'],
                    'url':it['url'],'published_date':it['published_date'],'fetched_at':now()[:10],'summary':proposal['summary'],'direction':proposal['direction'],
                    'strength':proposal['strength'],'role_ids':proposal['role_ids'],'skill_ids':proposal['skill_ids'],'tagged_by':tagger.name,
                    'feed_key':it['feed_key'],'run_id':run_id}
                reason='; '.join([outcome['proposal'].get('reason','')]+notes).strip('; ')
                review_id=c.execute('INSERT INTO signal_review(external_id,run_id,status,signal,source_item,validation_notes,created_at) VALUES(?,?,?,?,?,?,?)',
                                    (it['external_id'],run_id,'pending',json.dumps(signal),json.dumps(it),reason,now())).lastrowid
                c.execute('INSERT INTO signal_review_events(review_id,action,created_at,actor,reason) VALUES(?,?,?,?,?)',
                          (review_id,'staged',now(),'automatic-keywords' if automatic else 'manual-refresh',reason))
                pending+=1
                record_item(c,it,run_id,'pending',reason)
            any_ok=any(f['ok'] for f in feed_results)
            status='failed' if not any_ok else ('ok' if all(f['ok'] for f in feed_results) and failed==0 else 'partial')
            c.execute('UPDATE refresh_runs SET finished_at=?,status=?,feeds=?,checked=?,pending=?,rejected=?,failed=? WHERE id=?',
                      (now(),status,json.dumps(feed_results),len(fresh)+len(duplicates)+len(invalid),pending,rejected,failed,run_id))
        return {'run_id':run_id,'status':status,'tagger':tagger.name,'model':tagger.model,'feeds':feed_results,
                'checked':len(fresh)+len(duplicates)+len(invalid),'accepted':0,'pending':pending,'rejected':rejected,'failed':failed,'new_signals':[]}
    except Exception as err:
        with connection() as c:
            c.execute("UPDATE refresh_runs SET finished_at=?,status='failed',error=? WHERE id=?",(now(),str(err)[:500],run_id))
        raise
    finally:
        # Avoid a circular import at module load; schedule is persisted in the same DB.
        from .schedule import record_check
        record_check()
