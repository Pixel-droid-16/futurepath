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


def test_refresh_access_api_endpoint_returns_no_credentials(monkeypatch):
    from fastapi.testclient import TestClient
    from backend.app import app
    monkeypatch.delenv('FUTUREPATH_PUBLIC_DEMO', raising=False)
    monkeypatch.setenv('ADMIN_TOKEN', 'fictional-admin-token')
    response=TestClient(app).get('/api/signals/refresh-access')
    assert response.status_code==200
    assert response.json()['mode']=='admin'
    assert 'fictional-admin-token' not in response.text


def test_signals_v2_hides_admin_controls_but_keeps_backend_authorization():
    from pathlib import Path
    root = Path(__file__).resolve().parents[1] / 'frontend'
    html = (root / 'mockup_source' / 'pages' / 'signals.html').read_text(encoding='utf8')
    logic = (root / 'mockup_source' / 'logic' / 'state_and_actions.js').read_text(encoding='utf8')
    assembled = (root / 'index.html').read_text(encoding='utf8')

    # The V2 page is intentionally read-only for visitors, including admins.
    for control in ('Reload saved signals', 'Admin: refresh live feeds',
                    'Review pending evidence', 'Signal updates'):
        assert control not in html
    assert '<sc-if value="{{ adminRefreshAvailable }}"' not in html

    # The read-only page carries no admin client code: no token handling and no refresh calls.
    # The endpoints themselves stay authorised; the tests above check their 401/403 responses.
    assert "'/api/signals/refresh-access'" not in logic
    assert 'Authorization' not in logic
    assert "'/api/signals/refresh'" not in logic

    # Changes to the existing V2 source are reflected in the generated file.
    assert html in assembled
    bindings = (root / 'mockup_source' / 'logic' / 'page_bindings_view.js').read_text(encoding='utf8')
    for nav, label in (('risingNavLabel', 'Rising skills pages'),
                       ('decliningNavLabel', 'Declining skills and jobs pages'),
                       ('signalNavLabel', 'Signal evidence pages')):
        assert f'aria-label="{{{{ {nav} }}}}"' in html
        assert label in bindings
