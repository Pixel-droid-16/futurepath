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
new datasets and files absent from the original manifest are not hash-covered.
The explicit post-manifest policy below adds structural and schema coverage.
`tests/test_organization.py` also checks the assembled UI matches its source.
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

The original hash review changed no application source, rendered UI, or datasets.

## Post-manifest coverage policy (2026-10-24)

`python scripts/check_modular_coverage.py` is the companion to the hash verifier.
It needs only the Python standard library, reads files without importing the app,
and never writes generated output, datasets or manifests. CI runs it even when
the historical/reviewed hash step fails. The isolated regression suite includes
`tests/test_modular_coverage.py` fault-injection checks in disposable copies.

### Decisions and provenance

| Scope | Protection | Provenance and reason |
| --- | --- | --- |
| Original design/runtime/assets and historical snapshots | Existing original hashes, unchanged | Original manifest remains the evidence for immutable imported assets. |
| `frontend/index.html` | Existing narrowly reviewed hash **and** assembly equality | Evolved generated release page, not the original mockup. Its reviewed hash must still be approved independently of rebuilding. |
| `frontend/mockup_source` active fragments | Explicit required inventory, independent ordered assembly contract, output equality; existing UI/translation/organization tests | Modular source is visible at the shallow `caeb753` boundary; latest fragment change is `f3443e6` (Signals permissions). These are editable implementation files, not newly discovered immutable originals. No new hashes. |
| Retired fragments: `pages/intake.html`, `pages/login.html`, `logic/intake_sample_skills.js`, `logic/intake_skill_view.js` under `frontend/mockup_source` | Explicit retained inventory, excluded from assembly | Legacy remnants present at the shallow boundary, retained for reference only. Presence is protected, bytes are not certified historical originals. They must not be silently reintroduced into the active page. Deliberate deletion requires a policy/inventory review. |
| `backend/routes` and `backend/services` | Exact Python file inventories, regular-file and syntax checks; existing API/provider/profile/CV/scenario/signal behavior tests | Modular route/service structure is visible at `caeb753`; CV profile service was added in `3c5bae3`, with later route evolution including `f3443e6`. Hashing ongoing feature logic would freeze intended evolution rather than prove correct behavior. |
| `data/extra_courses.json` | Required nonempty raw dataset, per-row schema, unique IDs across both course sources, known skill references and checked-date provenance; `tests/test_courses.py` for learning coverage | Hand-maintained additions, latest change `59b31e6`; each row records a provider-page check date. Unlike imported `data/courses.json`, this file is expected to evolve. Dates are claims of past review, not a live link/quality guarantee. |

No additional immutable new asset was identified in these scopes. Do not add
hashes simply because a file is new. File inventories are deliberately explicit,
not generated from the working tree. Unexpected files in these three directories
fail as unclassified (except Python cache artifacts); missing files and symlinks
fail. Other post-manifest directories remain outside this inventory's scope.
This is not a security signature or exhaustive runtime correctness check.

The ordered fragment contract is independent of the builder's recipe so that
omitting, duplicating, reordering or reintroducing retired fragments is detected
even if the generated page is rebuilt to match the faulty recipe. Ordinary
source edits are allowed once output is rebuilt, but the page's reviewed hash
remains a separate approval gate. No current application output was rebuilt or
reverted for this policy.

### Updating coverage intentionally

1. For a new file in a covered directory, classify it as active, retained legacy,
   or a new immutable asset; document its source/history and intended contract.
2. Update only the relevant explicit inventory. For an intentional assembly
   recipe change, review both the builder and the independent ordered contract.
3. Add behavioral coverage for changed routes/services. Syntax and existence do
   not establish endpoint registration or correct behavior; the organization and
   feature tests remain required.
4. For extra courses, preserve row-level provider/date provenance and schema,
   and run course tests. Do not blindly hash the dataset or infer live accuracy
   from a successful offline check.
5. Run both integrity commands and `python scripts/check_regressions.py`.
   Do not refresh old hashes to hide unrelated failures.

At this review's starting tree (`230bc97`), hash verification already reports
`data/roles.json`, `backend/engine.py`, and `frontend/index.html` mismatches.
The current page nevertheless matches its assembly source. This policy neither
approves those hash mismatches nor resolves existing role/scoring behavior issues.

## SDC main alignment and Signals refresh review (2026-10-24)

The user authorized direct changes on GitHub `main` without new branches. The release was fast-forwarded to `f7ddb66`, preserving 30 upstream commits. The documentation update `761102f` rewrote `README.md` to match the official SDC Hackathon submission template and replaced the obsolete `docs/ARCHITECTURE.md`; it also corrected the Replit port reference to 5000 and added a pending submission checklist. No example placeholder handler was copied into the working project.

The Signals fix `f3443e6` integrated the already-reviewed isolated admin-refresh hotfix into the latest teammate frontend rather than overwriting its career/scenario changes. It changed the generated V2 `frontend/index.html` and the editable Signals fragments, added a read-only refresh-capability endpoint, preserved admin restrictions, and updated `.env.example` to document optional `ADMIN_TOKEN`. The original protected `frontend/app.js`, `frontend/style.css`, runtime helpers and image assets remain untouched.

Four previously reviewed file hashes were updated to the actual accepted bytes (`README.md`, `frontend/index.html`, `.env.example`, and newly reviewed `docs/ARCHITECTURE.md`). This is a **narrow documented review**, not a baseline reset. The original manifest remains unchanged. The existing malicious-change fixture still requires verification failures when any reviewed file is modified or removed.

Fresh final combined tests and browser validation are required; these hash updates are **not** a claim that the Signals refresh or all application paths have passed tests.

## Teammate scoring and role-data evolution (2026-10-24)

Two accepted `main` changes were not reflected in the historical reviewed manifest:
`95cd1a9` introduced embeddings/semantic search in career matching and updated role requirements, while
`4adc3a9` corrected a ranking crash and adjusted score/card presentation. The actual
`backend/engine.py` and `data/roles.json` bytes are now pinned, without altering these
teammate-authored files or the original manifest. These are *intentional changes with provenance*, not permission to
silently change the career scoring model later. Run all backend scoring, scenario and browser
tests after integration; a pinned hash does not prove algorithm quality.

## Generated V2 source alignment (2026-10-24)

The Signals refresh fix had added the permission-checking initializer to the generated
`frontend/index.html` but not to `frontend/mockup_source/logic/state_and_actions.js`.
The editable source was corrected to match the already-reviewed generated output,
without modifying the UI or original protected assets. The frontend assembly
consistency test must still pass before the release is considered verified.

## RunPod response reliability and fallback attribution (2026-10-24)

The user authorized a targeted main-branch reliability fix after a completed
RunPod response failed backend structure validation. Reviewed provider changes
accept bounded, known JSON wrappers and conservatively retain only fully decoded,
grounded candidate objects from a cut-off candidates array. They do not repair
partial quotes, invent skills, relax canonical IDs, or deploy a worker change.
The prompt requests at most eight candidates with short literal quotes.
Automatic text extraction falls directly from RunPod to the local dictionary;
scanned-PDF Claude routing remains separate. Failure details and logs exclude raw
model output, contact data and actual job identifiers.

The only reviewed hash updated here is `frontend/index.html`, assembled from
the existing V2 fragments. Its changes capture safe extraction-warning presence
and append a fixed fallback explanation to the existing dictionary confirmation
note. There are no layout, stylesheet, original asset, scoring or dataset changes.
The original manifest and all other reviewed hashes remain unchanged.
Offline mock-provider, grounding, fallback, assembly and browser tests validate
these contracts independently; hashes do not establish live provider reliability.

## Staged daily Signals evidence and administrator review (2026-10-24)

The user explicitly authorized development-only best-effort daily checking,
keyword-only automatic tagging, and an approval gate before new external evidence
can affect scoring. Newly fetched candidates now enter an auditable SQLite queue.
Bearer-authenticated review publishes approved evidence transactionally; rejection
and pending status cannot enter active signals. Public demo independently blocks
background/manual fetching and all review actions. Existing active evidence,
shared profiles, provider extraction behavior, datasets and original V2 assets
are preserved. See `SIGNALS_REFRESH.md` for timing, auth and deployment limits.

Exactly three previously reviewed hashes change deliberately:

- `.env.example`: document the safe default of 0/off and the development-only
  24-hour opt-in. The published synthetic demo remains off.
- `backend/app.py`: initialize persisted schedule timing during lifespan startup,
  including off/public-demo states, before creating the existing background task.
- `frontend/index.html`: regenerate from the editable V2 fragments after adding
  read-only schedule metadata, an authenticated evidence review queue and accurate
  pending-versus-approved refresh feedback. The API adapter retains HTTP status
  metadata so 401/403/409 review errors can be identified without displaying raw
  server errors. Token handling is short-lived and
  never persisted in browser state/storage; original layout/assets are unchanged.

No original manifest, stylesheet, protected asset or other reviewed hash is
refreshed. Additive storage migration and focused Signals modules are verified by
offline backend and isolated Chromium tests; the hash checker is not proof of
production timer reliability or durable storage.


## Signals V2 pagination and status source review (24 October 2026)

The V2 Signals fragments and generated `frontend/index.html` intentionally
change only the Signals page: three numbered pagers and a compact automatic
update status. The historical original manifest, nineteen other reviewed
hashes, original V2 theme, images and unrelated modules remain unchanged.
The SHA256 entry for `frontend/index.html` was updated to these exact
new assembled source bytes.


## Signals V2 pagination and scheduler-status refinement (24 October 2026)

The generated `frontend/index.html` is intentionally updated from its Signals
source fragments: no more than five numbered buttons are visible per independently
paged list, navigation and responsive filters stay within the container, empty
results have a readable state, and status displays disabled/partial/active checks
without claiming daily reliability on sleeping deployments. An optional read-only
browser timer reloads stored signals only when the Signals page is visible and
never invokes a news feed fetch or paid model. Original V2 CSS and image assets
are unchanged. The reviewed generated-page hash is updated to the new bytes.


## Team name metadata correction (24 October 2026)

The independent README update `06fb0f8` changed the team-name placeholder
to `KitaHack`. The exact existing README bytes are retained, and only the
corresponding reviewed SHA256 entry was updated. The original baseline and
all protected V2 design assets are unchanged.

## SDG explanations, interface tidy-up and README submission details (25 October 2026)

Three previously reviewed hashes are updated to the exact bytes merged into `main`
at `36d5a30`. The original manifest, the seventeen other reviewed hashes and all
protected V2 design assets are unchanged.

- `data/roles.json`: `70fe0af` replaces the placeholder `sdg_justification` text on
  12 of the 44 careers with role-specific explanations. No other field changes:
  role IDs, skill requirements, interests and scoring inputs are as reviewed at `95cd1a9`.
- `frontend/index.html`: reassembled from the V2 fragments after `70fe0af`, which
  aligns the Home hero, removes the Start page's "Private by design" box, reduces the
  Pathway SDG box to its badge and adds the matching Malay and Chinese text. The page
  equals its assembly source; no stylesheet, image or original asset changes.
- `README.md`: team-authored submission details since `06fb0f8`: confirmed members,
  SDG track and `src/` layout (`515cb6d`), repository structure (`0523435`), team
  information, presentation link and PDF descriptions (`b2bdfe6`, `1363db7`,
  `c962058`, `166a9d8`, `07cb77d`, `b23b1e4`, `cc0c51d`). Documentation only.

These hashes record accepted bytes, not correctness; the regression suite and
browser checks remain the evidence for behaviour.

## Submission checklist ticks (25 October 2026)

`README.md` only: the Submission Checklist now ticks the completed Preliminary
proposal and the renamed submission files, and names the actual
`SDC2026_KitaHack_*.pdf` files instead of the `TeamName` placeholder. The demo
video item stays unticked because no verified link exists yet. Only the README's
reviewed SHA256 entry is updated.
