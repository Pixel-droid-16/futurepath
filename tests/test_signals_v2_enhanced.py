"""Isolated Signals V2 checks. No real feed traffic or paid models."""
import asyncio
from datetime import date, timedelta
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient

from backend import storage
from backend.app import app
from backend.signals import refresh

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


def test_opt_in_requires_real_key_presence(monkeypatch):
    monkeypatch.setenv('SIGNALS_AUTO_AI_ENABLED', '1')
    assert not refresh.automatic_ai_allowed()
    assert run_check()['accepted'] == 0


def test_verified_synthetic_candidate_publishes_without_admin_token(monkeypatch):
    monkeypatch.setenv('SIGNALS_AUTO_AI_ENABLED', '1')
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'synthetic-test-key')
    monkeypatch.delenv('ADMIN_TOKEN', raising=False)

    class FakeVerified:
        name = 'claude'
        model = 'fictional-test'

        async def tag(self, items, catalog):
            return [
                {'ok': True, 'proposal': {
                    'relevant': True, 'direction': 'emerging',
                    'strength': 3, 'summary': item['title'],
                    'reason': 'Specific labour-market skills shortage',
                    'role_ids': ['cybersecurity-analyst'], 'skill_ids': ['SK011']
                }} for item in items
            ]

    monkeypatch.setattr(refresh, 'ClaudeTagger', FakeVerified)
    outcome = run_check()
    assert outcome['accepted'] == 1 and outcome['pending'] == 0
    api = TestClient(app)
    approved = next(x for x in api.get('/api/signals').json() if x['tagged_by'] == 'claude')
    assert approved['strength'] == 2
    with storage.connection() as connection:
        assert connection.execute(
            "SELECT COUNT(*) FROM signal_review WHERE status='approved'"
        ).fetchone()[0] == 1
        assert connection.execute(
            "SELECT actor FROM signal_review_events ORDER BY id DESC LIMIT 1"
        ).fetchone()[0] == 'automatic-ai'
    assert api.get('/api/signals/status').json()['last_successful_at']


def test_failed_ai_never_affects_active_evidence(monkeypatch):
    monkeypatch.setenv('SIGNALS_AUTO_AI_ENABLED', '1')
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'synthetic-test-key')

    class FailedVerification:
        name = 'claude'
        model = 'fictional-test'

        async def tag(self, items, catalog):
            return [{'ok': False, 'error': 'offline verifier unavailable'} for _ in items]

    monkeypatch.setattr(refresh, 'ClaudeTagger', FailedVerification)
    api = TestClient(app)
    before = api.get('/api/signals').json()
    result = run_check()
    assert result['accepted'] == 0 and result['failed'] == 1
    assert api.get('/api/signals').json() == before


def test_v2_pager_configuration_has_independent_pages():
    root = Path(__file__).resolve().parents[1]
    script = (root / 'frontend/mockup_source/logic/skill_trends_view.js').read_text(encoding='utf8')
    state = (root / 'frontend/mockup_source/logic/state_and_actions.js').read_text(encoding='utf8')
    signals = (root / 'frontend/mockup_source/logic/signal_filters_view.js').read_text(encoding='utf8')
    page = (root / 'frontend/mockup_source/pages/signals.html').read_text(encoding='utf8')
    assert 'risingPage: 1' in state and 'decliningPage: 1' in state
    assert "'risingPage'" in script and "'decliningPage'" in script
    assert 'items.slice((current-1)*5, current*5)' in script
    assert 'visibleEvidence.slice((signalsCurrent-1)*8,signalsCurrent*8)' in signals
    for label in ('Rising skills pages', 'Declining skills pages', 'Signals pages'):
        assert f'aria-label="{label}"' in page
    assert 'Review pending evidence' not in page


def test_signals_v2_shows_at_most_five_numbered_pages():
    root = Path(__file__).resolve().parents[1]
    rising = (root / 'frontend/mockup_source/logic/skill_trends_view.js').read_text(encoding='utf8')
    signals = (root / 'frontend/mockup_source/logic/signal_filters_view.js').read_text(encoding='utf8')
    assert 'Math.min(total, firstVisible + 4)' in rising
    assert 'Math.min(signalPagesTotal, signalPageFirst + 4)' in signals
    assert 'length:lastVisible-firstVisible+1' in rising
    assert 'length:signalPageLast-signalPageFirst+1' in signals


def test_status_does_not_promise_updates_while_disabled():
    root = Path(__file__).resolve().parents[1]
    src = (root / 'frontend/mockup_source/logic/signal_filters_view.js').read_text(encoding='utf8')
    assert 'sigAutoFrequency = feedStatus?.enabled' in src
    assert 'sigHealth = !feedStatus?.enabled' in src
    assert 'automatic_ai_enabled ? uiText.active : uiText.held' in src
    assert 'uiText.schedule.replace' in src


def test_saved_signal_polling_only_when_page_is_visible():
    root = Path(__file__).resolve().parents[1]
    src = (root / 'frontend/mockup_source/logic/state_and_actions.js').read_text(encoding='utf8')
    assert "this.state.page === 'signals' && !document.hidden" in src
    assert 'clearInterval(this._signalsPoll)' in src
    assert '10 * 60 * 1000' in src
