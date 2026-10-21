# Explain FuturePath v2 to your judges

1. `frontend/index.html`: loads the single-page application.
2. `frontend/style.css`: v2 colours, light/dark, responsive layout, transitions, cards, pill navigation. Users choose one of four accent palettes.
3. `frontend/app.js`: builds pages, handles clicks and calls backend APIs using `fetch()`. It does **not** contain AI keys.
4. `backend/app.py`: exposes FastAPI routes for data, profile updates, CV text extraction, AI candidate-skill suggestions, recommendation results, history, and evidence review.
5. `backend/engine.py`: deterministic role scoring and gap prioritisation. A user-confirmed skill can contribute; unknown is separate from zero.
6. `backend/scenarios.py`: documents per-role fictional task exposure/oversight assumptions; has distinct moderate and rapid descriptions and action plans.
7. `data/roles.json`: twelve careers, with nine role-skill requirements each and SDG justifications.
8. `data/skills.json`: 82 canonical skills with aliases (SK079-SK082 are transferable skills: leadership, teamwork, event management, problem solving).
9. `data/snapshots.json`: prepared synthetic S1 (published) and S2 (draft). Approving S2 does not rewrite previously saved recommendations.
10. `data/learning_resources.json`: 30 course **placeholders**. Do not claim verification. They are shown only for skills with no checked course.
    `data/courses.json` (imported from LaluanKu) and `data/extra_courses.json` (56 courses added by hand, each with the date its provider page was checked) are the checked courses: real links, cost and hours from the provider's page. Only Energy simulation and Content development still lack one.
11. `tests/`: verifies API and engine invariants, including scenario differences without changing the user profile.
12. `requirements.txt`: Python libraries needed to run.

## The four key explanations

**Skills:** A CV is untrusted input. Extracted items are suggestions; the user chooses a 0–5 proficiency or Unknown. Unknown is not 0.

**Matching:** Each role requirement has an importance weight and target level. Weighted assessed skill coverage becomes demonstrated readiness. Suitability adds interest, illustrative outlook, and reskilling feasibility. Scores are not job probabilities.

**Scenarios:** Moderate and Rapid hold the profile fixed but change hypothetical adoption assumptions, task-level descriptions and ordering/priority of learning gaps. The two futures are not factual predictions.

**Evidence refresh:** S1 generates saved version R1. Curator approves S2. Before saving a new result, FuturePath previews differences using R1's stored profile and scoring scenario, isolating the evidence change. User explicitly decides to save R2.

## Known compromises

This is a genuine interactive **demo** with a working local API, not a production-ready, fully sourced commercial product. AI credentials, real RunPod workers, verified resource links, user accounts, secure review permissions and observed labour-market datasets need additional implementation.
