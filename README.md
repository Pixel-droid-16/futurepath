# FuturePath

Career exploration and reskilling prototype for **SDC Hackathon 2026 — Domain 1**.

We're building FuturePath to help students, graduates and working professionals understand how their current skills relate to different careers, what they might need to learn next, and how AI adoption could change the work involved.

The project currently uses our team's **v2 interface design** with a Python backend. It is a hackathon prototype, not a live labour-market forecasting service.

## Try it locally

You'll need Python and a terminal.

```bash
python -m pip install -r requirements.txt
python -m uvicorn backend.app:app --reload
```

Open:

- **Website:** http://127.0.0.1:8000
- **AI extraction test page:** http://127.0.0.1:8000/ai-lab
- **API documentation:** http://127.0.0.1:8000/docs

If port 8000 is in use, stop the previous local server before starting this one.

## What you can try today

1. Open **Results**. The career cards load **12 roles across six sectors** from the Python matching API using a shared synthetic demo profile.
2. In **Scenario Lab**, select **Data Analyst** and compare **Moderate AI** with **Rapid AI**.
3. Change the selected career to see a different set of task impacts and skills to prioritise.
4. Open **Pathway** from a career card. It carries the selected role and scenario into the learning-priority view.
5. Open **AI Lab** to test rule-based skill extraction. Claude and RunPod adapters are included, but live use requires private credentials and an active provider endpoint.

The Moderate/Rapid scenarios use explicit, hand-authored assumptions about task change and human oversight. **They are not measured probabilities, job-loss forecasts or verified labour-market predictions.** Score adjustments are intentionally bounded; the more visible differences are in task impacts and learning priorities.

## Current implementation status

| Area | Current state |
| --- | --- |
| v2 Home, Results and Pathway design | Present |
| Career matching | Python API connected to Results |
| Moderate/Rapid scenario comparison | Backend-connected on Results |
| Career-specific learning priorities | Connected from Results to Pathway |
| Skill taxonomy and role catalogue | Local JSON datasets |
| CV skill extraction | Local fallback and optional AI provider adapters |
| Skills Radar / Home signal feed | Illustrative data and interface |
| Intake and saved user profile | Original form is not yet connected end-to-end |
| Login and user accounts | Mockup only; no real authentication |
| Evidence approval and recommendation history | Backend demo APIs exist; v2 screens are not fully connected |
| Claude API | Integration code included; live calls not verified for this deployment |
| RunPod GPU | Worker and adapter code included; GPU worker not deployed here |

The prototype uses **synthetic CV/profile information and prepared evidence snapshots**. Learning-resource details may be placeholders or unverified. Please don't treat the displayed career scores as employment probabilities.

## Project structure

```text
backend/
  app.py                 FastAPI entry point
  routes/                Endpoints grouped by feature
  services/              Recommendation, document and extraction logic
  providers/             Claude, RunPod and output validation
  engine.py              Career scoring and skill-gap calculations
  scenarios.py           Moderate and Rapid AI assumptions
data/
  roles.json             Career requirements
  skills.json            Canonical skill catalogue
  snapshots.json         Prepared evidence versions
  learning_resources.json
frontend/
  index.html             Generated v2 application page
  ai-lab.html            Standalone extraction test page
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

## API credentials and deployment

Keep keys out of the repository and frontend code. See `.env.example` for the environment variable names; **never commit actual values**.

The current application uses a shared demo profile and includes endpoints without user authentication. **It is not ready to deploy publicly with real user CVs or personal information.** Access control, data isolation, source verification and live provider testing need to be addressed first.

## What we're working on next

- Connect the original v2 Intake screen to profile saving and user-confirmed skills.
- Connect AI extraction to Intake without changing the team's UI design.
- Replace illustrative signals and course information with dated, reviewed sources.
- Complete evidence-update preview, saved history and deletion in the v2 interface.
- Add authentication and security checks before public deployment.

## Development notes and attribution

This prototype combines our team's v2 UI mockup with a modular FastAPI application and AI-assisted development. AI tools were used during prototyping and code preparation; the team is responsible for reviewing, testing and explaining the final submission. The original v2 interface design came from a team member and should be credited appropriately in the final project presentation.

We are keeping the existing commit history as a record of how the code entered the repository. Future changes should have commit messages describing the actual changes made.

Licensed under [Apache 2.0](LICENSE).
