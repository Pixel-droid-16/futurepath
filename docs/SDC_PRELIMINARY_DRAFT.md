# SDC 2026 — Preliminary Project Proposal: FuturePath (WORKING DRAFT)

**Based on the official XMUM AI Club Word template in the Participant Resources folder. Submission deadline printed on that template: 25 October 2026.**

**Not a signed/completed submission.** Transfer the approved answers into the organizer's editable Word form, preserve its tables and limits, obtain team declarations/signature, then export a verified PDF named `SDC2026_<RegisteredTeamName>_Preliminary.pdf`.

## 1. Team and project overview

| Official field | Proposed answer |
|---|---|
| Team Name | **KitaHack (team-confirmed)** |
| Selected Domain | Domain 1 |
| Selected SDG Track | **SDG 4 — Quality Education, target 4.4 (team-confirmed)** |
| Project / Solution Name | FuturePath |
| Name (Leader) | **CHANTHIRAA CHELVAN PASUPATHY** |
| Email & Phone (Leader) | **[PRIVATE CONTACT INFORMATION REQUIRED IN OFFICIAL FORM ONLY]** |
| University Affiliation(s) | **Team confirmed** |
| Number of Team Members | **Team confirmed** |

## 2. Executive summary and problem statement

### 2.1 The problem context (maximum 250 words)

Students, fresh graduates and working professionals often struggle to translate their education and experience into clear, evidence-based career choices. Job titles alone do not show which skills a person has demonstrated, how proficient they are, what competencies a role requires, or which learning resources would address the gap. Rapid adoption of AI and automation adds uncertainty, while unsourced career advice can overstate future job prospects.

The World Economic Forum's *Future of Jobs Report 2025* estimates that 39% of workers' existing skill sets will change or become outdated during 2025–2030, based on its global employer survey. This figure reflects global employer expectations, not a measured Malaysian unemployment rate or a FuturePath outcome. It illustrates the importance of accessible reskilling guidance.

FuturePath addresses the need for transparent, personalized career exploration: users should be able to identify relevant competencies, review the evidence behind suggestions, compare potential roles, and choose practical learning steps without being given invented employment probabilities.

Source: https://www.weforum.org/publications/the-future-of-jobs-report-2025

### 2.2 The proposed AI solution (maximum 300 words)

FuturePath is a browser-based, review-first career and reskilling assistant. Users enter a fictional profile or upload a synthetic CV in TXT, DOCX or text-based PDF format. A GPU-backed Qwen2.5-3B-Instruct model on RunPod suggests skills mapped to a canonical catalogue, while a local dictionary supplements model suggestions. Each skill includes supporting CV evidence, and **nothing is scored until the user confirms it and selects proficiency**. An optional Claude provider can examine image-only PDFs if configured.

A modular FastAPI backend on Replit compares the confirmed skills with documented role requirements and dated trend signals. The V2 interface shows explainable career rankings, missing and partially assessed skills, a Skills Radar, course-linked learning pathways, relevant UN SDGs and two hypothetical AI-adoption scenarios. An optional RIASEC interest quiz adds an interest dimension without hiding alternative careers. Curated evidence and conservative modelling are presented as estimates, not employment forecasts.

The prototype currently contains 44 careers, 110 catalogue skills, 36 curated baseline signal entries and 111 course entries. It uses cloud hosting, external model APIs, JSON/SQLite data architecture, input validation and browser regression testing. Its initial launch is restricted to synthetic examples because the shared demo is not a private user-account system. The next evaluation stage measures grounded extraction quality, task completion and safe deployment.

### 3. Technical architecture and implementation

#### 3.1 Conceptual tech stack

```text
Web browser (V2 HTML/CSS/JS) -> Replit / FastAPI
  -> text/PDF/DOCX parsing -> RunPod Serverless / Qwen GPU
  -> optional Claude PDF provider -> evidence validation
  -> user-confirmed skills -> explainable matching + RIASEC
  -> sourced signals / skill gaps -> learning pathway + SDG mapping
  -> JSON catalogues and SQLite fictional-demo state
```

Languages/libraries: Python 3.12, FastAPI, Pydantic, JavaScript, HTML/CSS, pypdf, python-docx, httpx, pytest, Playwright. Use Replit Secrets for API keys; no secret enters the frontend. Hosting uses Replit, GPU inference uses RunPod. The demo database is SQLite, not a deployed production account system.

**Official sponsor-provided platform/API used? [TEAM MUST CONFIRM whether the Replit/RunPod account/credits were provided by sponsors, or the team used personal plans. Do not assume.]**

#### 3.2 Design-thinking and deployment strategy (maximum 200 words)

The design starts with two user journeys: students and fresh graduates seeking career discovery, and working professionals planning a transition or reskilling. A teammate's V2 visual design provides approachable onboarding, skill-review cards, explainable result panels and course plans. The product separates suggested skills from confirmed skills to reduce unsupported recommendations.

The architecture uses independently editable frontend pages, backend routers, AI providers and datasets. This makes changes reviewable and allows a dictionary fallback when a GPU endpoint is unavailable. We test with fictional CVs to cover common technical skills, education, projects and uncertain evidence. Pytest validates scoring, provider contracts and security; Chromium tests exercise onboarding, mobile navigation, the interest quiz and protected synthetic-demo access.

Replit hosts the application while RunPod handles model inference. Final deployment requires the current GitHub code, secure environment settings, live endpoint smoke tests and user-journey checks. Real personal CV storage is out of scope for the hackathon demo.

## 4. Preliminary environmental and SDG impact framework

**Recommended primary SDG (requires team confirmation): SDG 4, target 4.4**, increasing relevant technical and vocational skills for employment and entrepreneurship. Secondary connections include SDG 8 (decent work) and SDG 9 (innovation).

| Required metric | Responsible proposal |
|---|---|
| Target SDG sub-target | SDG 4.4 — increase the number of youth and adults with relevant skills for employment, decent jobs and entrepreneurship |
| Current problem baseline | **Context benchmark:** WEF 2025 global employer survey expects 39% of workers' skills to change by 2030. **App-specific baseline not yet measured:** record manual task completion time and baseline skill-grounding accuracy on a labelled fictional CV set before claiming impact. |
| Core measurable KPI | Evidence-grounded skill suggestion precision = validated correct suggested skills / all suggested skills; and median minutes for a participant to produce a confirmed skills-to-learning plan |
| Phase 2 impact target | **Proposed, not achieved:** at least 80% grounded skill precision on 20 pre-labelled fictional CVs and at least 25% less median plan-creation time against a measured manual baseline |
| Validation | Freeze synthetic test set before evaluation; double-review ambiguous examples; report sample size, median, exclusions, model fallback and incomplete tasks |

**Critical:** A WEF global benchmark is not an app impact baseline. The team must supply the actual Phase 2 baseline measurement before presenting a percentage improvement as achieved. Never claim FuturePath has reduced unemployment or proven training outcomes.

## 5. Eligibility and readiness checklist

- [ ] All members completed mandatory **GenAI, Database and Cloud Deployment workshops** (team to verify).
- [ ] Team-approved SDG track and real, cited problem.
- [ ] Functional, deployed prototype verified through the public/private judge link.
- [ ] All form fields completed within word limits.
- [ ] Team leader reviews/signs the official version.

## 6. IP and originality declaration — must be decided by the team

**6.1 Pre-existing/prior-owned work:** [YES/NO TO CONFIRM]. Record any V2 interface, datasets, LaluanKu import or code that pre-dated the hackathon, the relevant teammate(s) and permission to submit. Do not assert that everything began during the event without checking the timeline.

**6.2 Third-party code, data and models:** **YES.** Examples: FastAPI, pypdf, python-docx, Playwright, Qwen2.5-3B-Instruct, optional Claude, WEF/ILO/O*NET-related sources, provider courses and imported data. Confirm licenses and full attribution in the technology declaration.

**6.3 Employment-related IP conflicts:** [YES/NO TO CONFIRM WITH EACH TEAM MEMBER]. Include relevant details if yes.

## 7. Declaration

Leader signature: **[SIGNATURE REQUIRED]**

Date: **[ACTUAL SIGNING DATE REQUIRED]**

This draft is not yet a legally effective declaration or a final submission.


## Team-confirmed declarations (24 October 2026)

- Team: **KitaHack**; project: **FuturePath**; Domain 1; primary **SDG 4, target 4.4**.
- Team leader: **CHANTHIRAA CHELVAN PASUPATHY**; four members at **Universiti Teknikal Malaysia Melaka**.
- All four completed mandatory workshops: **YES (leader-confirmed)**.
- SDC sponsor-provided resources used: **YES (leader-confirmed)**; **exact sponsor, allocation and service still to verify**.
- Project work created before hackathon: **NO (leader-confirmed)**.
- Employment-related IP conflicts: **NO (leader-confirmed)**.
- Leader's phone was supplied privately and intentionally excluded from public GitHub files.
- This is still a draft: actual leader signature, sponsor details, production URL, and real Replit/RunPod evidence are outstanding.
