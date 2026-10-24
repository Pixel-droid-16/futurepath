"""SDC template-compatible FuturePath entry point.

This is an adapter, not a second application. It exposes the exact same
FastAPI instance, middleware, routes, and lifespan as backend.app.
Run: python src/main.py
ASGI: uvicorn src.main:app --host 0.0.0.0 --port 5000
"""
from pathlib import Path
import sys

# Support both `python src/main.py` and `python -m src.main`.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.app import app  # noqa: E402


def main() -> None:
    import os
    import uvicorn

    port = int(os.getenv("PORT", "5000"))
    uvicorn.run("backend.app:app", host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
