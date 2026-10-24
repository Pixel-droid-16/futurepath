"""Public synthetic-demo gate and administrative lockdown."""
import base64

from fastapi.testclient import TestClient
from backend.app import app


def credentials(password):
    raw = base64.b64encode(f"judge:{password}".encode()).decode()
    return {"Authorization": f"Basic {raw}"}


def test_local_site_is_unchanged_without_public_demo(monkeypatch):
    monkeypatch.delenv("FUTUREPATH_PUBLIC_DEMO", raising=False)
    assert TestClient(app).get("/api/skills").status_code == 200


def test_public_demo_is_open_to_visitors_by_default(monkeypatch):
    monkeypatch.setenv("FUTUREPATH_PUBLIC_DEMO", "1")
    monkeypatch.delenv("FUTUREPATH_DEMO_REQUIRE_PASSWORD", raising=False)
    monkeypatch.delenv("FUTUREPATH_DEMO_PASSWORD", raising=False)
    client = TestClient(app)
    assert client.get("/start").status_code == 200
    assert client.get("/api/skills").status_code == 200
    # Opening the pages does not reopen the administrative writes.
    assert client.post("/api/signals/refresh").status_code == 403


def test_required_passcode_needs_secret_before_app_is_exposed(monkeypatch):
    monkeypatch.setenv("FUTUREPATH_PUBLIC_DEMO", "1")
    monkeypatch.setenv("FUTUREPATH_DEMO_REQUIRE_PASSWORD", "1")
    monkeypatch.delenv("FUTUREPATH_DEMO_PASSWORD", raising=False)
    assert TestClient(app).get("/start").status_code == 503


def test_required_passcode_on_api_and_pages(monkeypatch):
    monkeypatch.setenv("FUTUREPATH_PUBLIC_DEMO", "1")
    monkeypatch.setenv("FUTUREPATH_DEMO_REQUIRE_PASSWORD", "1")
    monkeypatch.setenv("FUTUREPATH_DEMO_PASSWORD", "a-demo-secret-password-1234")
    client = TestClient(app)
    assert client.get("/start").status_code == 401
    assert "Basic" in client.get("/api/skills").headers["www-authenticate"]
    assert client.get("/api/skills", headers=credentials("invalid-password")).status_code == 401
    assert client.get("/start", headers=credentials("a-demo-secret-password-1234")).status_code == 200
    assert client.get("/api/skills", headers=credentials("a-demo-secret-password-1234")).status_code == 200


def test_public_demo_disables_curator_and_refresh(monkeypatch):
    monkeypatch.setenv("FUTUREPATH_PUBLIC_DEMO", "1")
    monkeypatch.setenv("FUTUREPATH_DEMO_PASSWORD", "a-demo-secret-password-1234")
    client = TestClient(app)
    hdr=credentials("a-demo-secret-password-1234")
    assert client.post("/api/curator/approve/S1", headers=hdr).status_code == 403
    assert client.post("/api/signals/refresh", headers=hdr).status_code == 403
