"""Signals V2: fail-closed publication, bounded AI usage, provenance and scheduling."""
import asyncio
import base64
import json
import os
from datetime import date,datetime,timedelta,timezone
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient

from backend import storage
from backend.app import app
from backend.catalog import ROLES,SKILLS
from backend.signals import refresh,schedule,verification as ai
from backend.signals.fetch import parse_feed_xml
from backend.signals.guardrails import source_error

TOKEN='synthetic-review-token'
AUTH={'Authorization':'Bearer '+TOKEN}
FEED={'kind':'rss','key':'v2-test','name':'Synthetic feed','url':'https://feeds.test/rss',
      'source_type':'news','max_items':40,'max_age_days':45}
QUOTE='Malaysian employers need cybersecurity workers to address a growing shortage of security talent.'
CATALOG={'roles':ROLES,'skills':SKILLS}


@pytest.fixture(autouse=True)
def isolated(tmp_path,monkeypatch):
    monkeypatch.setattr(storage,'DB',tmp_path/'v2.sqlite3')
    monkeypatch.setenv('FUTUREPATH_PUBLIC_DEMO','0')
    monkeypatch.setenv('SIGNALS_REFRESH_HOURS','0')
    monkeypatch.setenv('ADMIN_TOKEN',TOKEN)
    monkeypatch.delenv('SIGNALS_PAID_AI_ENABLED',raising=False)
    monkeypatch.delenv('SIGNALS_AI_DAILY_ITEMS',raising=False)
    monkeypatch.delenv('SIGNALS_AI_DAILY_CALLS',raising=False)
    storage.init()


def paid(monkeypatch,items='16',calls='4'):
    monkeypatch.setattr(ai,'durable_storage_ready',lambda:True)
    monkeypatch.setenv('SIGNALS_PAID_AI_ENABLED','1')
    monkeypatch.setenv('SIGNALS_AI_DAILY_ITEMS',items)
    monkeypatch.setenv('SIGNALS_AI_DAILY_CALLS',calls)
    monkeypatch.setenv('ANTHROPIC_API_KEY','fictional-offline-key')


def proposal(**kw):
    return {'index':0,'relevant':True,'reason':'Grounded demand evidence',
            'direction':'emerging','strength':3,'summary':QUOTE,'supporting_quote':QUOTE,
            'role_ids':['cybersecurity-analyst'],'skill_ids':['SK011'],**kw}


def item(**kw):
    return {'external_id':'v2-test:example','feed_key':'v2-test',
            'title':'Malaysia cybersecurity hiring grows','source_name':'Synthetic publisher',
            'source_type':'news','url':'https://news.test/evidence',
            'published_date':(date.today()-timedelta(days=1)).isoformat(),'snippet':QUOTE,**kw}


def run(items=None,automatic=True,feeds=None):
    items=items or [item()]
    # Parser/fetch are tested separately; pipeline gets deterministic real source metadata.
    async def fetch(client,feed):
        return items
    original=refresh.fetch_feed
    refresh.fetch_feed=fetch
    async def invoke():
        async with httpx.AsyncClient(transport=httpx.MockTransport(
                lambda r:httpx.Response(200,text='unused'))) as client:
            return await refresh.refresh_signals(feeds=feeds or [FEED],client=client,automatic=automatic)
    try:
        return asyncio.run(invoke())
    finally:
        refresh.fetch_feed=original


def test_credentials_do_not_enable_paid_verification_or_publication(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY','fictional-configured-key')
    async def forbidden(*args):
        pytest.fail('Paid verification was not approved')
    monkeypatch.setattr(ai,'analyse',forbidden)
    api=TestClient(app)
    before={p:api.get(p).json() for p in ('/api/signals','/api/matches','/api/radar','/api/skill-trends')}
    result=run()
    assert result['accepted']==0 and result['quarantined']==1
    for path,value in before.items():
        assert api.get(path).json()==value
    assert api.get('/api/what-changed').json()['has_change'] is False
    status=api.get('/api/signals/status').json()
    assert not status['paid_verification_enabled'] and status['quarantined_count']==1
    with storage.connection() as c:
        assert c.execute('SELECT COUNT(*) FROM signal_ingestion_audit').fetchone()[0]==1
    assert run()['checked']==0


def test_actual_ai_analysis_then_guardrails_publishes_without_admin(monkeypatch):
    paid(monkeypatch)
    monkeypatch.delenv('ADMIN_TOKEN')
    calls=[]
    async def analysis(items,catalog):
        calls.append(items)
        return [proposal() for _ in items]
    monkeypatch.setattr(ai,'analyse',analysis)
    api=TestClient(app)
    before=api.get('/api/matches').json()
    result=run()
    assert result['accepted']==1 and result['quarantined']==0 and len(calls)==1
    active=next(s for s in api.get('/api/signals').json() if s['external_id']=='v2-test:example')
    assert active['tagged_by']=='claude-verified' and active['strength']==1
    assert active['provenance']=='live_ai_validated'
    assert api.get('/api/matches').json()!=before
    assert api.get('/api/what-changed').json()['new_signal_count']==1
    assert run()['checked']==0 and len(calls)==1


@pytest.mark.parametrize('change',[
    {'supporting_quote':'Fabricated evidence that was never published by this source.'},
    {'summary':'Invented 50000 new jobs'}, {'role_ids':['space-pilot']},
    {'skill_ids':['SK999']}, {'role_ids':['data-analyst']},
    {'direction':'declining'}, {'relevant':False}, {'role_ids':'cybersecurity-analyst'},
])
def test_unsupported_ai_output_cannot_publish_or_move_scores(monkeypatch,change):
    paid(monkeypatch)
    async def analysis(*args):return [proposal(**change)]
    monkeypatch.setattr(ai,'analyse',analysis)
    before=TestClient(app).get('/api/matches').json()
    result=run()
    assert result['accepted']==0 and result['quarantined']==1
    assert TestClient(app).get('/api/matches').json()==before
    assert TestClient(app).get('/api/what-changed').json()['has_change'] is False


def test_provider_error_is_sanitized_and_cannot_fall_back(monkeypatch):
    paid(monkeypatch)
    async def failed(*args):raise RuntimeError('DO_NOT_SAVE_RAW_MODEL_OR_CREDENTIALS')
    monkeypatch.setattr(ai,'analyse',failed)
    result=run()
    assert result['accepted']==0 and result['failed']==1 and result['quarantined']==1
    with storage.connection() as c:
        assert 'DO_NOT_SAVE' not in json.dumps([dict(r) for r in c.execute('SELECT * FROM signal_ingestion_audit')])
        assert c.execute('SELECT calls FROM signal_ai_usage').fetchone()[0]==1


def test_prefilter_excludes_irrelevant_and_headline_only_without_ai(monkeypatch):
    paid(monkeypatch)
    async def forbidden(*args):pytest.fail('Prefilter should prevent AI call')
    monkeypatch.setattr(ai,'analyse',forbidden)
    records=[item(snippet='Short teaser'),item(external_id='v2-test:other',title='Celebrity wedding',
            snippet='A completely unrelated celebrity wedding is the subject of this article, with photographs.')]
    result=run(records)
    assert result['accepted']==0 and result['quarantined']==2


def test_quota_is_hard_persistent_and_reserved_before_request(monkeypatch):
    paid(monkeypatch,items='2',calls='1')
    assert ai.reserve_batch(100)==2
    storage.init()
    assert ai.reserve_batch(1)==0
    with storage.connection() as c:
        row=c.execute('SELECT * FROM signal_ai_usage').fetchone()
        assert row['items']==2 and row['calls']==1
    monkeypatch.setenv('SIGNALS_AI_DAILY_ITEMS','999999')
    monkeypatch.setenv('SIGNALS_AI_DAILY_CALLS','999999')
    assert ai.reserve_batch(99)==4
    with storage.connection() as c:c.execute('UPDATE signal_ai_usage SET published=3')
    assert ai.reserve_batch(1)==0


def test_paid_switch_requires_both_explicit_positive_quotas(monkeypatch):
    monkeypatch.setattr(ai,'durable_storage_ready',lambda:True)
    monkeypatch.setenv('SIGNALS_PAID_AI_ENABLED','1')
    assert not ai.paid_enabled()


def test_ephemeral_storage_cannot_enable_paid_usage(monkeypatch):
    # Every switch is on, but the budget database is disposable, so paid verification stays off.
    monkeypatch.setenv('SIGNALS_PAID_AI_ENABLED','1')
    monkeypatch.setenv('SIGNALS_AI_DAILY_ITEMS','16')
    monkeypatch.setenv('SIGNALS_AI_DAILY_CALLS','4')
    monkeypatch.setenv('SIGNALS_AI_DURABLE_STORAGE_CONFIRMED','1')
    disposable=[Path(':memory:')]
    if os.name=='posix':  # the /tmp check is the Linux deployment rule (Replit keeps its demo DB in /tmp)
        disposable+=[Path('/tmp/futurepath-budget.sqlite3'),Path('/var/tmp/futurepath-budget.sqlite3')]
    for path in disposable:
        monkeypatch.setattr(storage,'DB',path)
        assert not ai.durable_storage_ready() and not ai.paid_enabled()


def test_paid_quotas_must_be_positive_whole_numbers(monkeypatch):
    monkeypatch.setattr(ai,'durable_storage_ready',lambda:True)
    monkeypatch.setenv('SIGNALS_PAID_AI_ENABLED','1')
    monkeypatch.setenv('SIGNALS_AI_DAILY_ITEMS','2')
    monkeypatch.setenv('SIGNALS_AI_DAILY_CALLS','1')
    assert ai.paid_enabled()
    for bad in ('0','-3','nan',''):
        monkeypatch.setenv('SIGNALS_AI_DAILY_ITEMS',bad)
        assert not ai.paid_enabled()


@pytest.mark.parametrize('field,value',[
    ('url','javascript:unsafe'),('url','http://127.0.0.1/a'),
    ('published_date','2999-01-01'),('source_name',''),('feed_key','spoofed'),
])
def test_bad_source_is_rejected_before_ai(field,value,monkeypatch):
    paid(monkeypatch)
    async def forbidden(*args):pytest.fail('Invalid source must not reach AI')
    monkeypatch.setattr(ai,'analyse',forbidden)
    result=run([item(**{field:value})])
    assert result['rejected']==1 and result['accepted']==0


def test_configured_source_identity_checks():
    gnews={**FEED,'key':'gnews-test','name':'Google News'}
    assert ai.identity_error(item(feed_key='gnews-test',external_id='gnews-test:x'),gnews)
    arxiv={**FEED,'key':'arxiv-test'}
    assert ai.identity_error(item(feed_key='arxiv-test',external_id='arxiv-test:x'),arxiv)


def test_chronology_uses_publication_not_ingestion_and_preserves_curated(monkeypatch):
    paid(monkeypatch)
    async def analysis(*args):return [proposal()]
    monkeypatch.setattr(ai,'analyse',analysis)
    day=(date.today()-timedelta(days=1)).isoformat()
    run([item(published_at=day+'T22:00:00+00:00')])
    api=TestClient(app)
    data=api.get('/api/signals').json()
    row=next(s for s in data if s['external_id']=='v2-test:example')
    assert row['published_at']==day+'T22:00:00+00:00'
    assert any(s['provenance']=='curated' for s in data)
    paged=api.get('/api/signals?limit=8&offset=8').json()
    assert paged==data[8:16]
    with storage.connection() as c:
        c.execute("UPDATE signals SET tagged_by='keyword' WHERE external_id='v2-test:example'")
    assert next(s for s in api.get('/api/signals').json() if s['external_id']=='v2-test:example')['provenance']=='stored'


def test_timestamp_parser_sorts_true_publication_time():
    day=(date.today()-timedelta(days=1)).isoformat()
    xml='<rss><channel>'+''.join(
        f'<item><title>{n}</title><link>https://news.test/{n}</link><pubDate>{day}T{hour}:00:00+00:00</pubDate></item>'
        for n,hour in [('early','08'),('late','21')])+'</channel></rss>'
    rows=parse_feed_xml(xml,FEED)
    assert [r['title'] for r in rows]==['late','early']


@pytest.mark.parametrize('method,path',[
    ('get','/api/signals/review'),('post','/api/signals/review/1/approve'),
    ('post','/api/signals/review/1/reject')])
def test_historical_privileged_routes_remain_authorized_but_cannot_publish(method,path):
    api=TestClient(app)
    assert getattr(api,method)(path).status_code==401
    if method=='post':
        assert getattr(api,method)(path,headers=AUTH).status_code==410


def test_public_demo_independently_blocks_mutations_and_timer(monkeypatch):
    monkeypatch.setenv('FUTUREPATH_PUBLIC_DEMO','1')
    monkeypatch.setenv('SIGNALS_REFRESH_HOURS','24')
    monkeypatch.setenv('FUTUREPATH_DEMO_PASSWORD','fictional-public-demo-password')
    basic={'Authorization':'Basic '+base64.b64encode(b'judge:fictional-public-demo-password').decode()}
    api=TestClient(app)
    for path in ('/api/signals/refresh','/api/signals/review/1/approve','/api/signals/review/1/reject'):
        assert api.post(path,headers=basic).status_code==403
    assert schedule.interval_hours()==0
    with pytest.raises(RuntimeError,match='public demo'):run()
    assert api.get('/api/signals/status',headers=basic).json()['next_expected_run'] is None


def test_delayed_schedule_restart_disable_and_honest_status(monkeypatch):
    monkeypatch.setenv('SIGNALS_REFRESH_HOURS','24')
    now=datetime(2026,10,24,12,tzinfo=timezone.utc)
    assert schedule.next_due() is None
    due=now+timedelta(hours=24)
    assert schedule.initialize_schedule(now)==due
    assert schedule.initialize_schedule(now+timedelta(hours=1))==due
    storage.init()
    assert schedule.next_due()==due
    overdue=due+timedelta(hours=2)
    assert schedule.initialize_schedule(overdue)==overdue+timedelta(hours=24)
    monkeypatch.setenv('SIGNALS_REFRESH_HOURS','0')
    assert schedule.initialize_schedule(overdue) is None
    status=TestClient(app).get('/api/signals/status').json()
    assert not status['schedule_guaranteed'] and status['next_expected_run'] is None


@pytest.mark.parametrize('value',['0','-1','nan','inf','invalid'])
def test_schedule_bad_values_fail_closed(value,monkeypatch):
    monkeypatch.setenv('SIGNALS_REFRESH_HOURS',value)
    assert schedule.interval_hours()==0
