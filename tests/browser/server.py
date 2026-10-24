"""Disposable browser-test server. Never import this from the production app."""
import os
import socket
import sys

# Set before importing anything that opens storage or loads dotenv.
os.environ["FUTUREPATH_DB"] = sys.argv[1]
os.environ["SIGNALS_REFRESH_HOURS"] = "0"
os.environ["FUTUREPATH_PUBLIC_DEMO"] = sys.argv[3]
os.environ["FUTUREPATH_DEMO_PASSWORD"] = "synthetic-browser-password"
# The public demo is open by default; these two modes exercise the optional passcode gate.
if sys.argv[3] in ("1", "unconfigured"):
    os.environ["FUTUREPATH_DEMO_REQUIRE_PASSWORD"] = "1"
if sys.argv[3] == "signals":
    os.environ["FUTUREPATH_PUBLIC_DEMO"] = "0"
    os.environ["SIGNALS_REFRESH_HOURS"] = "24"
    os.environ["ADMIN_TOKEN"] = "synthetic-browser-admin"
if sys.argv[3] == "unconfigured":
    os.environ["FUTUREPATH_PUBLIC_DEMO"] = "1"
    os.environ["FUTUREPATH_DEMO_PASSWORD"] = ""

# Defense in depth: even an accidentally unstubbed provider cannot leave this host.
_connect = socket.socket.connect


def local_connect(sock, address):
    if isinstance(address, tuple) and address[0] not in ("127.0.0.1", "::1"):
        raise RuntimeError("Browser tests forbid outbound server connections")
    return _connect(sock, address)


socket.socket.connect = local_connect
from backend.services import ai_extraction


async def synthetic_runpod(content, skills):
    assert "Python" in content
    return [{
        "skill_id": "SK005", "name": "Python programming", "excerpt": "Python",
        "method": "runpod AI suggestion (unconfirmed)", "proficiency": None,
    }]


async def forbidden_claude(*args, **kwargs):
    raise AssertionError("Claude must not be called by this text-CV journey")

async def synthetic_scanned_pdf(pdf, pages, skills, include_details=False):
    assert pdf.startswith(b"%PDF-")
    assert pages == [""]
    assert include_details is True
    return {
        "scanned": True,
        "_source_text": "TECHNICAL SKILLS\nPython",
        "candidates": [{
            "skill_id": "SK005", "name": "Python programming", "excerpt": "Python",
            "method": "claude AI suggestion (unconfirmed)", "proficiency": None,
            "evidence": {"page": 1, "source": "page_image"},
        }],
    }


ai_extraction.integration_status = lambda: {
    "runpod_enabled": True, "claude_enabled": sys.argv[3] == "scanned",
}
ai_extraction.runpod_extract = synthetic_runpod
ai_extraction.claude_extract = forbidden_claude
ai_extraction.claude_extract_pdf = (
    synthetic_scanned_pdf if sys.argv[3] == "scanned" else forbidden_claude
)

from backend.app import app

if sys.argv[3] == "signals":
    # Synthetic, already-validated pending fixtures; no feed fetch or paid tagger.
    import json
    from datetime import datetime, timezone, timedelta
    from backend import storage
    stamp = datetime.now(timezone.utc).isoformat()
    with storage.connection() as c:
        run = c.execute("INSERT INTO refresh_runs(started_at,finished_at,status,tagger,pending,trigger) "
                        "VALUES(?,?,'ok','keyword',2,'automatic')", (stamp, stamp)).lastrowid
        for n, title, role, skill in (
            (1, 'Malaysia needs cybersecurity workers', 'cybersecurity-analyst', 'SK011'),
            (2, 'Malaysia expands data analyst hiring', 'data-analyst', 'SK005'),
        ):
            item = {'external_id': f'browser:{n}', 'feed_key': 'browser', 'title': title,
                    'source_name': 'Synthetic evidence fixture', 'source_type': 'news',
                    'url': f'https://example.com/evidence/{n}',
                    'published_date': (datetime.now(timezone.utc)-timedelta(days=1)).date().isoformat(),
                    'snippet': title}
            signal = {**item, 'fetched_at': stamp, 'summary': title,
                      'direction': 'emerging', 'strength': 3,
                      'role_ids': [role], 'skill_ids': [skill],
                      'tagged_by': 'keyword', 'run_id': run}
            c.execute("INSERT INTO signal_review(external_id,run_id,status,signal,source_item,"
                      "validation_notes,created_at) VALUES(?,?,'pending',?,?,?,?)",
                      (item['external_id'], run, json.dumps(signal), json.dumps(item),
                       'Synthetic offline test evidence', stamp))
from backend.routes import cv_upload

# Route selection also checks configuration; never infer it from live secrets.
cv_upload.claude_configured = lambda: sys.argv[3] == "scanned"
import uvicorn

uvicorn.run(app, host="127.0.0.1", port=int(sys.argv[2]), log_level="warning")
