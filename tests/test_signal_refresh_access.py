"""Authorization-aware Signals refresh capability; no paid feed requests."""
from types import SimpleNamespace
from fastapi import HTTPException
import pytest

from backend.routes.signals import refresh_access, authorise


def fake_request(host='remote.proxy', authorization=''):
    return SimpleNamespace(
        client=SimpleNamespace(host=host),
        headers={'authorization': authorization},
    )


def test_remote_preview_without_admin_token_never_offers_refresh(monkeypatch):
    monkeypatch.delenv('FUTUREPATH_PUBLIC_DEMO', raising=False)
    monkeypatch.delenv('ADMIN_TOKEN', raising=False)
    remote=refresh_access(fake_request())
    assert remote['mode']=='local_only' and not remote['can_refresh']
    assert 'ADMIN_TOKEN' in remote['message']
    with pytest.raises(HTTPException) as e:
        authorise(fake_request())
    assert e.value.status_code==403


def test_local_development_still_allows_refresh_without_admin_token(monkeypatch):
    monkeypatch.delenv('FUTUREPATH_PUBLIC_DEMO', raising=False)
    monkeypatch.delenv('ADMIN_TOKEN', raising=False)
    local=refresh_access(fake_request('127.0.0.1'))
    assert local['mode']=='local' and local['can_refresh']
    assert not local['requires_token']
    assert authorise(fake_request('127.0.0.1')) is None


def test_hosted_admin_refresh_requires_correct_bearer_token(monkeypatch):
    monkeypatch.delenv('FUTUREPATH_PUBLIC_DEMO', raising=False)
    monkeypatch.setenv('ADMIN_TOKEN', 'fictional-admin-token')
    status=refresh_access(fake_request())
    assert status['mode']=='admin' and status['can_refresh'] and status['requires_token']
    assert 'fictional-admin-token' not in str(status)
    with pytest.raises(HTTPException) as e:
        authorise(fake_request())
    assert e.value.status_code==401
    with pytest.raises(HTTPException) as e:
        authorise(fake_request(authorization='Bearer incorrect'))
    assert e.value.status_code==401
    assert authorise(fake_request(authorization='Bearer fictional-admin-token')) is None


def test_public_demo_disables_refresh_even_with_admin_token(monkeypatch):
    monkeypatch.setenv('FUTUREPATH_PUBLIC_DEMO', '1')
    monkeypatch.setenv('ADMIN_TOKEN', 'fictional-admin-token')
    status=refresh_access(fake_request(authorization='Bearer fictional-admin-token'))
    assert status['mode']=='demo' and not status['can_refresh']
    assert not status['requires_token']
    with pytest.raises(HTTPException) as e:
        authorise(fake_request(authorization='Bearer fictional-admin-token'))
    assert e.value.status_code==403
