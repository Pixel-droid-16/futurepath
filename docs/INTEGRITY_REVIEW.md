# Integrity baseline review

## Evidence and decision

The original manifest is retained unchanged as historical evidence. Its hashes
for the 14 flagged files match their bytes in the modular import `20bb8ef`.
Comparing those files directly with release
`23df063daae98040e544edfcd9f9219e32a5da43` confirms all 14 differences were
already upstream. None is an original CSS, JS runtime, or image change.
Available history includes a shallow/grafted boundary at `caeb753`; comparisons
use actual Git blobs, not an assumption that the visible log is complete.

This review also covers the current pre-review tree at `67d602b`, including
the upstream feature update `59b31e6` and Replit/test setup. That tree has 15
warnings: `backend/scenarios.py` is the additional changed file. Four more files
were silently excluded by the old checker, so 19 reviewed hashes are recorded.
These are exact accepted bytes, not permission for arbitrary future changes.

## Reviewed changes (all paths in REVIEWED_FILE_HASHES.json)

| File | Historical change and reason for retaining it |
| --- | --- |
| `.env.example` | Provider model selection, signal admin/refresh settings and password-gated synthetic demo settings; later optional RunPod model display configuration. These are configuration examples, not design assets. |
| `requirements.txt` | Removed duplicate httpx, added dotenv and Anthropic SDK; later Playwright for isolated browser tests. Dependency evolution, not asset corruption. |
| `.gitignore` | Ignore local `.env` configuration. Preserve secret hygiene. |
| `INTEGRATION_EXPLAINED.md` | CV upload moved from the removed AI Lab to Start. Documentation follows implemented flow. |
| `tests/test_ai_providers.py` | Expanded provider validation, PDF extraction, queue handling and fallback regressions. Tests follow the evolved provider interfaces. |
| `tests/test_api.py` | Expected role count changed from 12 to 44. Matches the expanded catalogue rather than restoring obsolete data. |
| `tests/test_engine.py` | Broader catalogue validation and scoring/interest/scenario coverage. Assertions follow the updated matching model. |
| `data/roles.json` | Expanded careers and RIASEC interests; corrected developer role requirements. Includes the full-stack alignment in `d7e6b7a`. |
| `data/skills.json` | Expanded canonical skills/aliases, developer taxonomy (`5591005`) and retained Malay/Chinese SDG explanations (`ed779c0`). No dataset rollback is justified. |
| `docs/WHAT_EACH_FILE_DOES.md` | Updated catalogue descriptions and translation editing guidance, with line-ending changes. Documentation rather than immutable design. |
| `docs/PROGRAM_EXPLAINED.md` | Replaced obsolete fixed catalogue counts with references to the current files. |
| `backend/engine.py` | Weighted skill, signal-demand and optional RIASEC scoring replaced earlier scoring. `59b31e6` subsequently uses AI-weighted signal demand instead of a hypothetical task-exposure offset. Preserve intentional behavior, tested separately. |
| `runpod_worker/Dockerfile` | Corrected repository-root COPY paths; CUDA 12.8 and explicit torch 2.7.1 for Blackwell support. Do not revert infrastructure to satisfy old hashes. |
| `runpod_worker/requirements.txt` | Aligned torch 2.7.1 and bounded transformers, accelerate and safetensors with that worker runtime. |
| `backend/scenarios.py` | Unchanged at `23df063`; `59b31e6` updates explanation to match doubled AI-signal weighting. This explains the fifteenth warning now. |
| `backend/app.py` | Previously exempt modular entrypoint; subsequently adds signals routes/scheduling and demo access gate. Pin it instead of ignoring it. |
| `backend/ai_providers.py` | Previously exempt compatibility wrapper for modular providers; later exposes PDF/page helpers and configured model names. Pin current wrapper. |
| `README.md` | Previously exempt rewrite documenting the modular app, current features and safe demo setup. Pin current documentation. |
| `frontend/index.html` | Previously exempt assembled UI. Intentional historical Start/Results/Pathway/Signals updates, AI Lab removal, translations and model/scenario labels are preserved. Pin current assembled output, not the obsolete pre-modular page. |

## Protection and limits

`python scripts/verify_integrity.py` checks every original manifest entry:
original hashes by default, reviewed hashes only for the 19 listed files.
Original `frontend/style.css`, `app.js`, `support.js`, `image-slot.js`, `hero.svg`,
and all listed assets/uploads cannot receive reviewed overrides. Other unchanged
files (including original snapshots and learning resources) retain original hashes.
Missing files, changed reviewed files, malformed manifests and duplicate entries
fail with a nonzero exit status. No Git checkout/network is needed to run it.

The check is deliberately **not** a whole-repository/security signature or a
claim that the entire current UI equals the initial mockup. New modular source,
new datasets and files absent from the original manifest are not covered.
`tests/test_organization.py` separately checks the assembled UI matches its source.
Hashes cannot validate model correctness, course quality, provider availability
or pixel rendering. Use behavioral tests for those contracts.

## Future intentional edits

1. Inspect the diff against the recorded baseline and identify why it is needed.
2. Preserve protected original design files; do not auto-refresh their hashes.
3. For evolved files, document the reason and commit provenance here, then update
   only the reviewed entry after review. Never regenerate the entire manifest
   from a dirty working tree or add a blanket skip.
4. Build the frontend when editing its source, run integrity and regression tests.

This review changes no application source, rendered UI, or datasets.
