"""Disposable browser-test server. Never import this from the production app."""
import os
import socket
import sys

# Set before importing anything that opens storage or loads dotenv.
os.environ["FUTUREPATH_DB"] = sys.argv[1]
os.environ["SIGNALS_REFRESH_HOURS"] = "0"
os.environ["FUTUREPATH_PUBLIC_DEMO"] = sys.argv[3]
os.environ["FUTUREPATH_DEMO_PASSWORD"] = "synthetic-browser-password"
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


ai_extraction.integration_status = lambda: {
    "runpod_enabled": True, "claude_enabled": False,
}
ai_extraction.runpod_extract = synthetic_runpod
ai_extraction.claude_extract = forbidden_claude
ai_extraction.claude_extract_pdf = forbidden_claude

from backend.app import app
import uvicorn

uvicorn.run(app, host="127.0.0.1", port=int(sys.argv[2]), log_level="warning")
