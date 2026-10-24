"""Password gate for a synthetic-only hackathon demo.

Do not use this shared-password mode as multi-user account authentication:
everyone with the passcode can access the same server-side demo profiles.
"""
import base64
import binascii
import os
import secrets

from fastapi.responses import PlainTextResponse


def public_demo():
    return os.getenv("FUTUREPATH_PUBLIC_DEMO", "").strip().lower() in {"1", "true", "yes"}


def gate_response(request):
    """Return a response if the request must be blocked, otherwise None."""
    if not public_demo():
        return None
    # Public hackathon visitors do not need a passcode by default.\n    # Keep public_demo() enabled so curator and signal-write protections remain active.\n    require_password = os.getenv("FUTUREPATH_DEMO_REQUIRE_PASSWORD", "").strip().lower() in {"1", "true", "yes"}\n    if not require_password:\n        return None\n    password = os.getenv("FUTUREPATH_DEMO_PASSWORD", "")
    if len(password) < 12:
        return PlainTextResponse(
            "Demo is not configured. Set FUTUREPATH_DEMO_PASSWORD to a long secret.",
            status_code=503,
        )
    unauthorized = PlainTextResponse(
        "FuturePath demonstration passcode required.",
        status_code=401,
        headers={"WWW-Authenticate": 'Basic realm="FuturePath Demo", charset="UTF-8"'},
    )
    authorization = request.headers.get("authorization", "")
    scheme, _, encoded = authorization.partition(" ")
    if scheme.lower() != "basic" or not encoded:
        return unauthorized
    try:
        raw = base64.b64decode(encoded, validate=True).decode("utf-8")
        username, separator, supplied = raw.partition(":")
        if not separator or not username or not secrets.compare_digest(supplied, password):
            return unauthorized
    except (ValueError, UnicodeError, binascii.Error):
        return unauthorized
    return None
