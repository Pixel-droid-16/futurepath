# FuturePath on Replit

## Release and scope

Use the existing `release/hackathon-2026-final` release, verified at
`23df063daae98040e544edfcd9f9219e32a5da43`. Do not push to or overwrite GitHub
`main`. Preserve the Python FastAPI backend, V2 plain-JavaScript frontend,
datasets, and exact UI. Replit setup does not authorize a stack migration.

This is a synthetic-CV-only SDC Hackathon demo. Every visitor shares the same
profiles; a shared password does not provide per-user privacy. Never upload real
CVs or personal information.

## Run and verify

The **FuturePath** workflow runs:

```sh
python -m uvicorn backend.app:app --host 0.0.0.0 --port 5000
```

Port 5000 maps to external port 80 for Replit's web preview. This differs from
the release checklist's local port 8000 only for preview compatibility.
Python 3.12 and the original import's runtime settings are retained.
Dependencies come from the unchanged `requirements.txt`, installed with
Replit's package manager into its managed Python environment, not a virtualenv.

```sh
SIGNALS_REFRESH_HOURS=0 FUTUREPATH_DB=/tmp/futurepath_tests.sqlite3 python -m pytest -q --tb=short
python -m compileall -q backend
python scripts/build_frontend.py
```

Initial setup: 83 tests passed; compilation passed; the frontend builder reported
UNCHANGED. Browser preview of `/start`, page/API requests, and a fictional TXT
upload using the dictionary provider worked. No live paid provider was called.
Browser output includes existing numeric-template warnings and a missing favicon.
The complete interactive browser flow and live RunPod/Claude extraction have
not been verified on Replit.

`scripts/verify_integrity.py` reports 14 mismatches against its historical
manifest. These same mismatches exist in the exact upstream release commit,
including datasets and older source files. They were not introduced by Replit
setup. Do not silently rewrite the reference hashes to suppress this warning.
Application source, frontend output, datasets, and requirements remain unchanged
from the verified release.

## Environment and publishing

Development environment:

- `FUTUREPATH_PUBLIC_DEMO=0` for the private development preview.
- `SIGNALS_REFRESH_HOURS=0` prevents automatic feed refresh.
- `FUTUREPATH_DB=/tmp/futurepath_development.sqlite3`.

Keep development URL visibility private in Replit's Networking tool; do not
enable public development-URL access. Development does not use the judge
password gate. Do not share it as a public deployment.

Production environment is separately configured:

- `FUTUREPATH_PUBLIC_DEMO=1`.
- `SIGNALS_REFRESH_HOURS=0`.
- `FUTUREPATH_DB=/tmp/futurepath_demo.sqlite3`.

Production build installs the existing requirements and assembles the frontend.
Production runs Uvicorn on `0.0.0.0:5000` without reload. Autoscale is configured
but **nothing has been published by this setup**.

Before publishing, use secure Secrets tooling and confirm published-app scope:

- `FUTUREPATH_DEMO_PASSWORD`: unique random password, at least 12 characters;
  share privately with judges. Without it, public-demo mode returns 503.
- `RUNPOD_API_KEY` and the actual tested `RUNPOD_ENDPOINT_ID`: required for
  Qwen2.5-3B text CV extraction. Do not invent endpoint IDs or substitute models.
- `ANTHROPIC_API_KEY`: optional scanned-PDF provider; select an available
  `ANTHROPIC_MODEL` if needed. This has separate API billing.

Without AI keys, dictionary extraction works; image-only PDFs require the
optional scan provider or manual entry. Never paste credentials into chat, code,
documentation, command arguments, or logs. Do not run paid inference merely
because credentials become available.

Public-demo mode gates all pages/APIs with HTTP Basic authentication (any
nonempty username plus the judge password) and disables curator approval and
manual signal refresh. Existing tests verify fail-closed, unauthorized,
authorized, and blocked-admin cases. Before public release, verify these again
using the real production configuration, and complete an authorized synthetic
RunPod smoke test. Never publish before secrets and checks are ready.

Both `/tmp` databases are disposable and may reset on restart/redeploy.
Persistence is intentionally not promised. See `docs/REPLIT_RELEASE.md` for the
upstream release checklist. No GitHub merge or push is part of Replit setup.
