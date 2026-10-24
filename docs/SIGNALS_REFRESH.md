# Signals: daily checks and administrative evidence review

## Read-only use

Reload saved signals rereads SQLite and never fetches feeds or calls an AI.
`GET /api/signals/status` reports last checked, pending count, next due and run
status without authorization or scheduler mutation. Pending and rejected items
are not returned as active signals and never affect career scores, rankings,
Skills Radar, skill trends, scenarios or What changed.

## Private development: best-effort every 24 hours

Set `SIGNALS_REFRESH_HOURS=24` in **Development** and restart the existing server.
The default is 0/off. First activation waits a full interval: no immediate fetch.
The next due time is stored in the configured SQLite database. A restart preserves
a future due time; an overdue restart defers another full interval rather than
performing a surprise catch-up fetch. Disabling then re-enabling also waits a full
interval. Successful or failed checks schedule the next attempt 24 hours later;
there is no burst retry or missed-day catch-up. Startup has an additional 60-second
grace period and the scheduler checks while the workflow remains running.

Automatic checks always instantiate the deterministic **KeywordTagger**, even
when ANTHROPIC_API_KEY exists. They never call Claude or RunPod. Configured public
RSS/dataset endpoints are fetched, source/link/date metadata is validated,
duplicates and near-duplicates are excluded, catalogue IDs and numeric claims are
checked, and candidates enter an auditable **pending review** queue.

`ADMIN_TOKEN` is not needed on every scheduled check: the internal scheduler does
not invoke an authenticated browser action. It never auto-approves evidence.

## Administrator approval

Use **Review pending evidence** in Signals, enter the existing ADMIN_TOKEN in the
one-time prompt, inspect source, date, summary and validation notes, then approve
or reject. Each action requests bearer authorization. The action's short-lived
local token can authorize its follow-up queue read, but is never saved in
application state, localStorage, sessionStorage, a URL or logs. Optional decision
reasons are audited; do not enter credentials or personal information as reasons.

- `GET /api/signals/review?status=pending|approved|rejected|all` is protected.
- `POST /api/signals/review/{id}/approve` revalidates stored provenance and applies
  the signal, review decision and audit event in a single SQLite transaction.
- `POST /api/signals/review/{id}/reject` records a terminal rejection without
  changing active evidence. Repeated/conflicting decisions return 409.
- All three require ADMIN_TOKEN bearer authorization, **including localhost**.
  There is no review-token generation, unauthenticated curator shortcut, or
  automatic publication. Queue reads are bounded to 200 items.

Already-active curated and previously approved/imported evidence is preserved.
This gate applies to newly fetched evidence, not retroactive removal of existing
signals. Review history and timing survive process restart only while the same
SQLite file survives. Audit identifies the administrator role, not an individual
person; the existing shared administrator credential is unchanged.

## Manual refresh

**Admin: refresh live feeds** remains an explicit authorized action with a cost
confirmation. Its original default tagger semantics remain: when Claude is
configured, manual tagging may incur Claude charges. It does not call RunPod.
Manual refresh uses exactly the same pending-review gate and does **not** change
rankings until approval. Remote access requires the existing ADMIN_TOKEN bearer;
the historical localhost-only manual refresh capability is unchanged.

## Production remains restricted

Keep **Production** `FUTUREPATH_PUBLIC_DEMO=1` and `SIGNALS_REFRESH_HOURS=0`.
Public-demo mode independently disables background checks, manual refresh, queue
access and approve/reject operations, even if an admin token or positive interval
is present. The existing demo password must remain configured. Saved evidence can
still be reloaded behind the password gate.

Replit Autoscale can sleep. An in-process timer cannot guarantee a daily run on a
sleeping instance. The existing `/tmp` SQLite files are separate for development
and production and are not durable shared storage. **This is not guaranteed
unattended production refresh.** A separately approved always-on/scheduled job and
durable shared storage are prerequisites for that promise; do not enable public
demo fetching or silently change deployment/storage for it.

## Verification

Use offline mock transports and disposable SQLite for backend checks. Chromium
tests use synthetic pending evidence, fictional admin credentials, and outbound
blocking. Test delayed startup/restart/disable, keyword-only automatic tagging,
source validation/deduplication, pending/rejected score isolation, authenticated
atomic approval, and public-demo rejection. Build the generated frontend from V2
fragments, check parity, compile and verify the reviewed integrity manifest.
These tests must not fetch live feeds, call paid models, or modify shared profiles.
