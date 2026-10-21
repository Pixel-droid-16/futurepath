# How to Explain Every Part of FuturePath

## The 30-second explanation

"FuturePath is a career intelligence web prototype. Users confirm their skills and proficiency, then a rules-based engine compares those skills against 12 career profiles. We show separate readiness and assessment completeness, future scenarios, skill gaps and learning suggestions. Our evidence approval demo uses two synthetic versions to prove that new data can't silently overwrite an old recommendation."

## Step by step: what the files do

1. `frontend/index.html` — The **skeleton** of the website: sidebar, header, content area, dark-mode control and scenario selector. Think of it as a house's floor plan.
2. `frontend/style.css` — The **appearance**: premium colour palette, rounded cards, grids, responsive sizing, subtle transitions and light/dark colour variables. Think of it as the house's interior design.
3. `frontend/app.js` — The **behaviour**: which screen opens after a click, where scores appear, what happens on a form save, and when to ask the backend for new results. This is the UI controller.
4. `backend/app.py` — The **reception desk/API**: accepts UI requests, reads/writes records in SQLite, parses uploaded synthetic CVs, checks which snapshot is approved, and sends structured answers back.
5. `backend/engine.py` — The **career calculator**. It receives a profile, career requirements, an approved snapshot, skill definitions and learning resource candidates. It returns scores, skill gaps and ranked learning priorities. It does not ask generative AI to invent scores.
6. `data/skills.json` — The **skill dictionary**. Each skill has a stable ID; aliases help reconcile different spellings and CV expressions.
7. `data/roles.json` — The **career requirements handbook**. Each of 12 roles has nine required skills, a proficiency target, importance, classification and an illustrative SDG connection.
8. `data/demo_profile.json` — A **fictional learner**, useful for classroom demonstrations.
9. `data/snapshots.json` — Two **fictional evidence states**. S1 begins published; S2 needs manual approval. Never tell judges these are genuine published statistics.
10. `data/learning_resources.json` — 30 **unverified sample records** illustrating the planned course schema; real providers and links must be checked before a final submission.
11. `tests/test_engine.py` — Tests basic requirements, deterministic scoring, unknown proficiency and scenario invariants.
12. `tests/test_api.py` — Simulates save S1 → approve S2 → compare → delete.
13. `requirements.txt` — Lists the external Python packages the computer needs.

## What happens when users click Save Profile?

`app.js` collects inputs and sends JSON to `PUT /api/profile` → `app.py` validates IDs and proficiency 0–5 → SQLite stores the confirmed skill dictionary → frontend retrieves fresh `/api/matches` → `engine.py` recalculates results. Unselected or unassessed skills remain unknown.

## What do 84/100 and 78/100 mean?

They are **illustrative suitability index values**, not employment probabilities. Our rule combines assessed skills, interest alignment, a *synthetic* trend component and gap-related feasibility. We also display readiness and completeness; sparse information is tagged provisional. Weight values are design assumptions needing validation.

## What is a curator?

A person authorised to review changes in labour-market evidence before those changes affect users. In this educational prototype, the curator action is a visible simulated approval button **without authentication**; proper roles and audit logs must be added for real deployment.

## What makes FuturePath different?

The updated result does not erase the original. A saved S1 recommendation retains its own score, snapshot ID, profile and version information. Publishing S2 changes new results but does not rewrite the old stored result. The user previews differences and chooses whether to save a new version.

## How do AI and RunPod fit?

The planned RunPod component would interpret synthetic CV text and suggest skills with excerpts, but the actual local project uses transparent dictionary matching as a fallback. The matching engine itself remains deterministic and explainable. **Never claim that GPU AI is implemented in this package.**

## What remains for a full product?

Real evidence sourcing, verified courses, all 17 SDG mapping justifications, regulated-career qualification research, prerequisite graph planning, user login/privacy controls, authenticated curator, true RunPod integration, calibrated scoring, measured test results and broader accessibility testing.
