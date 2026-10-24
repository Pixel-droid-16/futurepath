# Beginner-safe editing workflow

The key rule is **one change, one test, one screenshot**. You can roll back using `backup/PREVIOUS_UNMODIFIED_RELEASE.zip`.

## Example 1: Change Home heading text

1. Open `frontend/mockup_source/pages/home.html` in VS Code.
2. Search for the visible heading. Make one text edit, taking care not to delete `{{ ... }}` bindings.
3. Run `python scripts/build_frontend.py` from the root folder.
4. Restart/refresh `http://127.0.0.1:8000/` and verify the heading.
5. Run `python -m pytest -q`.

## Example 2: Change the colour theme

1. Open `frontend/mockup_source/styles/v2_theme.css`.
2. Change the relevant `--pr`, `--soft`, or theme colour variables **within the selected theme/accent rule**.
3. Run the frontend builder and inspect both light and dark themes on mobile and desktop.
4. Do not replace the original shared `support.js` unless you know how the v2 custom runtime works.

## Example 3: Change the demonstration Moderate/Rapid scenario

- Mockup screen: the toggle is defined in `frontend/mockup_source/pages/results.html` and its view bindings live in `frontend/mockup_source/logic/page_bindings_view.js`. The original mockup data is not a live forecast.
- **Real backend outputs:** edit `backend/scenarios.py` to change task assumptions; edit `backend/engine.py` to change the numerical scenario influence. Existing tests ensure readiness and confirmed skill gaps don't change by scenario.
- Run `python -m pytest -q` and inspect `/api/scenarios/data-analyst`.
- Later when connecting results UI to the API, do not delete the original v2 markup; replace its data source carefully.

## Example 4: Change Claude or RunPod behaviour

- Claude: `backend/providers/claude.py`
- RunPod adapter: `backend/providers/runpod.py`
- AI evidence validation: `backend/providers/validation.py`
- Provider fallback order: `backend/services/ai_extraction.py`
- GPU worker inference: `runpod_worker/handler.py`

Never paste live keys into project files or screenshots. Tests of providers use simulated responses, **not** your live account.

## Example 5: Edit the career list

Edit `data/roles.json`, keeping unique IDs and referring only to skill IDs defined in `data/skills.json`. This changes backend recommendations, not the old static roles displayed by the v2 mockup. Changing JSON after a database is already seeded may also require an intentional data migration for stored versions.

## Testing commands

```bat
python scriptsuild_frontend.py
python scriptserify_integrity.py
python -m pytest -q
python -m uvicorn backend.app:app --reload
```

Run the integrity command as `python scripts/verify_integrity.py` (the legacy
command block above contains control-character typos).

An integrity failure requires reviewing the diff, even after an intentional edit.
See `docs/INTEGRITY_REVIEW.md` before updating a reviewed hash. The original
manifest is historical evidence and protected design assets cannot be overridden.
The checker never automatically accepts changed bytes.

## What not to do

- Don't edit assembled `frontend/index.html` directly.
- Don't delete the original runtime files under `frontend/`.
- Don't put API secrets in HTML, source code or GitHub.
- Don't treat the mockup's UI login button as actual secure authentication.
- Don't run Replit public deployment with the demo-only curator API or shared profile.
