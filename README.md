# FuturePath

**SDC Hackathon 2026 · Domain 1 · Career discovery and reskilling**

FuturePath helps students, graduates and working professionals compare their **confirmed** skills with careers, understand evidence-backed skill gaps and explore practical learning paths under different AI-adoption scenarios.

> **Hackathon prototype — synthetic CVs only.** The career scores are educational comparisons, **not** employment probabilities, hiring guarantees or labour-market forecasts. The shared demo is not a private user-account service.

## Team information

| Field | Information |
|---|---|
| Project name | FuturePath |
| Team name | KitaHack |
| Competition domain | Domain 1 |
| Primary SDG track | SDG 4 — Quality Education (target 4.4) |
| Related SDGs | 4 (Quality Education), 8 (Decent Work), 9 (Industry/Innovation), as mapped per career |
| Team leader | CHANTHIRAA CHELVAN PASUPATHY |
| University / institutions | Universiti Teknikal Malaysia Melaka (UTeM) |
| Team members and roles | CHANTHIRAA CHELVAN PASUPATHY (leader), HUA SOON LAI, ADAM BIN AZMI, MUHAMMAD ADAM BIN ROSLAN; individual technical roles to confirm |

## Submission links

| Resource | Link / status |
|---|---|
| GitHub repository | [Pixel-droid-16/futurepath](https://github.com/Pixel-droid-16/futurepath) |
| Live Replit deployment | **Pending publication and live verification** |
| Replit development project | [FuturePath Replit workspace](https://replit.com/@b152610182/futurepath) (may require project access) |
| RunPod endpoint | Configured through `RUNPOD_ENDPOINT_ID`; API key is private |
| Presentation / slide deck | https://drive.google.com/drive/folders/1ZWO4zt3pfn5IgmirVihVO56epyx6NYDD?usp=sharing |
| Demo video | **Team to supply verified link** |
| Official PDF submissions | See [submission/README.md](submission/README.md) |

## Problem

Students and working professionals frequently know some of their abilities but cannot readily explain which careers fit those abilities, which competencies are missing, or how changing AI adoption might affect the work involved. Online advice may lack explicit sources, treat unverified CV claims as proven skills, or offer learning resources unrelated to the person's gaps.

## Solution

FuturePath provides a review-first career exploration journey, combining AI-assisted **skill suggestions** with user confirmation, an explainable scoring engine, dated labour-market evidence, and sourced learning resources. Users retain control over what skills count toward matching; AI suggestions alone are not scored. Moderate and Fast AI modes are **illustrative modelling assumptions**, not predictions.

## Key features

1. **Synthetic CV upload:** TXT, text-based PDF and DOCX extraction. Qwen2.5-3B-Instruct on RunPod suggests catalogue skills; local dictionary matching supplements them. Claude can help with image-only PDFs if configured.
2. **Profile and skill review:** Add/remove proposed skills, assign proficiency and review evidence. An interest quiz supports optional RIASEC matching.
3. **Explainable career rankings:** Skill readiness, dated demand signals, optional interest fit and qualification-related context inform results with visible explanations and uncertainty.
4. **Skill gap analysis and pathway:** Distinguish confirmed, partial and unassessed skills; link gaps to a curated course catalogue and weekly learning schedule.
5. **Evidence-backed Signals and Skills Radar:** Show dated signal sources, rising/declining skills, and contextual sources. Administrator-initiated feed updates are protected.
6. **Moderate/Fast AI scenarios:** Compare explicit AI-adoption assumptions and how supported signals affect careers.
7. **SDG mapping:** Explain links between careers, learning and relevant Sustainable Development Goals.
8. **Versioning and governance prototype:** Snapshot and saved-result APIs exist; some curator/history screens remain incomplete.

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | HTML/CSS/JavaScript with the team's V2 presentation and screen fragments |
| Backend | Python 3.12, FastAPI, Pydantic |
| Data | Local JSON catalogues and SQLite demo profiles / signal runs |
| CV parsing | pypdf, python-docx and text parsing |
| GPU inference | RunPod Serverless with Qwen2.5-3B-Instruct |
| Optional scanned PDF support | Claude API (configured separately) |
| Hosting / development | Replit |
| Testing | pytest and isolated Playwright/Chromium browser regressions |

## Architecture

```text
Browser: V2 pages (Home / Start / Results / Pathway / Signals)
         |
         v
Replit: FastAPI backend + validation + SQLite demo database
         |                   |                   |
         |                   +--> curated data/*.json and Signals
         |                   +--> deterministic matching / scenarios
         |
         +--> RunPod Serverless: Qwen GPU skill suggestions
         +--> Optional Claude PDF provider for scanned documents
         |
         v
Grounded skill proposals -> user reviews -> confirmed skills
         |
         v
Career results -> skill gaps -> learning pathway + SDGs
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for implementation boundaries. The `frontend/index.html` file is generated from `frontend/mockup_source/` and must not be edited as the only source.

## SDC 2026 team and submission status

Our four members have confirmed completion of the mandatory workshops. The team declares use of official SDC sponsor-provided resources (exact sponsor/provider allocation still to verify), no pre-hackathon project work, and no employment-related IP conflicts. The submission PDFs require team-leader review and signature; actual Replit and RunPod proof must use genuine sanitized screenshots. See [submission status](submission/KITAHACK_SUBMISSION_STATUS.md).

The organizer's example uses `src/main.py`. We provide that path as a **thin compatibility entry point** to the existing tested `backend.app:app`, not as a replacement for the modular backend.

## Repository structure

```
├── backend/                     # FastAPI app: API, matching engine, AI providers, signals
│   ├── app.py                   # Creates the app, middleware and signal scheduler
│   ├── engine.py                # Career scoring (skills, demand, interests)
│   ├── routes/                  # One file per API area (careers, signals, CV upload, …)
│   ├── services/                # CV extraction, recommendations, document parsing
│   ├── providers/               # RunPod (Qwen) and Claude adapters, output validation
│   └── signals/                 # Feed fetching, tagging, review queue, GitHub snapshot
├── data/                        # Careers, skills, courses, curated and live signals (JSON)
├── docs/                        # Architecture, release and submission notes
├── frontend/
│   ├── index.html               # Built page served by FastAPI (generated, do not edit)
│   ├── mockup_source/           # Editable page templates and logic
│   └── assets/                  # SDG icons and images
├── runpod_worker/
│   ├── handler.py               # RunPod serverless handler (GPU workload, Qwen 2.5 3B)
│   ├── Dockerfile               # Worker image
│   └── requirements.txt         # Worker dependencies
├── scripts/                     # Frontend build, integrity checks, daily signal worker
├── src/
│   └── main.py                  # Application entry point (wraps backend.app)
├── submission/                  # Required submission documents
│   ├── SDC2026_KitaHack_Preliminary.pdf      # Preliminary submission (to add)
│   ├── SDC2026_KitaHack_TechDeclaration.pdf  # Technology declaration (to add)
│   ├── SDC2026_KitaHack_Replit_POU.pdf       # Replit proof of use (to add)
│   ├── SDC2026_KitaHack_Runpod_POU.pdf       # RunPod proof of use (to add)
│   ├── KITAHACK_SUBMISSION_STATUS.md         # What each PDF still needs
│   └── README.md                             # PDF naming checklist
├── tests/                       # Unit and API tests (pytest)
│   └── browser/                 # Chromium end-to-end journeys
├── .github/workflows/           # CI checks and the daily signals snapshot job
├── .env.example                 # Example environment variables
├── .gitignore
├── .replit                      # Replit run configuration
├── LICENSE                      # Apache 2.0
├── requirements.txt             # Python dependencies
└── README.md
```

The official SDC template uses `src/main.py` and `runpod/handler.py` as **example placeholders**. Our actual equivalents are `backend/app.py` and `runpod_worker/handler.py`. We preserve the working modular structure rather than replace it with the example echo handler.

## How to run

### Replit

Import this repository or open the connected Replit project. The tracked `.replit` configuration runs:

```bash
python -m uvicorn backend.app:app --host 0.0.0.0 --port 5000
```

Install packages with `python -m pip install -r requirements.txt` and check `python scripts/build_frontend.py`. Use **Replit Secrets** (and published-app secrets for deployment) for `RUNPOD_API_KEY`, `RUNPOD_ENDPOINT_ID`, optional `ANTHROPIC_API_KEY` and demo password. Do not paste keys in chat, commit them to Git, or expose them in browser JavaScript. See [docs/REPLIT_RELEASE.md](docs/REPLIT_RELEASE.md).

### Locally

```bash
git clone https://github.com/Pixel-droid-16/futurepath.git
cd futurepath
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
# Configure a private .env from .env.example (never commit .env).
python scripts/build_frontend.py
python -m uvicorn backend.app:app --reload --env-file .env
```

The local default address is http://127.0.0.1:8000/start. Replit's hosted workflow **uses port 5000**, not the local default. Without RunPod or Claude credentials, use the dictionary provider for **fictional** text CVs.

### Alternative SDC-style entry point

```bash
python src/main.py
# or: python -m uvicorn src.main:app --host 0.0.0.0 --port 5000
```

This serves the same FastAPI application as the original Replit command.

### Tests

```bash
python -m pytest -q --tb=short
python -m compileall -q backend
python scripts/build_frontend.py
python scripts/verify_integrity.py
# With a configured Chromium installation:
python -m pytest tests/browser --browser -q --tb=short
```

Browser tests isolate SQLite and stub paid model inference. Passing them does not certify a live GPU response or a published deployment. Record a fresh test summary after each combined change.

## How Replit is used — SDC requirement

The Replit application hosts the FastAPI + V2 website and connects server-side to the RunPod endpoint. Its project workflow, secrets and live preview have been configured and tested with synthetic requests. **The final published deployment and its URL must still be verified before claiming publication.** Proof of use belongs in `submission/SDC2026_<TeamName>_Replit_POU.pdf`.

## How RunPod is used — SDC requirement

`runpod_worker/handler.py` runs Qwen2.5-3B-Instruct on a GPU-backed RunPod Serverless endpoint. The Replit backend sends a bounded prompt to RunPod, validates returned catalogue skill IDs and source quotes, and supplements with local dictionary matches. A prior synthetic Replit → RunPod → Qwen smoke test succeeded; recheck the **current final version** before submission. Proof of GPU inference, endpoint setup and integration belongs in `submission/SDC2026_<TeamName>_Runpod_POU.pdf`. Never include the API key.

## Challenges and learnings

- **Grounded extraction:** Skills need exact quoted CV evidence, a canonical taxonomy and human confirmation. False positives are more damaging than missing suggestions.
- **Hosted security:** A remote browser cannot be treated as localhost; curator and feed-update operations need explicit authorization. The public demo intentionally blocks administrative writes.
- **Source confidence:** Scenario and career signals are team-modelled estimates backed by dated sources, not verified forecasts.
- **Team integration:** Preserve real Git commit history, audit feature changes and run tests after combining the V2 frontend, backend and GPU worker.

## Future improvements

- Private accounts and persistent per-user storage (the current shared demo is **not** suitable for real personal CVs).
- Broader evaluated CV extraction and controlled support for scanned documents.
- Complete evidence curator/history screens and source governance.
- Improved mobile accessibility, loading/error recovery, model monitoring and calibration of scoring.
- Production-grade persistent data store and end-to-end observability.

## Team

| Name | Role | GitHub Username |
|------|------|-----------------|
| CHANTHIRAA CHELVAN PASUPATHY (Leader) | Lead / Backend / RunPod / Replit | [Pixel-droid-16](https://github.com/Pixel-droid-16) |
| HUA SOON LAI | Frontend | [soonlai1129](https://github.com/soonlai1129) |
| ADAM BIN AZMI | Backend / AI | [Maestro05-coder](https://github.com/Maestro05-coder) |
| MUHAMMAD ADAM BIN ROSLAN | Frontend / Backend | [dammnnnnnnnn](https://github.com/dammnnnnnnnn) |

## Submission checklist

See [submission/README.md](submission/README.md) and [docs/SDC_SUBMISSION_CHECKLIST.md](docs/SDC_SUBMISSION_CHECKLIST.md). The team must verify the actual SDC form fields, PDF filenames and any deadlines in the [participant resources folder](https://drive.google.com/drive/folders/1xw7c2aN8N-at8hPEULzkcU76e_FFb0Ef).


## Team and attribution

Add real members and their contribution areas when confirmed. This project combines a teammate's original V2 interface with a modular FastAPI implementation, original and imported curated datasets, and AI-assisted coding. The team is responsible for explaining, reviewing and testing its submission. Keep the real commit history intact.

## License

[Apache License 2.0](LICENSE).
