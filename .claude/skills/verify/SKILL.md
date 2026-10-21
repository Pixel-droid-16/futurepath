---
name: verify
description: How to run FuturePath in isolation and check a change in the real app (pages and API).
---

# Verify FuturePath

Never use the user's own server (port 8000) or `futurepath_demo.sqlite3` directly.

## Isolated server
Copy the DB, point `FUTUREPATH_DB` at the copy, and use a spare port (8002+). The app does not read `.env` itself:
`--env-file .env` loads the Anthropic key, and leaving it out (`env -u ANTHROPIC_API_KEY`) gives the free keyword tagger.

```bash
S=<scratchpad>/verify; mkdir -p $S; cp futurepath_demo.sqlite3 $S/a.sqlite3
FUTUREPATH_DB="$(cygpath -w $S/a.sqlite3)" .venv/Scripts/python.exe -m uvicorn backend.app:app --port 8002 --env-file .env > $S/a.log 2>&1 &
```
Stop it with PowerShell: `Get-NetTCPConnection -LocalPort 8002 -State Listen` then `Stop-Process -Id <OwningProcess> -Force`.

## Gotchas
- After editing `frontend/mockup_source/**`, run `.venv/Scripts/python.exe scripts/build_frontend.py` (it writes `frontend/index.html`).
- Pages are `/`, `/start`, `/results`, `/pathway`, `/signals`, `/about`. Use a background browser tab, read text with `find` / `get_page_text`, and wait about 3 s after navigating for the data to load.
- The automatic signal refresh starts 60 s after start-up when one is overdue, and it uses the Anthropic key if one is loaded. To test it cheaply, move the last `refresh_runs.finished_at` back two days in the DB copy and start the server without the key.
- `SIGNALS_REFRESH_HOURS=0` turns the automatic refresh off.
