"""Automatic evidence publication: prefilter, quota-bound AI, strict validation, audit."""
import asyncio
import json
import re
from datetime import datetime, timedelta, timezone

import httpx

from ..catalog import ROLES, SKILLS
from ..storage import connection, insert_signal
from ..demo_security import public_demo
from ..providers.claude import configured
from .feeds import FEEDS
from .fetch import fetch_feed
from . import verification as ai

MAX_NEW_ITEMS_PER_RUN = 40
STALE_RUN_MINUTES = 15
STOPWORDS = {'the','and','for','with','from','says','said','its','into','over','will','has','have','are','was'}


class RefreshInProgress(Exception):
    def __init__(self):
        super().__init__('A signal refresh is already running. Try again later.')


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def title_tokens(title):
    return {w for w in re.sub(r'[^a-z0-9\s]',' ',title.lower()).split()
            if len(w)>2 and w not in STOPWORDS}


def near_duplicate(a,b):
    smaller = min(len(a),len(b))
    return smaller>=4 and len(a&b)/smaller>=0.6


def record_item(c,it,run_id,status,reason,signal_id=None):
    c.execute('''INSERT INTO feed_items(external_id,feed_key,title,url,published_date,run_id,status,reason,signal_id,seen_at)
        VALUES(?,?,?,?,?,?,?,?,?,?) ON CONFLICT(external_id) DO UPDATE SET run_id=excluded.run_id,
        status=excluded.status,reason=excluded.reason,signal_id=excluded.signal_id,seen_at=excluded.seen_at''',
        (it['external_id'],it['feed_key'],it['title'],it.get('url',''),it.get('published_date',''),
         run_id,status,reason[:500],signal_id,now()))


def quarantine(c,it,run_id,status,reason,signal_id=None):
    stamp = now()
    c.execute('''INSERT INTO signal_candidates(external_id,content_hash,run_id,status,source_item,reason,
        created_at,checked_at,signal_id,verified_by) VALUES(?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(external_id) DO UPDATE SET content_hash=excluded.content_hash,run_id=excluded.run_id,
        status=excluded.status,source_item=excluded.source_item,reason=excluded.reason,
        checked_at=excluded.checked_at,signal_id=excluded.signal_id,verified_by=excluded.verified_by''',
        (it['external_id'],ai.fingerprint(it),run_id,status,json.dumps(it),reason[:500],stamp,stamp,
         signal_id,'claude-verified' if status=='published' else None))
    c.execute('INSERT INTO signal_ingestion_audit(external_id,run_id,status,reason,created_at) VALUES(?,?,?,?,?)',
              (it['external_id'],run_id,status,reason[:500],stamp))
    record_item(c,it,run_id,status,reason,signal_id)


async def refresh_signals(feeds=None,tagger=None,client=None,automatic=False):
    """No human approval and no keyword-only publication, including manual refreshes.

    The legacy tagger argument cannot bypass AI verification or opt-in settings.
    """
    if public_demo():
        raise RuntimeError('External refresh is disabled in public demo mode')
    feeds = FEEDS if feeds is None else feeds
    catalog = {'roles':ROLES,'skills':SKILLS}
    with connection() as c:
        c.execute('BEGIN IMMEDIATE')
        cutoff = (datetime.now(timezone.utc)-timedelta(minutes=STALE_RUN_MINUTES)).isoformat()
        if c.execute("SELECT 1 FROM refresh_runs WHERE status='running' AND started_at>?",(cutoff,)).fetchone():
            raise RefreshInProgress()
        run_id = c.execute("INSERT INTO refresh_runs(started_at,status,tagger,trigger) VALUES(?,'running',?,?)",
                           (now(),'ai-verification' if ai.paid_enabled() else 'verification-disabled',
                            'automatic' if automatic else 'manual')).lastrowid
    owned = client is None
    client = client or httpx.AsyncClient()
    feed_results = []
    accepted = rejected = failed = pending = checked = 0
    new = []
    try:
        results = await asyncio.gather(*(fetch_feed(client,f) for f in feeds),return_exceptions=True)
        fetched = {}
        for feed, result in zip(feeds,results):
            if isinstance(result,BaseException):
                feed_results.append({'key':feed['key'],'name':feed['name'],'ok':False,
                                     'error':'Source could not be checked'})
                continue
            feed_results.append({'key':feed['key'],'name':feed['name'],'ok':True,'items':len(result)})
            for it in result:
                fetched.setdefault(it['external_id'],(it,feed))
        with connection() as c:
            active_ids = {r[0] for r in c.execute('SELECT external_id FROM signals')}
            cached = {r['external_id']:dict(r) for r in c.execute('SELECT * FROM signal_candidates')}
            known = [title_tokens(r[0]) for r in c.execute('SELECT title FROM signals WHERE published_date>=?',
                     ((datetime.now(timezone.utc)-timedelta(days=90)).date().isoformat(),))]
            known += [title_tokens(json.loads(r['source_item'])['title']) for r in cached.values()]
        candidates = sorted(fetched.values(),key=lambda pair:pair[0].get('published_at') or
                            pair[0].get('published_date',''),reverse=True)[:MAX_NEW_ITEMS_PER_RUN]
        ready = []
        for it,feed in candidates:
            eid = it['external_id']
            if eid in active_ids:
                continue
            old = cached.get(eid)
            unchanged = old and old['content_hash']==ai.fingerprint(it)
            if unchanged and old['status'] in ('published','rejected'):
                continue
            # Disabled verification caches quarantine without repeating work daily.
            if unchanged and not (ai.paid_enabled() and configured()):
                continue
            # Failed/unsupported unchanged candidates retry at most once per UTC day.
            if unchanged and old['checked_at'][:10]==ai.utc_day():
                continue
            checked += 1
            error = ai.identity_error(it,feed)
            tokens = title_tokens(it['title'])
            duplicate = not old and any(near_duplicate(tokens,k) for k in known)
            if error or duplicate:
                reason = error or 'Duplicate evidence story'
                with connection() as c:
                    quarantine(c,it,run_id,'rejected',reason)
                rejected += 1
                continue
            allowed, reason = await ai.prefilter(it,catalog)
            if allowed is None:
                with connection() as c:
                    quarantine(c,it,run_id,'quarantined',reason)
                pending += 1
                known.append(tokens)
                continue
            known.append(tokens)
            ready.append((it,allowed))
        offset = 0
        while offset < len(ready):
            remaining = ready[offset:]
            count = ai.reserve_batch(len(remaining))
            if not count:
                reason = ('Paid AI verification is off' if not ai.paid_enabled() else
                          'AI unavailable or daily verification quota exhausted')
                with connection() as c:
                    for it,_ in remaining:
                        quarantine(c,it,run_id,'quarantined',reason)
                        pending += 1
                break
            batch = remaining[:count]
            offset += count
            try:
                replies = await ai.analyse([it for it,_ in batch],catalog)
                if not isinstance(replies,list) or len(replies)!=count:
                    raise ValueError('Incomplete verification results')
            except Exception:
                # Never save/log provider exceptions, credentials or raw model responses.
                replies = [None]*count
                failed += count
            for (it,allowed),reply in zip(batch,replies):
                proposal,reason = await ai.validate_analysis(it,reply,catalog,allowed)
                with connection() as c:
                    c.execute('BEGIN IMMEDIATE')
                    usage = c.execute('SELECT published FROM signal_ai_usage WHERE day=?',
                                      (ai.utc_day(),)).fetchone()
                    if proposal is None or not usage or usage[0]>=ai.MAX_DAILY_PUBLICATIONS:
                        quarantine(c,it,run_id,'quarantined',
                                   reason or 'Daily publication safety limit reached')
                        pending += 1
                        continue
                    # Recheck source/config state at the publication boundary.
                    if public_demo() or not ai.paid_enabled() or not configured():
                        quarantine(c,it,run_id,'quarantined','Verification configuration changed')
                        pending += 1
                        continue
                    signal = {k:it[k] for k in ('external_id','feed_key','title','source_name',
                              'source_type','url','published_date')}
                    signal.update({k:proposal[k] for k in
                                   ('summary','direction','strength','role_ids','skill_ids')})
                    signal.update(fetched_at=now()[:10],tagged_by='claude-verified',run_id=run_id)
                    sid = insert_signal(c,signal)
                    if sid:
                        c.execute('UPDATE signal_ai_usage SET published=published+1 WHERE day=?',(ai.utc_day(),))
                        quarantine(c,it,run_id,'published','AI analysis and automated evidence checks passed',sid)
                        accepted += 1
                        new.append({'id':sid,'title':it['title'],'direction':proposal['direction']})
        any_ok = any(f['ok'] for f in feed_results)
        status = 'failed' if not any_ok else ('ok' if all(f['ok'] for f in feed_results) and not failed else 'partial')
        with connection() as c:
            c.execute('UPDATE refresh_runs SET finished_at=?,status=?,feeds=?,checked=?,accepted=?,pending=?,rejected=?,failed=? WHERE id=?',
                      (now(),status,json.dumps(feed_results),checked,accepted,pending,rejected,failed,run_id))
        return {'run_id':run_id,'status':status,'tagger':'ai-verification','model':None,
                'feeds':feed_results,'checked':checked,'accepted':accepted,'pending':pending,
                'quarantined':pending,'rejected':rejected,'failed':failed,'new_signals':new}
    except Exception:
        with connection() as c:
            c.execute("UPDATE refresh_runs SET finished_at=?,status='failed',error=? WHERE id=?",
                      (now(),'Signal check failed safely; no unverified evidence published',run_id))
        raise
    finally:
        if owned:
            await client.aclose()
        from .schedule import record_check
        record_check()
