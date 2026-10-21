# FuturePath Architecture (MVP)

```text
Browser — frontend/index.html + frontend/app.js + frontend/style.css
          | HTTP /api/...
          v
FastAPI — backend/app.py --------> SQLite local demo database
          |                           - profiles
          |                           - evidence snapshot state
          |                           - saved recommendation history
          | uses
          v
Pure matching engine — backend/engine.py
          |                  \
          v                   v
Canonical data/*.json    Synthetic S1/S2 snapshots
```

**Request flow:** Browser calls `/api/matches`; app.py reads the confirmed demo profile and active approved snapshot; engine.py calculates all career recommendations; app.py returns JSON; app.js displays career cards, components, gaps and learning steps.

**CV flow:** Upload synthetic text PDF/DOCX/TXT → backend parses text → dictionary matcher suggests skills with excerpts → UI displays candidates → user chooses level 0–5 and saves → only saved skills enter matching. RunPod AI is a **planned optional replacement of the extraction adapter**, NOT currently connected.

**Evidence flow:** S1 published → save original version → S2 pending → curator approves S2 → matches now use S2 → old saved recommendation still contains S1 version and its frozen original result → preview computes with the saved profile, same scenario and scoring version → user may explicitly save another result. All evidence content is synthetic and explicitly marked.

**Scoring:** `0.45 * assessed-readiness + 0.20 * interest-alignment + 0.20 * synthetic trend + 0.15 * feasibility`. Readiness is a weighted mean of confirmed proficiency relative to role requirements. Assessment completeness separately quantifies weighted requirement coverage. This demonstration does not calibrate the formula for real employment outcomes.

**Known limitations:** This mini-stack uses native JS and SQLite for learning and fast local execution. The longer-term architecture proposed React/TypeScript, PostgreSQL, RunPod, stronger data provenance and authenticated curation. It would be misleading to claim these are already implemented.
