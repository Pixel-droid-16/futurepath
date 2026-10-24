# KitaHack — 25 October 2026 Phase 1 submission status

This is a factual handoff for the registered **FuturePath** (Domain 1)
submission. Read the [official example repository](https://github.com/michaelzhngg/SDC_Hackathon_Submission_Template)
and use the organizers' original forms as the submission authority.

## Four expected PDFs

| PDF filename on completion | Evidence / next action |
|---|---|
| `SDC2026_KitaHack_Preliminary.pdf` | Preliminary proposal; source template deadline **25 Oct 2026**. Needs confirmed primary SDG, phone number, workshop eligibility, IP declarations and leader signature |
| `SDC2026_KitaHack_TechDeclaration.pdf` | All APIs, platforms, licenses, datasets, models and **AI-assisted coding tools** disclosed; needs actual sponsor allocation, cloud plan/region, leader signature; cover prints 25 Oct but inside has an unfilled deadline |
| `SDC2026_KitaHack_Replit_POU.pdf` | Genuine Replit screenshots of project, running FastAPI app, and published deployment URL once available; redact all secrets |
| `SDC2026_KitaHack_Runpod_POU.pdf` | Genuine RunPod GPU endpoint, model workload, fictional input/output and FastAPI integration proof; redact all endpoint credentials |

**Do not commit blank or unsigned PDFs with their final filenames.** Use signed
official templates and preserve the organizers' wording. Proof-of-use documents
must show actual tool use, not recreated or fabricated screenshots.

## Team details visible in participant listing

- **Team**: KitaHack (the GitHub README; verify official registration)
- **Project**: FuturePath
- **Domain**: Domain 1
- **Leader**: CHANTHIRAA CHELVAN PASUPATHY
- **Members**: HUA SOON LAI; ADAM BIN AZMI; MUHAMMAD ADAM BIN ROSLAN
- **Affiliation**: Universiti Teknikal Malaysia Melaka
- **Member count**: 4
- **Primary SDG track**: SDG 4, target 4.4 (team confirmed).

Do not put participant email addresses, phone numbers, real CVs, passcodes or
credentials in the public GitHub README. Contact details belong in the submitted
form or organizer portal.

## Current technical evidence

The verified GitHub `main` prior to submission documents included:
- Replit-compatible FastAPI app with the V2 frontend
- RunPod Qwen2.5-3B-Instruct *integration code* (live endpoint verification pending)
- Human-confirmed skill scoring and explainable pathways
- Optional Claude integration; unattended paid calls are disabled without operator opt-in
- GitHub Actions daily Signals snapshot (first actual live scheduled run not yet verified)
- 286 non-browser tests and 19 Chromium journey tests green at commit `35e8c2d`

**A green CI is not a published Replit site or live RunPod proof.** The Replit
connector most recently reported no published deployment. Final review must
check the public judge-facing URL, actual RunPod inference and credential safety.

## Finish in priority order

1. Verify team leader contact, chosen SDG, mandatory workshops, original IP,
   employment IP conflicts and sponsor allocation.
2. Transfer/review answers from editable drafts into the organizer's official
   preliminary and technical declaration forms; obtain actual signatures.
3. Capture sanitized **real** screenshots for Replit and RunPod proof-of-use PDFs.
4. Add live site URL, slide deck/video URL when available, and final PDFs here.
5. Submit via organizer's prescribed mechanism, not GitHub alone unless instructed.

Other references: `docs/SDC_PRELIMINARY_DRAFT.md`,
`docs/SDC_TECH_DECLARATION_DRAFT.md`,
`docs/SDC_SUBMISSION_CHECKLIST.md`, and `submission/README.md`.

## Team confirmations received 24 October 2026

- Primary SDG: **4 — Quality Education**, target **4.4**.
- Mandatory workshops: **all four members completed** (team confirmation; attendance evidence not independently checked).
- Official SDC sponsor-provided resources: **Yes**; **which sponsor, resource, credit amount and use are still unconfirmed**.
- Pre-existing project work: **No**, according to team leader.
- Employment-related IP conflicts: **No**, according to team leader.
- Leader phone: supplied privately for official PDF; intentionally **not included in public GitHub**.
- Outstanding: live Replit URL, RunPod test screenshots, exact third-party licensing, sponsor details, signed official forms, presentation/video links.

## Structure aligned to organizer example

The repository now has `src/main.py` and `src/__init__.py`. `src/main.py` exposes `backend.app:app`, so `python src/main.py` starts the actual existing FastAPI application; it is not a placeholder or a duplicate implementation. The real GPU worker remains in `runpod_worker/handler.py` rather than the sample `runpod/handler.py`. No existing files were moved or deleted.
