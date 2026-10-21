# FuturePath v2 — Modular architecture

## Motivation

The earlier app had one FastAPI file containing nearly every HTTP endpoint and one large embedded v2 mockup document. This edition separates **editable screen source** and **backend feature logic** while keeping the built HTML and existing backend HTTP contracts unchanged.

## Folders

```text
FuturePath_v2_Modular_Organized/
├── frontend/
│   ├── index.html                  generated output; identical to original v2
│   ├── ai-lab.html                 generated output; identical to original AI Lab
│   ├── mockup_source/
│   │   ├── pages/                   home, intake, results, pathway, signals, about, login
│   │   ├── styles/                  shared v2 theme
│   │   ├── logic/                   separated v2 sample data + view interactions
│   │   ├── ai_lab/                  editable AI Lab HTML, CSS, JavaScript
│   │   └── shell/                   navbar, HTML wrapper, footer
│   ├── assets/ and uploads/        original group images
│   └── support.js, image-slot.js   original custom mockup runtime
├── backend/
│   ├── app.py                      application assembly only
│   ├── catalog.py                  load JSON reference data
│   ├── schemas.py                  request contracts
│   ├── storage.py                  demo SQLite and evidence/profile reads
│   ├── engine.py                   transparent matching and learning priorities
│   ├── scenarios.py                Moderate/Rapid task assumptions
│   ├── ai_providers.py             old import compatibility
│   ├── providers/
│   │   ├── validation.py           evidence-based candidate validation
│   │   ├── claude.py               Anthropic adapter
│   │   └── runpod.py               RunPod adapter
│   ├── services/
│   │   ├── recommendations.py      bridge HTTP to scoring engine
│   │   ├── documents.py            PDF, DOCX and TXT parser
│   │   ├── dictionary.py           offline skill detection
│   │   └── ai_extraction.py        provider selection and fallbacks
│   └── routes/
│       ├── pages.py, meta.py, skills.py, careers.py, learning.py
│       ├── profiles.py, cv_upload.py, ai.py, matches.py, scenarios.py
│       └── radar.py, snapshots.py, curator.py, history.py
├── data/                            original JSON examples
├── runpod_worker/                   original deployment starter
├── tests/                           tests incl. structure/integrity checks
├── scripts/                         HTML builder and integrity verifier
├── docs/                            editing map and explanations
├── backup/PREVIOUS_UNMODIFIED_RELEASE.zip
├── requirements.txt
└── README.md
```

## Backend request graph

Browser → FastAPI `backend/app.py` → matching `backend/routes/<feature>.py` → service → `backend/storage.py`, `backend/engine.py` or `backend/providers/<provider>.py`.

**Existing URLs remain the same**, including `/api/matches`, `/api/scenarios/<career>`, `/api/ai/skills`, `/api/history`, `/api/curator/approve/<snapshot>`, and `/ai-lab`.

## How the mockup is split without changing the screen

`frontend/index.html` is intentionally an *assembled file*. The original mockup uses a custom `<x-dc>` runtime where seven pages share one state component. Splitting it into seven independent standalone HTML documents would break existing navigation. Instead, `scripts/build_frontend.py` concatenates screen fragments and state fragments **in their original order**. This preserves original runtime mechanics while allowing each page to be edited in a separate file.

The source consists of textual fragments, so you should not try to open `frontend/mockup_source/pages/home.html` by itself in Chrome. **Run the builder** and open the main application.

## Long-term backend vs mockup integration

The mockup still uses its own career roles, scenario values and signal text. The FastAPI backend uses a separate 12-role catalogue and synthetic evidence. A future development phase must migrate those mockup displays to fetch actual backend results, while preserving the approved design. That work is intentionally **not** part of this organisation-only refactor.

## Security boundaries

Only FastAPI is allowed to see `ANTHROPIC_API_KEY` and `RUNPOD_API_KEY`. Raw synthetic CV text reaches the API provider on demand and is not stored by this app. Original group v2 'Login' remains only a mockup; the demo curator approval API and global demo profile are unauthenticated and not suitable for public hosting.
