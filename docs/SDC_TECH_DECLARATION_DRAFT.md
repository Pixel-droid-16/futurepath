# SDC 2026 — Technical & Tools Declaration: FuturePath (WORKING DRAFT)

**Official XMUM AI Club technical declaration template.** Its deadline field is left blank, so confirm the event's current submission date and method. Transfer approved content to the organizer Word form and export `SDC2026_<RegisteredTeamName>_TechDeclaration.pdf`.

## 1. Team & project overview

Team name, leader name, leader email and phone, university: **[TEAM TO COMPLETE IN OFFICIAL FORM]**.

Project name: **FuturePath**. Domain: **1**. Repository: https://github.com/Pixel-droid-16/futurepath

Live prototype: **[INSERT VERIFIED PUBLISHED REPLIT URL — NOT A PRIVATE PREVIEW]**

## 2. Architecture & technology stack

### 2.1 System architecture overview (maximum 200 words)

FuturePath serves the team's V2 browser interface through a Python FastAPI backend hosted on Replit. It accepts fictional profile input or synthetic CV uploads, extracts text from TXT, DOCX and PDFs, and calls a Qwen2.5-3B-Instruct model on a GPU-backed RunPod Serverless endpoint to suggest skills. A local dictionary supplements model output; an optional Claude API can read scanned PDFs. Evidence validation rejects unsupported skill IDs and ungrounded excerpts. Users explicitly approve skills and proficiency before deterministic role matching.

JSON files hold the canonical skill, career, course and signal catalogues. SQLite stores fictional demo profiles and signal audit history. The backend calculates explainable readiness, trend-informed demand and learning priorities; the frontend displays career choices, SDGs and hypothetical Moderate/Fast AI scenarios. Replit Secrets keep external credentials out of source control. The public demonstration uses a shared password and disables administrative signal refresh and curator approval. It is not a private account or durable production-data service.

### 2.2 Languages, frameworks and libraries

| Name / version range | Usage | License / terms to verify |
|---|---|---|
| Python 3.12 | Backend | Python Software Foundation License |
| FastAPI (`>=0.110,<1`) | HTTP API | MIT (confirm exact release) |
| Pydantic (`>=2,<3`) | Request validation | MIT (confirm exact release) |
| uvicorn (`>=0.27,<1`) | ASGI server | BSD-3-Clause (confirm exact release) |
| httpx (`>=0.27,<1`) | External API calls | BSD-3-Clause (confirm exact release) |
| pypdf (`>=4,<7`) | Extract text PDF | BSD-3-Clause (confirm) |
| python-docx (`>=1.1,<2`) | DOCX extraction | MIT (confirm) |
| Playwright (`>=1.55,<2`) | Browser tests | Apache-2.0 (confirm) |
| Pytest / pytest-asyncio | Automated tests | Confirm versions and licenses |
| V2 HTML/CSS/JS assets | UI and interactions | Team-created vs imported assets must be checked |

## 3. APIs & cloud services

### 3.1 External APIs

| Provider | Purpose | Access tier |
|---|---|---|
| RunPod API | GPU inference of Qwen skill suggestions | **Team to confirm personal/paid/sponsor credit source** |
| Anthropic API (optional) | Claude-based scanned PDF reading and optionally trend tagging | **Team to confirm paid/tier and whether exercised in final demo** |
| Public Google News / arXiv / Hugging Face feeds | Dated news/research/context on employment and skills | Public feeds; respect each provider's terms |
| Linked course/provider websites | Resource links shown to users | No backend transactional integration claimed |

### 3.2 Cloud platforms & deployment

| Service | Purpose | Plan / region |
|---|---|---|
| Replit | Python FastAPI hosting, Secrets, development workflow | **Team to confirm Autoscale deployment/region** |
| RunPod Serverless | GPU hosting for Qwen model | **Team to confirm endpoint hardware/region** |
| SQLite | Fictional demonstration storage (not hosted database as a service) | Disposable application filesystem |

## 4. AI models & datasets

### 4.1 AI models

| Model | Provider | Usage | License / terms |
|---|---|---|---|
| Qwen2.5-3B-Instruct | Qwen/Alibaba via RunPod | Pretrained GPU inference; no fine-tuning claimed | Check official Qwen license/model card and deployed model ID |
| Claude (actual configured model must be verified) | Anthropic API | Optional scanned PDF / signal tagging | Anthropic API terms; model name not hard-coded as evidence of invocation |
| No team-trained model | — | No training/fine-tuning claimed | — |

### 4.2 Datasets

| Dataset | Source | Type | Personal data? |
|---|---|---|---|
| Career-skill requirements and canonical skills | Team-curated local `data/roles.json`, `data/skills.json`; inspect imported portions | Curated and partly synthesized | No real CVs in the catalogue |
| Dated signal baseline | `data/signals.json`, WEF/ILO/other sources, imported LaluanKu mapping | Mixed public-source / team-interpreted | No user personal data |
| Learning catalogues | `data/courses.json`, `data/extra_courses.json` | Public links, team curated | No |
| RIASEC interest mappings | O*NET-derived interest references in career records | Third-party | No direct user records in references |
| Demo/example profiles | `data/demo_profile.json` and synthetic tests | Fictional | No |
| User-uploaded CV (ephemeral request) | User supplied to current request and external model when selected | **Synthetic only for public demo** | Real CVs could contain personal data; prohibited from shared deployment |

Confirm exact upstream licenses, reuse permissions, attribution, and dates before signing.

### 4.3 AI-assisted development tools

**YES — disclosure required.** Verified development tooling includes ChatGPT and Replit Agent. Other coding assistants used by team members: **[CONFIRM]**. These tools helped with planning, code edits, integration, test generation and documentation; the team must review ownership, licenses and output correctness.

**Responsibility statement (maximum 100 words):**

We reviewed AI-assisted code through readable commits, targeted regression tests and an isolated browser suite. Skills returned by models are validated against allowed catalogue IDs and literal supporting CV excerpts, and the user confirms any suggestion before career scoring. Automated tests do not prove model correctness, so live synthetic RunPod smoke tests are recorded separately. The team maintains responsibility for security, source attribution, documentation, factual claims and the final submission.

## 5. Sponsor-provided resources

**[TEAM MUST CHOOSE YES/NO]** for each sponsor resource, including Replit, RunPod, GenAI/API credits, mentoring or data. Distinguish use of a public commercial provider from receipt of an actual sponsor allocation. Do not claim sponsored credits unless verified.

**Replaceability statement (maximum 100 words):**

RunPod currently hosts the Qwen inference workload required for the hackathon architecture. Replit hosts the main FastAPI application. At the software-design level, equivalent hosting and GPU providers could be substituted, but doing so would require deployment, credential and reliability changes. The local skill dictionary provides reduced-functionality fallback; it is not equivalent to GPU-assisted extraction. The team will state which resources were sponsor-provided after checking account ownership and actual credit allocation.

## 6. Security, privacy & responsible use

### 6.1 Data handling (maximum 150 words)

FuturePath's current demo accepts fictional CV documents, names and career-profile information. Uploaded documents are read for extraction; when AI is selected, extracted text is transmitted to RunPod or, for image-only PDFs, the document may be sent to Anthropic. Exact external retention depends on the provider's service terms and account configuration; no zero-retention guarantee is claimed. The backend stores approved fictional profiles and dated Signals refresh records in SQLite. Development and public demo databases may use temporary storage and can reset across restarts. There are no private user accounts or per-person access controls: users sharing the judge password share the demo profiles. Server-side secrets are held in Replit Secrets. Published demo mode disables curator and manual feed-refresh actions. Real CVs and personal data must **not** be uploaded to this shared prototype.

### 6.2 Limitations and risks (maximum 150 words)

Qwen and Claude can omit skills or make unsupported inferences; output is validated against catalogue IDs and quoted evidence, with final human confirmation required. Image-only PDFs depend on an optional Claude API, while poor text layers or DOCX layouts can lose context. RunPod cold starts, service rates, API billing and external network failures affect response time. The dictionary fallback may miss context. Labour trend links and proficiency weights are modelling judgements, not calibrated hiring probabilities. The curated sources may age, and course prices or availability may change. The demo uses a shared password and ephemeral SQLite rather than private accounts or durable storage; it must use fictional data. Mitigations include bounded request sizes, validation, clear source attributions, protected administrative operations, dated sources, regression tests and explicit limitations.

## 7. Compliance checklist

- [ ] All APIs, model versions, cloud services, datasets and licenses verified and declared.
- [ ] No keys, passwords or real personal CVs in repo, demo screenshots or this document.
- [ ] Third-party and pre-existing work attributed and authorized.
- [ ] AI-assisted coding/design/documentation use disclosed.
- [ ] Actual sponsor credits/resources confirmed.
- [ ] Final published Replit link tested and accessible to judges.
- [ ] Every official form field and word limit checked by team.

## 8. Declaration

Name/signature/date of team leader: **[REQUIRED IN OFFICIAL FORM AFTER REVIEW]**.

This is a working draft, not a signed claim that all declarations are complete.


## Team-confirmed declarations (24 October 2026)

- Team: **KitaHack**; project: **FuturePath**; Domain 1; primary **SDG 4, target 4.4**.
- Team leader: **CHANTHIRAA CHELVAN PASUPATHY**; four members at **Universiti Teknikal Malaysia Melaka**.
- All four completed mandatory workshops: **YES (leader-confirmed)**.
- SDC sponsor-provided resources used: **YES (leader-confirmed)**; **exact sponsor, allocation and service still to verify**.
- Project work created before hackathon: **NO (leader-confirmed)**.
- Employment-related IP conflicts: **NO (leader-confirmed)**.
- Leader's phone was supplied privately and intentionally excluded from public GitHub files.
- This is still a draft: actual leader signature, sponsor details, production URL, and real Replit/RunPod evidence are outstanding.
