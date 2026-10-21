# FuturePath v2 — Scenario Connected Edition

**Status:** Local runnable demo using the group's **confirmed original v2 mockup**. This release adds backend-driven career results, a functional Moderate AI / Rapid AI comparison and linked learning priorities to the original screen style. It is not yet an end-to-end production app.

## Quick start (Windows)

1. Extract this ZIP into a **new** folder, for example `C:\Users\<you>\OneDrive\Desktop\FuturePath_v2_Scenarios_Connected`. Keep your existing `FuturePath_v2` intact.
2. Open File Explorer in the new extracted folder that contains `requirements.txt` and `backend`, click the address bar, type `cmd` and press Enter.
3. Install and start:

```bat
python -m pip install -r requirements.txt
python -m uvicorn backend.app:app --reload
```

4. Open `http://127.0.0.1:8000` and click **Results**, then scroll to **Scenario Lab — Moderate AI vs Rapid AI**.
5. The Results page should say **Connected to Python matching engine · SYNTHETIC EVIDENCE**.

If another FuturePath server is already running on port 8000, press **Ctrl+C** in its Command Prompt first.

## Demonstration

- Original v2 **Home**, **Intake**, **Results**, **Pathway**, **Signals**, **About**, **Login** design framework preserved.
- **12 backend careers** replace the earlier seven sample Results cards when connected.
- **Moderate/Rapid** toggles change the task-impact comparisons, skill-priority ordering and illustrative suitability component. Compare Data Analyst first.
- Click **See pathway** on any career result to open a role-specific pathway with the selected scenario's priority skills. Unverified course details are clearly labelled.
- Your friend’s original v2 styling and page navigation are maintained; only targeted result/pathway content and one matching-style scenario panel are changed.

## Important limits

- Career trends are **synthetic prepared snapshots**. Neither the feed nor scenario numbers are verified labour-market forecasts.
- The original v2 **Intake** page, **Signals** page, login, and evidence/history user interface still contain mockup functionality. The real Python profile and recommendation APIs, the curator demo endpoints, and `/ai-lab` remain available. The next integration step is to wire skill confirmation and profile saving to the original v2 Intake page.
- RunPod worker deployment and real Claude API calls are **not yet verified with your account**. Neither is required to compare the two AI adoption scenarios.
- The demo has a shared profile, an unauthenticated curator endpoint and no user accounts. **Do not publicly deploy without securing these routes and isolating user data.**

## Project organization and edit locations

Read **`docs/SCENARIO_CONNECTION_GUIDE.md`** first. It includes a file-by-file editing map, exact demo walk-through and the distinction between true functionality and mockup behaviour.

All frontend v2 pages remain individually editable under `frontend/mockup_source/pages/`. Feature-specific JavaScript lives under `frontend/mockup_source/logic/`. Python APIs are divided under `backend/routes/` with engine logic in `backend/engine.py` and assumptions in `backend/scenarios.py`.

To rebuild the assembled frontend after editing its source:

```bat
python scripts\build_frontend.py
```

To verify and run tests:

```bat
python scripts\verify_integrity.py
python -m pytest -q
```

The previous unchanged release is available under `backup/` for rollback. This ZIP has no API keys and makes no changes to your local folder or GitHub.
