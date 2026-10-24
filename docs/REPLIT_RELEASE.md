# Replit release checklist — FuturePath

This is a **synthetic-data-only hackathon demo**. Use the reviewed `release/hackathon-2026-final` branch to configure and test, then merge the approved pull request into `main` and publish `main` as the final submission source.

## 1. Import from GitHub

In Replit, create/import a project from `https://github.com/Pixel-droid-16/futurepath`. Work from the release branch during verification, not an unreviewed historical main build. Importing does not automatically grant access to RunPod keys.

Install dependencies using:

```bash
python -m pip install -r requirements.txt
```

Build the V2 frontend (already tracked but verify consistency):

```bash
python scripts/build_frontend.py
```

## 2. Web server

The tracked `.replit` configuration starts FastAPI with:

```bash
python -m uvicorn backend.app:app --host 0.0.0.0 --port 5000
```

Expose **local port 5000** for the Replit web server. Do not deploy `uvicorn --reload`. For publishing, choose a web-app deployment such as Autoscale or Reserved VM, not static hosting or a scheduled task.

## 3. Replit Secrets / published-app secrets

Set in the Replit Secrets UI, **not** inside source files:

| Secret | Value |
| --- | --- |
| `FUTUREPATH_PUBLIC_DEMO` | `1` — opt in to shared-password access |
| `FUTUREPATH_DEMO_PASSWORD` | A unique random password of at least 12 characters; share privately with judges |
| `RUNPOD_API_KEY` | Server-side RunPod API key |
| `RUNPOD_ENDPOINT_ID` | The actual tested Qwen2.5-3B endpoint ID |
| `ANTHROPIC_API_KEY` | Optional scanned-PDF fallback; involves separate API billing |
| `ANTHROPIC_MODEL` | Optional Claude model available to your account |
| `SIGNALS_REFRESH_HOURS` | `0` for a reproducible demo, avoiding background spend |
| `FUTUREPATH_DB` | `/tmp/futurepath_demo.sqlite3` for a disposable synthetic-only demo |

Remember: development secrets and **published app** secrets can be different. Confirm the values are set for the published deployment and never log or paste them publicly.

`FUTUREPATH_PUBLIC_DEMO=1` makes every website page and API require the shared password via the browser's HTTP Basic prompt. Without a valid secret, the app returns 503 (fail closed); it does **not** silently publish profiles. The demo password is **not per-user authentication**: everyone using it shares the same synthetic profiles. The public demo **disables curator approval and manual feed refresh**; test those locally with synthetic snapshots instead.

The `/tmp` SQLite example is disposable and may reset after a restart/redeploy. It is not durable production storage. Replit persistence must be separately configured and verified before promising users their data is saved indefinitely. Never use real CVs or personal data on this shared server.

## 4. Required tests before merging

```bash
python -m pytest -q --tb=short
python -m compileall -q backend
python scripts/build_frontend.py
git status --short
```

### Automated browser regressions (no paid inference)

Install the requirements above, then provide Chromium. Replit's configured
`playwright-driver` supplies it; elsewhere run `python -m playwright install chromium`
(and install your OS's required browser libraries). To use an existing binary,
set `PLAYWRIGHT_CHROMIUM_EXECUTABLE` to its path.

```bash
python -m pytest tests/browser --browser -q --tb=short
```

These tests are opt-in: the ordinary pytest command reports them as skipped.
The browser command must pass before merging; a missing browser is an error,
not a silent skip. It exercises the tracked `frontend/index.html` and real FastAPI
routes, without rebuilding or changing the UI.

Coverage includes manual profile creation, a fictional TXT upload through the
existing file control, unconfirmed skill safeguards, proficiency and removal,
all 18 quiz answers and skipping the quiz, Moderate/Rapid ranking (the UI labels
Rapid as “Fast”), pathway navigation, two saved people and switching, refresh
on results/pathway/signals/about, a 390px mobile journey, light/dark toggling,
and public-demo missing/wrong/correct password and blocked administration.
The native HTTP Basic prompt cannot be typed into by Playwright: browser-context
credentials test successful login, and HTTP responses test the challenge.

Each test starts its own server on a temporary loopback port with a new SQLite
database under pytest's temporary directory. No development database or shared
profile is modified. The server receives only runtime environment settings,
not deployment secrets. Qwen is stubbed at the provider boundary (the upload,
parsing, dictionary supplementation, profile saving and matching remain real);
Claude calls fail explicitly, scheduled feeds are disabled, and outbound server
connections are blocked. Tests never incur RunPod/Claude charges.

The unchanged UI requires its pinned React, ReactDOM and Babel scripts from
unpkg; allow access to those URLs when running the suite. Other external assets
are blocked in the journey fixture. Browser checks do not prove real provider
availability, native PDF file-picker behavior, or production deployment health.

Browser smoke test with synthetic CV:

1. Open the protected `/start` URL; without a password expect a 401 prompt.
2. Enter the judge passcode and confirm `/api/skills` loads.
3. Upload a fictional text-based PDF, DOCX, or TXT through `/api/extract`, using RunPod.
4. Confirm the UI reports Qwen and dictionary **separately**, highlights exact CV quotes and proposes project/education details for review.
5. Remove a proposed skill; choose Basic, Working, or Strong for remaining skills. Verify that no unconfirmed suggestion is automatically scored.
6. Complete/skip the interest quiz; verify both Moderate and Rapid results and `/pathway` links.
7. Confirm `/signals` and `/about` work, and the curator/refresh APIs are blocked in public-demo mode.
8. Refresh the browser on `/results`, `/pathway`, and `/signals` to verify deep links.
9. Check both light and dark themes, mobile width, API errors, and the release logs.

**Do not merge into `main` until these checks pass.** Check the published Replit URL independently: local Uvicorn and unit tests do not prove that deployment is healthy.

## 5. Known limitations

- Qwen inference may return zero accepted candidates; dictionary supplementation is a separate method, not Qwen reasoning.
- Scanned PDFs currently rely on the configured Claude PDF provider; no local OCR worker is included.
- Experience-derived proficiency is **never automatic**. The user confirms the skills and strengths.
- Suggested education and project achievements are review-only; a degree in progress must not be counted as completed.
- Evidence and signal governance exist as prototype APIs; not all curator/history screens are complete.
- The dataset and matching scores are educational estimates, not verified job prospects, probabilities, or promises.


## Submission version checklist

Confirm the deployment is built from the GitHub `main` commit currently approved by the team; do not assume a private Replit preview is a published link. Record both the full commit SHA and deployment URL in the SDC proof-of-use form. See `submission/README.md` for the official PDF naming checklist.
