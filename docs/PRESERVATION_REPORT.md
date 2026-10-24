# Preservation report — reorganised release

> Historical report for the initial modular reorganization, not invariants of
> today's release. Later source, datasets and assembled UI intentionally evolved.
> See [the current integrity review](INTEGRITY_REVIEW.md) for reviewed differences,
> exact hash coverage and the distinction between original and evolved files.

## Intended invariants

1. **Original v2 home HTML** remains byte-for-byte identical to the previous package.
2. **Original AI Lab HTML** remains byte-for-byte identical.
3. **Original CSS, JS runtime, images and JSON datasets** remain unchanged.
4. **Same FastAPI paths and response contracts** for all existing endpoints; tests exercise them.
5. **Same deterministic matching and scenario engine** in `backend/engine.py` and `backend/scenarios.py`.
6. **Same RunPod worker starter and Dockerfile**.
7. **Same startup command:** `python -m uvicorn backend.app:app --reload`.
8. **Original package available for rollback** at `backup/PREVIOUS_UNMODIFIED_RELEASE.zip`.

## Structural changes (intentional)

- Split original v2 `frontend/index.html` into independent editable page, theme and view-data fragments under `frontend/mockup_source/`; the runtime `index.html` file is rebuilt from these pieces without changes.
- Split original `frontend/ai-lab.html` into markup, CSS and interactions under `frontend/mockup_source/ai_lab/`.
- Refactored the large `backend/app.py` into feature-specific `backend/routes/`, shared `backend/services/`, `backend/storage.py`, `backend/schemas.py`, `backend/catalog.py`.
- Refactored `backend/ai_providers.py` into `backend/providers/claude.py`, `runpod.py` and `validation.py`. A compatibility re-export remains in `backend/ai_providers.py` so existing imports still work.
- Added integrity checks, documentation and a previous release backup.

## What this preservation report DOES NOT prove

- Pixel-perfect layout in your specific version of Chrome; no browser screenshot test is included.
- Live Claude API or RunPod GPU success (simulated network tests only).
- Correct data from authoritative workforce sources; the dataset remains a synthetic demo.
- Integration between the original friend's v2 screen content and the real backend, which was **already incomplete** in the prior release and is still incomplete.
- Production-ready user login, secure multiuser isolation or curator authentication.

Run `python scripts/verify_integrity.py` to recheck the original-asset hashes and `python -m pytest -q` for behavioural regression tests.

> Later change: the separate AI Lab page (`frontend/ai-lab.html`, `/ai-lab`) has since been removed; CV extraction now runs from the Start page.
