# How to Explain Every Part of FuturePath

## The 30-second explanation

"FuturePath is a career intelligence web prototype. Users confirm their skills and proficiency, then a rules-based engine compares those skills against every career profile in `data/roles.json`. We show separate readiness and assessment completeness, future scenarios, skill gaps and learning suggestions. Our evidence approval demo uses two synthetic versions to prove that new data can't silently overwrite an old recommendation."

## Step by step: what the files do

1. `frontend/index.html` — The **skeleton** of the website: sidebar, header, content area, dark-mode control and scenario selector. Think of it as a house's floor plan.
2. `frontend/style.css` — The **appearance**: premium colour palette, rounded cards, grids, responsive sizing, subtle transitions and light/dark colour variables. Think of it as the house's interior design.
3. `frontend/app.js` — The **behaviour**: which screen opens after a click, where scores appear, what happens on a form save, and when to ask the backend for new results. This is the UI controller.
4. `backend/app.py` — The **reception desk/API**: accepts UI requests, reads/writes records in SQLite, parses uploaded synthetic CVs, checks which snapshot is approved, and sends structured answers back.
5. `backend/engine.py` — The **career calculator**. It receives a profile, career requirements, an approved snapshot, skill definitions and learning resource candidates. It returns scores, skill gaps and ranked learning priorities. It does not ask generative AI to invent scores.
6. `backend/semantic.py` — The **local similarity helper**. It loads cached `all-MiniLM-L6-v2` vectors for every career and skill, adds capped related-skill credit and an optional profile-text fit, and never replaces an exact catalogue skill. If the model is unavailable, `backend/text_match.py` provides a keyword fallback.
7. `data/skills.json` — The **skill dictionary**. Each skill has a stable ID; aliases help reconcile different spellings and CV expressions.
8. `data/roles.json` — The **career requirements handbook**. Every role lists its required skills with a proficiency target, importance, classification and an illustrative SDG connection.
9. `data/skill_relations.json` — The **human-reviewed related-skill list**. It adds partial credit for skills such as Dashboard design → Data visualisation and blocks known false friends.
10. `data/semantic_vectors.json` — **Precomputed MiniLM vectors** for all careers and skills. Regenerate with `python scripts/build_semantic_vectors.py` after editing the catalogue.
11. `data/demo_profile.json` — A **fictional learner**, useful for classroom demonstrations.
12. `data/snapshots.json` — Two **fictional evidence states**. S1 begins published; S2 needs manual approval. Never tell judges these are genuine published statistics.
13. `data/learning_resources.json` — 30 **unverified sample records** illustrating the planned course schema; real providers and links must be checked before a final submission.
14. `tests/test_engine.py` — Tests basic requirements, deterministic scoring, unknown proficiency and scenario invariants.
15. `tests/test_api.py` — Simulates save S1 → approve S2 → compare → delete.
16. `requirements.txt` — Lists the external Python packages the computer needs.

## What happens when users click Save Profile?

`app.js` collects inputs and sends JSON to `PUT /api/profile` → `app.py` validates IDs and proficiency 0–5 → SQLite stores the confirmed skill dictionary → frontend retrieves fresh `/api/matches` → `engine.py` recalculates results. Unselected or unassessed skills remain unknown.

## What do 84/100 and 78/100 mean?

They are **illustrative suitability index values**, not employment probabilities. Our rule combines exact catalogue skills, capped credit for human-reviewed related skills, optional profile-text fit from a local sentence model, interest alignment, a *synthetic* trend component and gap-related feasibility. We also display readiness and completeness; sparse information is tagged provisional. Readiness uses exact skills only, so related-skill credit never makes someone look job-ready on its own. Weight values are design assumptions needing validation.

## How does the local sentence model fit?

It is a small supporting signal, not a generative decision-maker. `all-MiniLM-L6-v2` turns career profiles, skills and a person's optional free text (current role, headline, goals) into vectors. Precomputed career/skill vectors live in `data/semantic_vectors.json`; the app uses them to add cautious skill-to-skill credit and a profile-fit score. A human-reviewed `data/skill_relations.json` overrides known related pairs and blocks false friends. Exact catalogue skills still score highest, and the formula on screen shows the contribution. If the model is unavailable, keyword matching takes over and the rest of the score is unchanged.

## What is a curator?

A person authorised to review changes in labour-market evidence before those changes affect users. In this educational prototype, the curator action is a visible simulated approval button **without authentication**; proper roles and audit logs must be added for real deployment.

## What makes FuturePath different?

The updated result does not erase the original. A saved S1 recommendation retains its own score, snapshot ID, profile and version information. Publishing S2 changes new results but does not rewrite the old stored result. The user previews differences and chooses whether to save a new version.

## How do AI and RunPod fit?

The planned RunPod component would interpret synthetic CV text and suggest skills with excerpts, but the actual local project uses Claude (when configured) or transparent dictionary matching as a fallback. It also uses a **local, non-generative** MiniLM sentence model for similarity, with cached vectors and a keyword fallback. The matching engine itself remains deterministic and explainable. **Never claim that GPU AI is implemented in this package.**

## What remains for a full product?

Real evidence sourcing, verified courses, all 17 SDG mapping justifications, regulated-career qualification research, prerequisite graph planning, user login/privacy controls, authenticated curator, true RunPod integration, calibrated scoring, measured test results and broader accessibility testing.
