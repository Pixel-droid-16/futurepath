# FuturePath

Career exploration and reskilling prototype for **SDC Hackathon 2026 — Domain 1**.

We're building FuturePath to help students, graduates and working professionals understand how their current skills relate to different careers, what they might need to learn next, and how AI adoption could change the work involved.

The project currently uses our team's **v2 interface design** with a Python backend. It is a hackathon prototype, not a live labour-market forecasting service.

## Try it locally

**New to the project? Follow [SETUP.md](SETUP.md)** for step-by-step setup on Windows, macOS or Linux, including the `.env` file and troubleshooting. The short version, inside an activated virtual environment:

```bash
python -m pip install -r requirements.txt
python -m uvicorn backend.app:app --reload --env-file .env
```

`--env-file .env` loads your private keys (see `.env.example`). Without it, Claude features fall back to keyword matching.

Open:

- **Website:** http://127.0.0.1:8000
- **API documentation:** http://127.0.0.1:8000/docs

If port 8000 is in use, stop the previous local server before starting this one.

## What you can try today

The main flow is one page, **/start**, in four steps:

```text
1 Choose start      ->  2 Check profile        ->  3 Interest quiz      ->  4 Results
CV or form              edit + approve skills      18 RIASEC questions      matches, scenarios, radar
```

1. **Choose start:** upload a fictional CV (PDF), or fill a short form (role, experience, qualification, languages, skills, goals).
2. **Check profile:** set each skill to Basic (2/5), Working (3/5) or Strong (4/5), remove or add skills, set study hours per week, then tick the approval box.
3. **Interest quiz (optional):** 18 Holland RIASEC questions. They add a 20% interest-fit score and never hide a career.
4. **Results:** every career in `data/roles.json` ranked by a visible formula, `0.55 × skills + 0.45 × demand` (or `0.45 / 0.35 / 0.20` with interest fit), with a ± range from signal confidence, a Moderate/Fast AI disruption toggle, weight sliders, **What changed**, and a Future Skills Radar of rising and declining careers. **See pathway** opens a course plan built from your weekly study hours.
**Saved people:** every finished Start run is saved as its own person ("Person 1", "Person 2", … or the name you give). **+ Analyse a different CV** starts a new person without overwriting anyone; the **Saved people** buttons on Results, or the list on Start, switch back to anyone's results. **Delete** in the Start list removes a person after you confirm (the original shared profile is reset instead). New people get the lowest unused "Person N" name. The browser remembers who you were last viewing. There are no accounts, so everyone using the same server sees the same list: use fictional CVs.

5. Open **/signals** to see **Rising skills** and **Declining skills & jobs** cards (each with a 3-year signal trend line, signal count, source, date and SDGs; declining also lists jobs that WEF and ILO reports name as declining), then the dated, sourced signals behind them. Press **Refresh signals** to pull new items from live feeds.
6. CV reading uses Qwen through RunPod for text-based CVs when configured; Claude can handle scanned PDFs; grounded dictionary suggestions supplement the model. Upload results require user confirmation. To test provider keys, run the targeted synthetic extraction checks.

The Moderate/Rapid scenarios use explicit, hand-authored assumptions about task change and human oversight. **They are not measured probabilities, job-loss forecasts or verified labour-market predictions.** Score adjustments are intentionally bounded; the more visible differences are in task impacts and learning priorities.

## Current implementation status

| Area | Current state |
| --- | --- |
| Start flow (choose, check, quiz, results) | Connected end to end |
| Career matching | Python API connected to Results |
| Moderate/Rapid scenario comparison | Backend-connected on Results |
| Interest fit | RIASEC quiz against O*NET interest profiles for every career (sources in data/roles.json) |
| Learning pathway | /pathway, every checked course (free, low-cost, HRD Corp claimable) with alternatives per step; weeks from study hours |
| Skill taxonomy and role catalogue | Local JSON datasets |
| AI-trend signal layer | 36 curated report signals plus refreshable Google News, arXiv and Anthropic Economic Index feeds; Claude tagging with keyword fallback |
| Trends score | Computed from signals (strength, recency, caps), with cited sources and confidence |
| Learning pathway courses | 81 checked courses covering 79 of the 81 required skills; placeholders only where no checked course exists |
| CV skill extraction | Qwen2.5-3B-Instruct via RunPod for text PDFs/DOCX/TXT, Claude for scanned PDFs, dictionary supplement; all skills reviewed before use |
| Home signal feed | Latest stored signals |
| Home skills radar | Illustrative data and interface |
| Saved people | Many profiles (`/api/profiles`), switchable on Results; no accounts or access control |
| Login and user accounts | Mockup only; no real authentication |
| Evidence approval and recommendation history | Backend demo APIs exist; v2 screens are not fully connected |
| Claude API | Integration code included; live calls not verified for this deployment |
| RunPod GPU | Live synthetic extraction verified on the release branch (2026-10-24); production Replit connectivity still requires testing |

**Production demo:** See [docs/REPLIT_RELEASE.md](docs/REPLIT_RELEASE.md) for password protection, run commands, and verification. Never upload personal CVs to the public/shared hackathon demo.

The prototype uses **synthetic CV/profile information**. Trend signals are real, dated sources, but which careers and skills they link to, and their strength, are modelling judgements. Please don't treat the displayed career scores as employment probabilities.

## Project structure

```text
backend/
  app.py                 FastAPI entry point
  routes/                Endpoints grouped by feature
  services/              Recommendation, document and extraction logic
  providers/             Claude, RunPod and output validation
  engine.py              Career scoring and skill-gap calculations
  signals/               Trend signal layer: feeds, tagging, guardrails, refresh, demand formula
  scenarios.py           Moderate and Rapid AI assumptions
data/
  roles.json             Career requirements
  skills.json            Canonical skill catalogue
  signals.json           36 curated trend signals (imported from LaluanKu)
  declining_jobs.json    Declining jobs for the Signals page cards, each linked to the curated reports that name it
  courses.json           Checked courses for pathways (imported from LaluanKu)
  extra_courses.json     56 more checked courses, added by hand (79 of 81 required skills covered)
  snapshots.json         Prepared evidence versions (fallback Trends values)
  learning_resources.json  Placeholders for skills without a checked course
frontend/
  index.html             Generated v2 application page
  mockup_source/
    pages/               Editable v2 screen markup
    logic/               Screen-specific interaction code
    styles/              Theme styles
runpod_worker/           Example GPU inference worker
scripts/                 Frontend build and integrity checks
tests/                   Automated checks
docs/                    Architecture, edit locations and demo walkthrough
```

**Editing the UI:** Change the source fragments under `frontend/mockup_source/`, then regenerate `frontend/index.html`:

```bash
python scripts/build_frontend.py
```

For a guide to the Results scenario connection, see [docs/SCENARIO_CONNECTION_GUIDE.md](docs/SCENARIO_CONNECTION_GUIDE.md). For other edit locations, see [docs/WHERE_TO_EDIT.md](docs/WHERE_TO_EDIT.md).

## Checks

Run from the repository root:

```bash
python scripts/verify_integrity.py
python -m pytest -q
```

The integrity script checks preserved design assets. The tests cover parts of the backend and its API adapters; **passing them is not the same as verifying the whole experience in a browser**.

## Trend signal layer

Every Trends score comes from dated, sourced signals, a design ported from the team's LaluanKu project:

- **Baseline:** 36 curated signals from reports and news (WEF, ILO, MOSTI, DOSM, Anthropic Economic Index and others), checked on 2026-10-20. `scripts/import_laluanku_seed.py` maps LaluanKu's careers and skills to ours; links to careers we don't have are dropped, never guessed.
- **Feeds** (`backend/signals/feeds.py`): Google News searches on AI, green jobs, digital talent and skills policy in Malaysia; arXiv research on generative AI and labour markets; new Anthropic Economic Index releases on Hugging Face.
- **Refresh** (`POST /api/signals/refresh`, or the button on /signals): fetch feeds, skip items already seen and near-duplicate headlines, tag new items, apply guardrails, store. Every item and run is kept in an audit trail with its reason.
- **Tagging:** Claude decides relevance and direction and links each item only to career and skill IDs in our catalogue. Without `ANTHROPIC_API_KEY`, a keyword tagger takes over. Each signal shows which method tagged it.
- **Guardrails:** unknown IDs are dropped; items with no valid link are rejected; a summary with a number not in the source is replaced by the headline; feed items are capped at strength 3.
- **Trends formula** (`backend/signals/demand.py`): ±strength × 0.5^(age in days / 365); full weight for a signal naming the career, reduced weight through a required skill; skill-path signals capped at ±2 and feed signals at ±3 per career; mapped to 0–100 where 50 means no net signal.

Refreshing is allowed from this computer only, unless you set `ADMIN_TOKEN`, in which case requests need `Authorization: Bearer <token>`.

While the server runs, signals also refresh **automatically once a day** (`backend/signals/schedule.py`): a full day after the last finished run, a minute after start-up if one is overdue, and an hour after a failed run. Set `SIGNALS_REFRESH_HOURS` to change the interval, or `0` to turn it off. The Home radar shows when the live feeds were last checked.

## API credentials and deployment

Keep keys out of the repository and frontend code. See `.env.example` for the environment variable names; **never commit actual values**.

The current application uses a shared demo profile and includes endpoints without user authentication. **It is not ready to deploy publicly with real user CVs or personal information.** Access control, data isolation, source verification and live provider testing need to be addressed first.

## What we're working on next

- Add the optional interest quiz so interest fit comes from the user, not the demo profile.
- Replace illustrative signals and course information with dated, reviewed sources.
- Complete evidence-update preview, saved history and deletion in the v2 interface.
- Add authentication and security checks before public deployment.

## Development notes and attribution

This prototype combines our team's v2 UI mockup with a modular FastAPI application and AI-assisted development. AI tools were used during prototyping and code preparation; the team is responsible for reviewing, testing and explaining the final submission. The original v2 interface design came from a team member and should be credited appropriately in the final project presentation.

We are keeping the existing commit history as a record of how the code entered the repository. Future changes should have commit messages describing the actual changes made.

Licensed under [Apache 2.0](LICENSE).
