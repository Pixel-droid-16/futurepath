# Explain FuturePath v2 to your judges

1. `frontend/index.html`: loads the single-page application.
2. `frontend/style.css`: v2 colours, light/dark, responsive layout, transitions, cards, pill navigation. Users choose one of four accent palettes.
3. `frontend/app.js`: builds pages, handles clicks and calls backend APIs using `fetch()`. It does **not** contain AI keys.
4. `backend/app.py`: exposes FastAPI routes for data, profile updates, CV text extraction, AI candidate-skill suggestions, recommendation results, history, and evidence review.
5. `backend/engine.py`: deterministic role scoring and gap prioritisation. A user-confirmed skill can contribute; unknown is separate from zero.
6. `backend/scenarios.py`: documents per-role fictional task exposure/oversight assumptions; has distinct moderate and rapid descriptions and action plans.
7. `data/roles.json`: every career in the catalogue, with role-skill requirements, importance levels and SDG justifications.
8. `data/skills.json`: canonical skills with aliases and SDG tags/explanations (SK079-SK082 are transferable skills: leadership, teamwork, event management, problem solving).
9. `data/snapshots.json`: prepared synthetic S1 (published) and S2 (draft). Approving S2 does not rewrite previously saved recommendations.
10. `data/learning_resources.json`: course **placeholders**. Do not claim verification. They are shown only for skills with no linked course.
    `data/courses.json` contains imported catalogue entries; `data/extra_courses.json` entries record provider-page check dates. The pathway distinguishes provider-page dates from the imported catalogue snapshot date. Confirm current course details with providers. Energy simulation and Content development lack a checked course.
11. `tests/`: verifies API and engine invariants, including scenario differences without changing the user profile.
12. `requirements.txt`: Python libraries needed to run.
13. `frontend/mockup_source/logic/translations.js`: shared English, Bahasa Melayu and Simplified Chinese text catalogue and localization helper. Change this file when adding or correcting app copy translations; rebuild both generated pages with `python scripts/build_frontend.py`.
14. `backend/semantic.py`: local MiniLM profile-fit and cautious skill-to-skill similarity, using cached vectors. `backend/text_match.py` is the keyword fallback.
15. `data/skill_relations.json`: human-reviewed related-skill pairs and blocked false friends. `data/semantic_vectors.json` holds precomputed vectors; rebuild it with `scripts/build_semantic_vectors.py` after editing role or skill text.

## The four key explanations

**Skills:** A CV is untrusted input. Extracted items are suggestions; the user chooses a 0–5 proficiency or Unknown. Unknown is not 0.

**Matching:** Each role requirement has an importance weight and target level. Exact catalogue skills score first; a curated related skill can add partial credit, but demonstrated readiness stays exact-only. Suitability combines skills, illustrative outlook, optional RIASEC interest, optional profile-text fit and a small sector prior, then spreads near-duplicate roles. Scores are not job probabilities.

**Scenarios:** Moderate and Rapid hold the profile fixed but change hypothetical adoption assumptions, task-level descriptions and ordering/priority of learning gaps. The two futures are not factual predictions.

**Evidence refresh:** S1 generates saved version R1. Curator approves S2. Before saving a new result, FuturePath previews differences using R1's stored profile and scoring scenario, isolating the evidence change. User explicitly decides to save R2.

## Known compromises

This is a genuine interactive **demo** with a working local API, not a production-ready, fully sourced commercial product. AI credentials, real RunPod workers, verified resource links, user accounts, secure review permissions and observed labour-market datasets need additional implementation.
