# Where do I edit? — FuturePath v2 file map

## A. Change a *page* (original design kept)

| Screen your friend designed | Edit this source file | Script/logic it uses |
| --- | --- | --- |
| Home + Live Signal Feed | `frontend/mockup_source/pages/home.html` | `logic/home_signal_feed_view.js` |
| Start / Profile intake | `frontend/mockup_source/pages/intake.html` | `logic/intake_skill_view.js`, `logic/intake_sample_skills.js` |
| Results / Ranked careers | `frontend/mockup_source/pages/results.html` | `logic/career_ranking_view.js`, `logic/career_cards.js`, `logic/declining_careers.js` |
| Moderate AI / Rapid AI toggle | `frontend/mockup_source/pages/results.html` | `logic/page_bindings_view.js` (existing mockup controls); **actual API model:** `backend/scenarios.py` |
| Pathway / Training plan | `frontend/mockup_source/pages/pathway.html` | `logic/page_bindings_view.js`; **actual API model:** `backend/engine.py` |
| Signals / Skills Radar | `frontend/mockup_source/pages/signals.html` | `logic/signal_filters_view.js`, `logic/radar_view.js` |
| About / SDG explanation | `frontend/mockup_source/pages/about.html` | `logic/sdg_mapping_view.js`, `logic/sdg_colors.js` |
| Login / Signup mockup | `frontend/mockup_source/pages/login.html` | `logic/page_bindings_view.js` (**UI only, no authentication**) |
| Separate working AI Lab | `frontend/mockup_source/ai_lab/03_document_after_css.html` | `ai_lab/04_interactions.js` |

**After any change under mockup_source, run:** `python scripts/build_frontend.py`. The resulting `frontend/index.html` is compiled from these pieces. Don't edit it manually.

## B. Change common design

- `frontend/mockup_source/styles/v2_theme.css` — Light/dark palette, emerald/ocean/coral/violet accents, shared visual rules and typography.
- `frontend/mockup_source/shell/document_before_css.html` and `document_after_css.html` — HTML document, navbar and shared wrapper; rarely edit.
- `frontend/mockup_source/shell/after_pages.html` and `document_end.html` — Footer and script boundaries; rarely edit.
- `frontend/assets/`, `frontend/uploads/`, `frontend/hero.svg`, `frontend/support.js`, `frontend/image-slot.js` — Original v2 mockup assets and runtime; **do not casually replace**.
- `frontend/app.js` and `frontend/style.css` — Legacy unused prototype files retained untouched for compatibility/reference; editing these will **not** change the original v2 mockup.

## C. Change a real *backend function*

| Function | HTTP route file | Actual calculation / support file |
| --- | --- | --- |
| Career catalogue | `backend/routes/careers.py` | `data/roles.json` |
| Canonical skills | `backend/routes/skills.py` | `data/skills.json` |
| Profile and proficiency | `backend/routes/profiles.py` | `backend/storage.py` |
| CV PDF/DOCX/TXT extraction | `backend/routes/cv_upload.py` | `backend/services/documents.py`, `backend/services/dictionary.py` |
| Claude & RunPod API | `backend/routes/ai.py` | `backend/services/ai_extraction.py`, `backend/providers/{claude,runpod,validation}.py` |
| Matching / suitability | `backend/routes/matches.py` | `backend/engine.py` |
| Related-skill credit and profile fit | `backend/routes/matches.py` | `backend/semantic.py`, `backend/text_match.py`, `data/skill_relations.json` |
| Cached sentence vectors | `backend/routes/matches.py` | `data/semantic_vectors.json`; rebuild with `scripts/build_semantic_vectors.py` |
| Moderate vs Rapid | `backend/routes/scenarios.py` | `backend/scenarios.py`, `backend/engine.py` |
| Skills Radar | `backend/routes/radar.py` | `backend/storage.py` |
| Snapshot status | `backend/routes/snapshots.py` | `backend/storage.py` |
| Curator review | `backend/routes/curator.py` | `backend/storage.py` |
| Learning resource list | `backend/routes/learning.py` | `data/learning_resources.json` |
| Ordered learning priorities | `backend/routes/matches.py` | `backend/engine.py` |
| Saving/previewing/deleting recommendations | `backend/routes/history.py` | `backend/storage.py` |
| SDG mapping | `backend/routes/careers.py` | `data/roles.json` / `backend/engine.py` |
| Website pages and assets | `backend/routes/pages.py` | `frontend/index.html`, `frontend/ai-lab.html` |
| API documentation | Generated automatically by FastAPI | `backend/app.py` registers routers |

## D. How data gets to users

### CURRENT WORKING AI LAB (real backend flow)

`frontend/ai-lab.html` → POST `/api/ai/skills` → `backend/routes/ai.py` → `backend/services/ai_extraction.py` → `backend/providers/claude.py` or `backend/providers/runpod.py` → `backend/providers/validation.py` → browser suggestion review → PUT `/api/profile` → stored confirmed skill.

### CURRENT ORIGINAL V2 HOME (design mockup flow)

`frontend/index.html` → v2 mockup runtime (`support.js`) → embedded screen state / data in `frontend/mockup_source/logic/*.js`. This screen currently **does not request career results or evidence from the Python API**. Reorganisation does not alter that. Its numbers and examples are not actual calculated user recommendations.

### NEXT FUTURE INTEGRATION (not implemented here)

`intake` page → real profile + skill API → real matches API → scenario API → pathways / Radar API → history API. Each interface will reuse your friend's markup; only data bindings will be replaced after your approval.

## E. Rules to prevent accidental breakage

1. Start by making a copy of this project directory.
2. Change **one source file at a time**.
3. Run `python scripts/build_frontend.py` if changing mockup source.
4. Run `python scripts/verify_integrity.py` (passes before edits; after *intentional* UI edits, the hash will differ and should be reviewed, not blindly suppressed).
5. Run `python -m pytest -q`.
6. Keep personal/API secrets out of the project; do not deploy this shared-user demo publicly.
