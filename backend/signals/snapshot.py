"""Validated, cached, public GitHub snapshot for automatically approved feed evidence."""
import logging
import os
import threading
import time
from datetime import date, datetime, timedelta, timezone
import httpx
from ..catalog import ROLES, SKILLS
from .guardrails import source_error

SNAPSHOT_URL = 'https://raw.githubusercontent.com/Pixel-droid-16/futurepath/main/data/live_signals.json'
CACHE_SECONDS = 300
log = logging.getLogger('futurepath.signals.snapshot')
_lock = threading.Lock()
_cache = {'time':0.0, 'signals':[], 'meta':None}
ROLES_SET = {r['id'] for r in ROLES}
SKILLS_SET = {s['id'] for s in SKILLS}

def enabled():
    return os.getenv('SIGNALS_REMOTE_SNAPSHOT_ENABLED','').strip().lower() in ('1','true','yes')

def validate_signal(raw):
    if not isinstance(raw,dict) or raw.get('tagged_by') != 'claude':
        return None
    fields = ('external_id','feed_key','title','source_name','source_type',
              'url','published_date','fetched_at','summary','direction',
              'strength','role_ids','skill_ids')
    row = {key:raw.get(key) for key in fields}
    if source_error(row) or not row['url'].startswith('https://'):
        return None
    if row['direction'] not in ('emerging','declining'):
        return None
    if type(row['strength']) is not int or not (1 <= row['strength'] <= 2):
        return None
    roles,skills = row['role_ids'],row['skill_ids']
    if not isinstance(roles,list) or not isinstance(skills,list):
        return None
    if (len(roles)>12 or len(skills)>100 or not (roles or skills)
            or any(not isinstance(v,str) or v not in ROLES_SET for v in roles)
            or any(not isinstance(v,str) or v not in SKILLS_SET for v in skills)):
        return None
    if not isinstance(row['summary'],str) or not (0<len(row['summary'])<=400):
        return None
    if not isinstance(row['fetched_at'],str):
        return None
    try:
        if date.fromisoformat(row['fetched_at']) > datetime.now(timezone.utc).date():
            return None
    except ValueError:
        return None
    return {**row,'tagged_by':'claude','run_id':None}

def validate_document(data):
    if not isinstance(data,dict) or data.get('schema_version') != 1:
        raise ValueError('Invalid snapshot schema')
    candidates=data.get('signals')
    if not isinstance(candidates,list) or len(candidates)>200:
        raise ValueError('Invalid signal count')
    if data.get('status') not in ('not_checked','ok','partial','failed'):
        raise ValueError('Invalid status')
    checked=data.get('checked_at')
    if checked is not None:
        dt=datetime.fromisoformat(checked)
        if dt.tzinfo is None or dt > datetime.now(timezone.utc)+timedelta(minutes=5):
            raise ValueError('Invalid check time')
    seen=set()
    valid=[]
    for entry in candidates:
        signal=validate_signal(entry)
        if signal and signal['external_id'] not in seen:
            valid.append(signal)
            seen.add(signal['external_id'])
    return valid, {'checked_at':checked,
                   'last_successful_at':data.get('last_successful_at'),
                   'status':data['status'],
                   'ai_enabled':data.get('ai_enabled') is True,
                   'external_scheduler':True,'verified_count':len(valid)}

def read_snapshot():
    if not enabled():
        return [],None
    now=time.monotonic()
    if now-_cache['time'] < CACHE_SECONDS:
        return _cache['signals'],_cache['meta']
    with _lock:
        now=time.monotonic()
        if now-_cache['time'] < CACHE_SECONDS:
            return _cache['signals'],_cache['meta']
        _cache['time']=now
        try:
            response=httpx.get(SNAPSHOT_URL,timeout=5.0,follow_redirects=False)
            response.raise_for_status()
            if len(response.content)>512_000:
                raise ValueError('Oversized public snapshot')
            rows,meta=validate_document(response.json())
            _cache['signals'],_cache['meta']=rows,meta
        except (httpx.HTTPError,ValueError,TypeError,KeyError):
            log.warning('Evidence snapshot unavailable; retained verified evidence')
        return _cache['signals'],_cache['meta']
