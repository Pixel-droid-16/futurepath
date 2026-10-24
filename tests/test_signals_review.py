"""Offline staging, approval, scheduling and public-demo safety contracts."""
import asyncio
import base64
import json
from datetime import datetime, timedelta, timezone, date

import httpx
import pytest
from fastapi.testclient import TestClient

from backend import storage
from backend.app import app
from backend.signals import refresh, schedule
from backend.signals.guardrails import source_error
from backend.signals.review import decide
from backend.signals.tagging import KeywordTagger

TOKEN = 'synthetic-review-token'
AUTH = {'Authorization': 'Bearer ' + TOKEN}
FEED = {'kind': 'rss', 'key': 'review-test', 'name': 'Synthetic test feed',
        'url': 'https://feeds.test/rss', 'source_type': 'news',
        'max_items': 10, 'max_age_days': 45}


@pytest.fixture(autouse=True)
def isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, 'DB', tmp_path / 'review.sqlite3')
    monkeypatch.setenv('FUTUREPATH_PUBLIC_DEMO', '0')
    monkeypatch.setenv('SIGNALS_REFRESH_HOURS', '0')
    monkeypatch.setenv('ADMIN_TOKEN', TOKEN)
    storage.init()


def stage(automatic=False, url='https://news.test/evidence', title=None, guid='one'):
    published = (date.today() - timedelta(days=1)).strftime('%a, %d %b %Y 08:00:00 GMT')
    title = title or 'Malaysia faces cybersecurity talent shortage as hiring expands'
    xml = (f'<rss><channel><item><title>{title}</title><guid>{guid}</guid>'
           f'<link>{url}</link><pubDate>{published}</pubDate>'
           '<description>Malaysian employers need cybersecurity skills.</description>'
           '</item></channel></rss>')

    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(
                lambda request: httpx.Response(200, text=xml))) as client:
            return await refresh.refresh_signals(
                feeds=[FEED], tagger=None if automatic else KeywordTagger(),
                client=client, automatic=automatic)
    return asyncio.run(run())


def scored(api):
    return {path: api.get(path).json() for path in
            ('/api/matches', '/api/radar', '/api/skill-outlook', '/api/skill-trends')}


def test_pending_and_rejected_never_enter_active_scoring():
    api = TestClient(app)
    baseline = scored(api)
    active = api.get('/api/signals').json()
    out = stage()
    assert out['accepted'] == 0 and out['pending'] == 1 and out['new_signals'] == []
    assert api.get('/api/signals').json() == active
    after = scored(api)
    for path in ('/api/matches', '/api/radar', '/api/skill-trends'):
        assert after[path] == baseline[path]
    for key in ('rising', 'declining'):
        assert after['/api/skill-outlook'][key] == baseline['/api/skill-outlook'][key]
    assert api.get('/api/what-changed').json()['has_change'] is False
    queue = api.get('/api/signals/review', headers=AUTH).json()
    assert queue['total'] == 1
    item = queue['items'][0]
    response = api.post(f"/api/signals/review/{item['id']}/reject",
                        headers=AUTH, json={'reason': 'Insufficient evidence'})
    assert response.json()['status'] == 'rejected'
    assert api.get('/api/signals').json() == active
    assert api.get('/api/matches').json() == baseline['/api/matches']
    assert api.get('/api/what-changed').json()['has_change'] is False
    assert api.get('/api/signals/status').json()['pending_count'] == 0
    assert stage()['checked'] == 0


def test_approval_changes_only_after_authenticated_decision_and_is_audited():
    api = TestClient(app)
    before = api.get('/api/matches').json()
    out = stage()
    item = api.get('/api/signals/review', headers=AUTH).json()['items'][0]
    rid = item['id']
    approved = api.post(f'/api/signals/review/{rid}/approve', headers=AUTH,
                        json={'reason': 'Source reviewed'})
    assert approved.status_code == 200 and approved.json()['signal_id']
    assert api.get('/api/matches').json() != before
    assert api.get('/api/what-changed').json()['has_change'] is True
    assert api.get('/api/signals/status').json()['last_approved_at']
    assert api.post(f'/api/signals/review/{rid}/approve', headers=AUTH).status_code == 409
    assert api.post(f'/api/signals/review/{rid}/reject', headers=AUTH).status_code == 409
    with storage.connection() as c:
        events = list(c.execute('SELECT action,reason FROM signal_review_events ORDER BY id'))
        assert [r['action'] for r in events] == ['staged', 'approved']
        assert events[-1]['reason'] == 'Source reviewed'
        assert c.execute('SELECT accepted,pending FROM refresh_runs WHERE id=?',
                         (out['run_id'],)).fetchone()['accepted'] == 1
    assert stage()['pending'] == 0
    storage.init()
    assert api.get('/api/signals/review?status=approved', headers=AUTH).json()['total'] == 1


@pytest.mark.parametrize('method,path', [
    ('get', '/api/signals/review'),
    ('post', '/api/signals/review/1/approve'),
    ('post', '/api/signals/review/1/reject'),
])
def test_review_always_requires_bearer_even_on_localhost(method, path, monkeypatch):
    api = TestClient(app)
    request = getattr(api, method)
    assert request(path).status_code == 401
    assert request(path, headers={'Authorization': 'Bearer wrong'}).status_code == 401
    assert request(path, headers={'Authorization': 'Basic irrelevant'}).status_code == 401
    monkeypatch.delenv('ADMIN_TOKEN')
    assert request(path).status_code == 503


def test_public_demo_blocks_all_mutations_and_background(monkeypatch):
    stage()
    monkeypatch.setenv('FUTUREPATH_PUBLIC_DEMO', '1')
    monkeypatch.setenv('SIGNALS_REFRESH_HOURS', '24')
    password = 'fictional-public-demo-password'
    monkeypatch.setenv('FUTUREPATH_DEMO_PASSWORD', password)
    basic = {'Authorization': 'Basic ' + base64.b64encode(
        ('judge:' + password).encode()).decode()}
    api = TestClient(app)
    for path in ('/api/signals/refresh', '/api/signals/review/1/approve',
                 '/api/signals/review/1/reject'):
        assert api.post(path, headers=basic).status_code == 403
    assert api.get('/api/signals/review', headers=basic).status_code == 403
    status = api.get('/api/signals/status', headers=basic).json()
    assert status['enabled'] is False and status['next_due'] is None
    assert schedule.interval_hours() == 0
    assert schedule.initialize_schedule() is None
    with pytest.raises(RuntimeError, match='public demo'):
        stage(automatic=True)


def test_automatic_forces_keywords_even_with_claude_credentials(monkeypatch):
    def forbidden():
        pytest.fail('Automatic check must not instantiate the paid default tagger')
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'fictional-key')
    monkeypatch.setattr(refresh, 'default_tagger', forbidden)
    out = stage(automatic=True)
    assert out['tagger'] == 'keyword' and out['model'] is None and out['pending'] == 1
    with storage.connection() as c:
        assert c.execute('SELECT trigger FROM refresh_runs').fetchone()[0] == 'automatic'


def test_first_activation_restart_overdue_and_disable_reenable(monkeypatch):
    now = datetime(2026, 10, 24, 12, tzinfo=timezone.utc)
    monkeypatch.setenv('SIGNALS_REFRESH_HOURS', '24')
    due = now + timedelta(hours=24)
    assert schedule.next_due() is None
    assert schedule.initialize_schedule(now) == due
    assert schedule.initialize_schedule(now + timedelta(hours=1)) == due
    storage.init()  # additive migrations do not erase timing
    assert schedule.next_due() == due
    later = due + timedelta(hours=3)
    assert schedule.initialize_schedule(later) == later + timedelta(hours=24)
    monkeypatch.setenv('SIGNALS_REFRESH_HOURS', '0')
    assert schedule.initialize_schedule(later) is None
    monkeypatch.setenv('SIGNALS_REFRESH_HOURS', '24')
    assert schedule.initialize_schedule(later) == later + timedelta(hours=24)


@pytest.mark.parametrize('value', ['0', '-1', 'nan', 'inf', 'invalid'])
def test_bad_schedule_values_fail_closed(value, monkeypatch):
    monkeypatch.setenv('SIGNALS_REFRESH_HOURS', value)
    assert schedule.interval_hours() == 0


def test_no_auto_tagger_or_fetch_before_first_full_interval(monkeypatch):
    now = datetime(2026, 10, 24, 12, tzinfo=timezone.utc)
    current = [now]
    calls = []
    monkeypatch.setenv('SIGNALS_REFRESH_HOURS', '24')
    monkeypatch.setattr(schedule, 'clock', lambda: current[0])

    async def sleep(seconds):
        current[0] += timedelta(seconds=seconds)
    async def refresh_mock(**kwargs):
        calls.append((current[0], kwargs))
        raise asyncio.CancelledError()
    monkeypatch.setattr(schedule.asyncio, 'sleep', sleep)
    monkeypatch.setattr(schedule, 'refresh_signals', refresh_mock)
    with pytest.raises(asyncio.CancelledError):
        asyncio.run(schedule.run_forever())
    assert calls == [(now + timedelta(hours=24), {'automatic': True})]


def test_status_and_reload_are_read_only_without_admin():
    api = TestClient(app)
    for path in ('/api/signals/status', '/api/signals', '/api/signals/runs',
                 '/api/skill-trends', '/api/skill-outlook'):
        assert api.get(path).status_code == 200
    assert schedule.next_due() is None
    with storage.connection() as c:
        assert c.execute('SELECT COUNT(*) FROM signal_schedule').fetchone()[0] == 0


@pytest.mark.parametrize('url', ['javascript:alert(1)', 'https://localhost/a',
                               'http://127.0.0.1/a', 'https://user:pass@news.test/a'])
def test_source_validation_rejects_unsafe_links(url):
    out = stage(url=url)
    assert out['pending'] == 0 and out['rejected'] == 1


def test_near_duplicate_pending_items_are_not_queued_again():
    assert stage()['pending'] == 1
    out = stage(title='Malaysia faces cybersecurity talent shortage as hiring expands again',
                guid='another', url='https://news.test/another')
    assert out['pending'] == 0 and out['rejected'] == 1


def test_approval_revalidates_persisted_evidence():
    stage()
    with storage.connection() as c:
        row = c.execute('SELECT * FROM signal_review').fetchone()
        item = json.loads(row['source_item'])
        item['url'] = 'javascript:unsafe'
        c.execute('UPDATE signal_review SET source_item=? WHERE id=?',
                  (json.dumps(item), row['id']))
    with pytest.raises(Exception) as error:
        decide(row['id'], 'approved')
    assert error.value.status_code == 409
    assert TestClient(app).get('/api/what-changed').json()['has_change'] is False


@pytest.mark.parametrize('field,value', [
    ('published_date','2999-01-01'), ('published_date','not-a-date'),
    ('source_name',''), ('source_type','invented'), ('external_id','wrong:identifier'),
])
def test_source_metadata_is_validated(field,value):
    item={'external_id':'test:1','feed_key':'test','title':'Synthetic source title',
          'source_name':'Synthetic source','source_type':'news',
          'url':'https://example.com/evidence','published_date':'2026-01-01'}
    assert source_error({**item,field:value}) is not None


def test_public_status_does_not_expose_tokens_or_queue_contents():
    stage()
    response=TestClient(app).get('/api/signals/status')
    assert response.json()['pending_count']==1
    assert TOKEN not in response.text and 'news.test/evidence' not in response.text
