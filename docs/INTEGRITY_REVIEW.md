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
were silently excluded by the old checker, so 19 reviewed hashes were originally recorded. One additional reviewed documentation file is now tracked, giving 20 reviewed entries.
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
| `docs/ARCHITECTURE.md` | SDC submission alignment replaces an obsolete statement that RunPod/Qwen was merely planned; documents the actual modular backend, privacy limits and Replit port 5000. This is a reviewed documentation correction, not a CSS/JS asset change. |

## Protection and limits

`python scripts/verify_integrity.py` checks every original manifest entry:
original hashes by default, reviewed hashes only for the 20 listed files.
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

### Automated repository checks

`.github/workflows/repository-checks.yml` runs on pushes, pull requests and manual
dispatch. Independent jobs run `python scripts/verify_integrity.py` and
`python scripts/check_regressions.py` on Python 3.12. The latter installs no
browser runtime and explicitly excludes `tests/browser`; all other tests run
without expected-failure exemptions. Dependencies use the existing
`requirements.txt`.

The regression runner creates and removes a unique temporary synthetic SQLite
database, initializes the storage module before legacy test collection can
redirect it to a shared path, disables scheduled refresh and local dotenv
loading, clears provider credentials, and blocks socket connections. Provider
tests still use their synthetic keys and mocks; live paid calls are forbidden.
Run the same two commands locally to reproduce the checks.

The CLI regression test mutates a reviewed file only in a disposable copy and
requires exit status 1 from the actual verifier command. Neither CI nor tests
regenerate hashes. Existing behavioral failures remain blocking failures, not
silently skipped tests.

To enforce these checks before merging, a repository administrator must require
**Reviewed file integrity** and **Non-browser regressions** in the target
branch's protection/ruleset. Merely adding a workflow does not prevent direct
pushes or deployments outside that policy.

### Review procedure

1. Inspect the diff against the recorded baseline and identify why it is needed.
2. Preserve protected original design files; do not auto-refresh their hashes.
3. For evolved files, document the reason and commit provenance here, then update
   only the reviewed entry after review. Never regenerate the entire manifest
   from a dirty working tree or add a blanket skip.
4. Build the frontend when editing its source, run integrity and regression tests.

This review changes no application source, rendered UI, or datasets.

## SDC main alignment and Signals refresh review (2026-10-24)

The user authorized direct changes on GitHub `main` without new branches. The release was fast-forwarded to `f7ddb66`, preserving 30 upstream commits. The documentation update `761102f` rewrote `README.md` to match the official SDC Hackathon submission template and replaced the obsolete `docs/ARCHITECTURE.md`; it also corrected the Replit port reference to 5000 and added a pending submission checklist. No example placeholder handler was copied into the working project.

The Signals fix `f3443e6` integrated the already-reviewed isolated admin-refresh hotfix into the latest teammate frontend rather than overwriting its career/scenario changes. It changed the generated V2 `frontend/index.html` and the editable Signals fragments, added a read-only refresh-capability endpoint, preserved admin restrictions, and updated `.env.example` to document optional `ADMIN_TOKEN`. The original protected `frontend/app.js`, `frontend/style.css`, runtime helpers and image assets remain untouched.

Four previously reviewed file hashes were updated to the actual accepted bytes (`README.md`, `frontend/index.html`, `.env.example`, and newly reviewed `docs/ARCHITECTURE.md`). This is a **narrow documented review**, not a baseline reset. The original manifest remains unchanged. The existing malicious-change fixture still requires verification failures when any reviewed file is modified or removed.

Fresh final combined tests and browser validation are required; these hash updates are **not** a claim that the Signals refresh or all application paths have passed tests.
