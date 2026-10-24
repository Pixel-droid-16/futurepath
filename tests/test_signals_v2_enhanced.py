"""Isolated Signals V2 checks. No real feed traffic or paid models."""
import asyncio
import importlib.util
import json
import os
from datetime import date, timedelta
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient

from backend import storage
from backend.app import app
from backend.signals import refresh, verification

FEED = {
    'kind': 'rss', 'key': 'enhanced-test', 'name': 'Fictional job feed',
    'source_type': 'news', 'url': 'https://feeds.test/rss',
    'max_items': 8, 'max_age_days': 45,
}


@pytest.fixture(autouse=True)
def isolated_database(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, 'DB', tmp_path / 'signals-v2.sqlite3')
    monkeypatch.setenv('FUTUREPATH_PUBLIC_DEMO', '0')
    monkeypatch.setenv('SIGNALS_REFRESH_HOURS', '0')
    monkeypatch.delenv('SIGNALS_AUTO_AI_ENABLED', raising=False)
    monkeypatch.delenv('ANTHROPIC_API_KEY', raising=False)
    monkeypatch.setenv('SIGNALS_REMOTE_SNAPSHOT_ENABLED', '0')
    # The daily worker sets these for its own run; recording them here restores them afterwards.
    for name in ('SIGNALS_PAID_AI_ENABLED', 'SIGNALS_AI_DAILY_ITEMS', 'SIGNALS_AI_DAILY_CALLS',
                 'SIGNALS_AI_DURABLE_STORAGE_CONFIRMED', 'RUNNER_TEMP'):
        monkeypatch.delenv(name, raising=False)
    storage.init()


def run_check():
    published = (date.today() - timedelta(days=1)).strftime('%a, %d %b %Y 08:00:00 GMT')
    xml = (f'<rss><channel><item><title>Malaysia faces cybersecurity talent shortage as hiring expands</title>'
           f'<guid>one</guid><link>https://news.test/evidence</link><pubDate>{published}</pubDate>'
           '<description>Malaysian employers need cybersecurity skills and plan to hire more skilled workers.</description>'
           '</item></channel></rss>')

    async def run():
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(lambda request: httpx.Response(200, text=xml))
        ) as client:
            return await refresh.refresh_signals(
                feeds=[FEED], client=client, automatic=True
            )

    return asyncio.run(run())


def test_automatic_without_opt_in_never_publishes():
    before = TestClient(app).get('/api/signals').json()
    result = run_check()
    assert result['accepted'] == 0
    assert result['pending'] == 1
    assert TestClient(app).get('/api/signals').json() == before


ROOT = Path(__file__).resolve().parents[1]


def load_worker():
    """The daily GitHub Actions worker, imported the way the workflow runs it."""
    spec = importlib.util.spec_from_file_location('update_live_signals', ROOT / 'scripts/update_live_signals.py')
    worker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(worker)
    return worker


def test_daily_worker_needs_actions_variable_and_key(monkeypatch):
    worker = load_worker()
    previous = {'ai_enabled': False, 'checked_at': None}
    assert not worker.enable_verification(previous)
    monkeypatch.setenv('SIGNALS_AUTO_AI_ENABLED', '1')
    assert not worker.enable_verification(previous)
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'synthetic-test-key')
    assert worker.enable_verification(previous)
    assert os.environ['SIGNALS_PAID_AI_ENABLED'] == '1'
    assert os.environ['SIGNALS_AI_DURABLE_STORAGE_CONFIRMED'] == '1'


def test_daily_worker_allows_one_paid_run_per_utc_day(monkeypatch):
    worker = load_worker()
    monkeypatch.setenv('SIGNALS_AUTO_AI_ENABLED', '1')
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'synthetic-test-key')
    today = verification.utc_day()
    assert not worker.enable_verification({'last_ai_check_day': today})
    # Snapshots written before last_ai_check_day existed fall back to checked_at.
    assert not worker.enable_verification({'ai_enabled': True, 'checked_at': today + 'T02:17:00+00:00'})
    assert worker.enable_verification({'ai_enabled': True, 'checked_at': '2026-01-01T02:17:00+00:00'})


def test_daily_worker_exports_verified_rows_as_snapshot(monkeypatch, tmp_path):
    worker = load_worker()
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    def signal(key, tagged_by):
        return {'external_id': f'fictional:{key}', 'feed_key': 'fictional', 'title': f'Malaysia {key} jobs expand',
                'source_name': 'Fictional source', 'source_type': 'news', 'url': f'https://example.org/{key}',
                'published_date': yesterday, 'fetched_at': yesterday,
                'summary': 'Evidence-backed cybersecurity jobs expansion', 'direction': 'emerging', 'strength': 1,
                'role_ids': ['cybersecurity-analyst'], 'skill_ids': ['SK011'], 'tagged_by': tagged_by}

    out = tmp_path / 'live_signals.json'
    out.write_text(json.dumps({'schema_version': 1, 'checked_at': None, 'last_successful_at': None,
                               'status': 'not_checked', 'ai_enabled': False,
                               'signals': [signal('earlier', 'claude')]}), encoding='utf-8')
    monkeypatch.setattr(worker, 'OUT', out)
    monkeypatch.setenv('RUNNER_TEMP', str(tmp_path))
    monkeypatch.setenv('SIGNALS_AUTO_AI_ENABLED', '1')
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'synthetic-test-key')
    monkeypatch.setattr(verification, 'durable_storage_ready', lambda: True)  # tmp_path can sit under /tmp

    async def checked_feeds(automatic):
        assert automatic
        with storage.connection() as c:  # what the verifier publishes, plus an unverified row
            storage.insert_signal(c, signal('verified', 'claude-verified'))
            storage.insert_signal(c, signal('keywords', 'keyword'))
        return {'status': 'ok', 'pending': 0, 'rejected': 0}

    monkeypatch.setattr(worker, 'refresh_signals', checked_feeds)
    asyncio.run(worker.main())
    snapshot = json.loads(out.read_text(encoding='utf-8'))
    assert snapshot['ai_enabled'] and snapshot['last_ai_check_day'] == verification.utc_day()
    ids = {row['external_id']: row['tagged_by'] for row in snapshot['signals']}
    assert ids == {'fictional:earlier': 'claude', 'fictional:verified': 'claude'}


def test_v2_pager_configuration_has_independent_pages():
    trends = (ROOT / 'frontend/mockup_source/logic/skill_trends_view.js').read_text(encoding='utf8')
    bindings = (ROOT / 'frontend/mockup_source/logic/page_bindings_view.js').read_text(encoding='utf8')
    page = (ROOT / 'frontend/mockup_source/pages/signals.html').read_text(encoding='utf8')
    # The trend columns are paged once, in page_bindings_view; paging them twice left only page 1 reachable.
    assert 'trRising: trRising.map(c => trCard(c, true))' in trends
    assert 'trDecl: trDecl.map(c => trCard(c, false))' in trends
    assert 'makePager' not in trends
    assert 'rising.slice((risingPage - 1) * 5, risingPage * 5)' in bindings
    assert 'declining.slice((decliningPage - 1) * 5, decliningPage * 5)' in bindings
    assert 'signals.slice((signalPage - 1) * 8, signalPage * 8)' in bindings
    for nav in ('risingNavLabel', 'decliningNavLabel', 'signalNavLabel'):
        assert f'aria-label="{{{{ {nav} }}}}"' in page
    assert 'Review pending evidence' not in page


def test_signals_v2_shows_at_most_five_numbered_pages():
    bindings = (ROOT / 'frontend/mockup_source/logic/page_bindings_view.js').read_text(encoding='utf8')
    assert 'first = Math.max(1, Math.min(current - 2, total - 4)), last = Math.min(total, first + 4)' in bindings
    assert 'length: Math.max(0, last - first + 1)' in bindings


def test_status_does_not_promise_updates_while_disabled():
    bindings = (ROOT / 'frontend/mockup_source/logic/page_bindings_view.js').read_text(encoding='utf8')
    assert 'feedStatus?.schedule_guaranteed === false ? words.unavailable' in bindings
    assert 'feedStatus?.paid_verification_enabled === true' in bindings
