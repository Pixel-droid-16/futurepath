# FuturePath — Current Application Architecture

## Runtime layout

- **Frontend:** `frontend/mockup_source/pages/` holds V2 screen markup; `logic/` holds screen and interaction code; `styles/` contains theme styling. Run `python scripts/build_frontend.py` to regenerate `frontend/index.html`.
- **FastAPI:** `backend/app.py` mounts feature-specific routers from `backend/routes/`. Core matching lives in `backend/engine.py` and `backend/services/recommendations.py`.
- **Data:** `data/skills.json` (canonical catalogue), `data/roles.json` (career requirements), `data/signals.json` (dated seed evidence), `data/courses.json` and `data/extra_courses.json` (pathway resources).
- **Storage:** SQLite stores the demo profile(s), recommendations and signal refresh runs. It is shared, without personal account isolation; Replit's `/tmp` demo database is disposable.
- **AI:** The text-CV provider path calls RunPod Serverless Qwen2.5-3B-Instruct using the server-side API key. A dictionary supplement uses grounded keyword matches; Claude can read image-only PDFs when configured. The RunPod worker source is `runpod_worker/handler.py` and is a real GPU inference adapter, **not** the SDC example echo handler.
- **Testing:** `tests/` contains deterministic backend checks and `tests/browser/` has isolated Playwright journeys. Model providers are mocked in the browser suite, so a separate live synthetic RunPod smoke test is required.

## Data flows

```text
Fictional CV (TXT/DOCX/text PDF) or manual profile
  -> backend/routes/cv_upload.py
  -> backend/services/documents.py
  -> providers/runpod.py -> RunPod endpoint / Qwen GPU (when configured)
       \-> providers/claude.py for scanned PDF (when configured)
       \-> dictionary fallback/supplement
  -> grounded evidence + canonical skills + review-only profile hints
  -> user confirms/removes skills and selects proficiency
  -> backend/services/recommendations.py -> backend/engine.py
  -> explainable scores, gaps, scenarios, SDGs
  -> learning pathway with source links
```

No proposed AI skill counts toward career scoring until user confirmation. Scanned files without a supported image-capable provider should receive an explicit error, not fabricated extraction.

## Signals and scenario governance

The baseline `data/signals.json` contains dated signal entries. `backend/signals/` manages feed parsing, tagging, guardrails, recency weighting and auditable refresh runs. Moderate/Fast modes apply documented hypothetical changes to AI-related signal importance rather than forecasting real job losses. Automatic feed checks can be disabled with `SIGNALS_REFRESH_HOURS=0`. Public-demo mode disables manual updates to prevent visitors from triggering external costs or modifying evidence.

The evidence-refresh and saved-recommendation version APIs exist but do not imply the complete curator approval and history interface is deployed. Score explanations must distinguish direct observations from modelling choices.

## Replit and RunPod

Replit's checked-in `.replit` currently runs FastAPI on **port 5000** and defines an Autoscale deployment. The development preview may run without the public demo password; production mode requires the configured strong password for a synthetic-only shared demonstration. RunPod credentials stay in Replit Secrets. For production verification follow `docs/REPLIT_RELEASE.md`, and record proof-of-use separately in `submission/`.

## Security and limits

- No real CVs or personally identifiable records in the shared hackathon instance.
- No public access to API keys. No keys embedded in the frontend.
- Published demo login is a **shared password gate**, not identity/account-based authentication.
- Stored example profiles are shared, and `/tmp` is ephemeral.
- Admin curator and live-feed actions are forbidden in the public-demo configuration.
- Live AI provider reliability, source confidence, costs and authentication must be verified separately before claims of production readiness.
