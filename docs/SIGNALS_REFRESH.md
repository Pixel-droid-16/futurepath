# Signal feed refresh on Replit

FuturePath always displays its stored dated signals. Reloading stored signals is a read-only operation and does **not** fetch Google News, arXiv or other external data.

## Why the old Refresh button returned 403

The `POST /api/signals/refresh` endpoint is intentionally restricted. On a hosted Replit preview, the browser is not localhost. Without an `ADMIN_TOKEN`, the server returns `403`. With an `ADMIN_TOKEN` but no bearer authorization, it returns `401`. Both are correct security checks, not failures in the feed parser.

## Private Replit preview

1. Review and integrate this change from `fix/signals-refresh-admin-ux` after your teammates finish their release-branch work.
2. Add **ADMIN_TOKEN** as a Replit Secret with a new strong random value (at least 24 characters recommended). Do not share it, commit it, or put it in the Agent chat.
3. Restart the development workflow so the backend reads the new secret.
4. On Signals, use **Reload saved signals** to reread current evidence without calling providers.
5. For a live update, use **Admin: refresh live feeds**, enter the token in the one-time prompt, and confirm the potential Claude tagging cost. The page does not store the token in localStorage or application state.
6. The API records a run and shows its status; a run can finish with zero accepted signals or partial feed failures. Review the cited sources before relying on new information.

## Published synthetic demo

With `FUTUREPATH_PUBLIC_DEMO=1`, manual feed refresh is **disabled even with ADMIN_TOKEN**. Judges see the latest stored curated evidence and can reload it, but cannot initiate external requests or incur provider charges. The demo also uses a disposable database, so do not promise that a dev preview refresh persists into production; curate/import a suitable evidence snapshot separately before publishing.

## Acceptance checks

- Confirm `GET /api/signals/refresh-access` reports local, admin, local-only, or demo mode correctly.
- Public mode hides the admin button and blocks direct POST refresh with HTTP 403.
- Remote private preview without ADMIN_TOKEN shows a setup explanation rather than a failing button.
- With ADMIN_TOKEN set, a missing/wrong token returns 401; a valid one permits the existing refresh pipeline.
- Reload stored signals remains available when admin refresh is disabled.
- Run the full backend tests and `python scripts/build_frontend.py` before merging; no live provider calls are needed for regression tests.
