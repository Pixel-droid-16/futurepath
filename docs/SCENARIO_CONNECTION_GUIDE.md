# FuturePath v2 — Scenario connection (next step)

This release starts from your group's confirmed **v2 mockup**, using its original page fragments, typography, colours and design runtime. It **does not** switch back to the older FuturePath Prism dashboard. The Results page has an intentionally added comparison panel using the same existing card style.

## What has become functional in the original v2 interface

1. **Results / career cards** — On page load, the browser fetches `/api/matches?scenario=moderate` and `/api/matches?scenario=rapid` and displays **12 backend roles** using the local, shared synthetic demo profile. Cards replace the seven hard-coded mock roles when the API connects. If the API fails, the screen shows an error instead of silently presenting invented results.
2. **Moderate vs Rapid AI** — The Results page now includes two real controls. Switching changes the career card rankings and selects the corresponding scenario's task impacts and skill priorities. The selected role is pulled from `/api/scenarios/{role_id}`.
3. **Career selection** — Use the dropdown in the comparison panel to compare a different career. The side-by-side task and learning priorities refresh from the backend.
4. **Learning pathway** — Clicking **See pathway** on a backend career card opens the chosen role's scenario-specific skill-priority list on the original v2 Pathway screen. Missing/unknown proficiency stays marked as **Assess**, not a confirmed gap.
5. **Honest demo notices** — The Results, Home, and Pathway pages label synthetic evidence and unverified course information. This package does not imply real labour-market forecasts or verified course fees.

## What is still a mockup

- The original v2 Intake form is not yet connected to profile persistence or AI extraction. Use `/ai-lab` for actual Claude/RunPod extraction testing. `/api/profile` still uses the single synthetic demo profile.
- The original v2 Signals page and Home feed are illustrative, not an approved live labour-market feed.
- The original v2 login screen is not an actual authentication system.
- Evidence approval and history APIs exist, but are not yet wired into the v2 page flow.
- Actual Claude/RunPod connectivity depends on your credentials and a running RunPod worker. No live external AI calls are needed for this feature.

## What to edit later

| Feature | Source to edit |
|---|---|
| Results page HTML and scenario cards | `frontend/mockup_source/pages/results.html` |
| Pathway page HTML | `frontend/mockup_source/pages/pathway.html` |
| Backend browser API calls, value mapping | `frontend/mockup_source/logic/live_career_adapter.js` |
| Scenario selection and API-loading state | `frontend/mockup_source/logic/state_and_actions.js` |
| Scenario comparison data for UI | `frontend/mockup_source/logic/live_scenario_comparison_view.js` |
| Rendered page bindings and toggles | `frontend/mockup_source/logic/page_bindings_view.js` |
| Career card adaptation | `frontend/mockup_source/logic/career_ranking_view.js` |
| Python scoring rules | `backend/engine.py` |
| Moderate/Rapid assumptions | `backend/scenarios.py` |
| Scenario route | `backend/routes/scenarios.py` |
| Demo role skills | `data/roles.json` |
| Demo profile and evidence | `data/demo_profile.json`, `data/snapshots.json` |

After editing a frontend fragment, **rebuild** before refreshing Chrome:

```bat
python scripts\build_frontend.py
```

Then run the tests:

```bat
python scripts\verify_integrity.py
python -m pytest -q
```

The verifier now excludes the *intentionally modified* assembled `frontend/index.html`, while continuing to verify untouched original design assets against prior release hashes. The original unchanged release is retained under `backup/` for rollback.

## Live scenario demonstration

1. Start the server from the folder containing `requirements.txt`.
2. Visit `http://127.0.0.1:8000/` and click **Results**.
3. Wait for **Connected to Python matching engine · SYNTHETIC EVIDENCE**.
4. Scroll to **Scenario Lab** and select **Data Analyst**.
5. Compare the Moderate and Rapid task impacts and learning priorities. Note that a scenario score change might be small: this is deliberate because it is a bounded hypothetical adjustment, not an invented prediction.
6. Choose **Rapid AI** and click the pathway link. The original Pathway design will show the role's corresponding priority skills.
7. Try **Cybersecurity Analyst** and **Sustainability Analyst** to show different role-specific task assumptions.

### Scores and slider warning

The **official backend score** uses fixed 45/20/20/15 weights for skills, interests, evidence trends, and learning feasibility. The original mockup's two sliders are now explicitly a **display-only sensitivity preview**, redistributing the skills-and-trends 65% share. Do not treat a slider-adjusted display score as an officially saved version.

### Security

Keep Anthropic and RunPod credentials only on the backend. The earlier exposed Anthropic key should be revoked. The demo curator endpoints remain unauthenticated and should never be placed on a public deployment as-is.
