"""Remote snapshot safety, no network or paid models."""
from datetime import date, datetime, timedelta, timezone
import httpx
import pytest
from fastapi.testclient import TestClient
from backend import storage
from backend.app import app
from backend.routes import signals as signal_routes
from backend.signals import snapshot

def example():
    return {
        'external_id':'fictional:verified-source','feed_key':'fictional',
        'title':'Malaysia cybersecurity jobs expand','source_name':'Fictional source',
        'source_type':'news','url':'https://example.org/article',
        'published_date':date.today().isoformat(),'fetched_at':date.today().isoformat(),
        'summary':'Evidence-backed cybersecurity jobs expansion',
        'direction':'emerging','strength':2,'role_ids':['cybersecurity-analyst'],
        'skill_ids':['SK011'],'tagged_by':'claude'
    }

def test_remote_validator_keeps_only_structured_verified_sources():
    approved=example()
    assert snapshot.validate_signal(approved)['strength']==2
    for variant in ({**approved,'tagged_by':'keyword'},
                    {**approved,'strength':5},
                    {**approved,'role_ids':['invented']},
                    {**approved,'url':'http://localhost/article'},
                    {**approved,'direction':'increasing'}):
        assert snapshot.validate_signal(variant) is None

def test_snapshot_document_rejects_invalid_schema_and_deduplicates():
    row=example()
    good={'schema_version':1,'checked_at':None,'status':'ok',
          'last_successful_at':None,'ai_enabled':True,'signals':[row,row]}
    rows,meta=snapshot.validate_document(good)
    assert len(rows)==1 and meta['ai_enabled']
    with pytest.raises(ValueError):
        snapshot.validate_document({**good,'schema_version':2})

def test_enabled_by_default_and_no_network_when_disabled(monkeypatch):
    monkeypatch.delenv('SIGNALS_REMOTE_SNAPSHOT_ENABLED',raising=False)
    assert snapshot.enabled()
    monkeypatch.setenv('SIGNALS_REMOTE_SNAPSHOT_ENABLED','0')
    monkeypatch.setattr(snapshot.httpx,'get',lambda *a,**kw: pytest.fail('network called'))
    assert snapshot.read_snapshot()==([],None)


def serve_snapshot(monkeypatch, tmp_path, **meta):
    """Serve one verified snapshot row (dated yesterday) through the real API, without network."""
    monkeypatch.setattr(storage, 'DB', tmp_path / 'snapshot-api.sqlite3')
    monkeypatch.setenv('FUTUREPATH_PUBLIC_DEMO', '0')
    storage.init()
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    row = snapshot.validate_signal({**example(), 'published_date': yesterday, 'fetched_at': yesterday})
    served = ([row], {'checked_at': None, 'last_successful_at': '2026-10-24T21:35:52+00:00', 'status': 'ok',
                      'ai_enabled': False, 'last_ai_check_day': None, 'external_scheduler': True,
                      'verified_count': 1, **meta})
    monkeypatch.setattr(snapshot, 'read_snapshot', lambda: served)
    monkeypatch.setattr(signal_routes, 'read_snapshot', lambda: served)
    return TestClient(app)


def test_snapshot_rows_are_labelled_ai_validated(monkeypatch, tmp_path):
    api = serve_snapshot(monkeypatch, tmp_path, ai_enabled=True)
    row = next(s for s in api.get('/api/signals').json() if s['external_id'] == 'fictional:verified-source')
    assert row['provenance'] == 'live_ai_validated'
    assert row['provenance_label'] == 'AI-validated live source'
    assert row['verification_status'] == 'ai_and_guardrails_passed'


def test_status_reports_recent_github_ai_verification(monkeypatch, tmp_path):
    today = datetime.now(timezone.utc).date()
    api = serve_snapshot(monkeypatch, tmp_path, ai_enabled=True)
    assert api.get('/api/signals/status').json()['external_ai_verification'] is True
    # A same-day re-run skips paid verification; the verified day still counts.
    api = serve_snapshot(monkeypatch, tmp_path, last_ai_check_day=today.isoformat())
    assert api.get('/api/signals/status').json()['external_ai_verification'] is True
    api = serve_snapshot(monkeypatch, tmp_path, last_ai_check_day=(today - timedelta(days=3)).isoformat())
    assert api.get('/api/signals/status').json()['external_ai_verification'] is False


def test_unexpected_fetch_error_keeps_last_evidence(monkeypatch):
    # CI and the browser server block sockets with RuntimeError; that must never break /api/signals.
    monkeypatch.setenv('SIGNALS_REMOTE_SNAPSHOT_ENABLED', '1')
    monkeypatch.setitem(snapshot._cache, 'time', 0.0)
    monkeypatch.setitem(snapshot._cache, 'signals', [])
    monkeypatch.setitem(snapshot._cache, 'meta', None)
    def blocked(*args, **kwargs):
        raise RuntimeError('network blocked')
    monkeypatch.setattr(snapshot.httpx, 'get', blocked)
    assert snapshot.read_snapshot() == ([], None)
