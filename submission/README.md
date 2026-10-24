# SDC Hackathon 2026 — Submission Folder

The official [SDC submission-template repository](https://github.com/michaelzhngg/SDC_Hackathon_Submission_Template/tree/main) expects **four PDF documents** here. The supplied template PDFs are examples; obtain the latest editable/fillable forms and rules from the [SDC Participant Resources folder](https://drive.google.com/drive/folders/1xw7c2aN8N-at8hPEULzkcU76e_FFb0Ef) before preparing the final documents.

## Files to provide

| Final filename after replacing TeamName | Purpose | State |
|---|---|---|
| `SDC2026_TeamName_Preliminary.pdf` | Preliminary submission | Pending actual team name, form requirements and completed evidence |
| `SDC2026_TeamName_TechDeclaration.pdf` | Technology declaration | Pending verified team declaration and official fields |
| `SDC2026_TeamName_Replit_POU.pdf` | Replit proof of use | Pending screenshots of **final** project and verified published deployment |
| `SDC2026_TeamName_Runpod_POU.pdf` | RunPod proof of use | Pending sanitized live GPU endpoint evidence, worker setup and integration |

**Do not commit template PDFs under these filenames as if they were completed documents.** Replace `TeamName` using the official naming rules, and redact all API keys, bearer tokens, real CV content, names of demo visitors and unnecessary personal data from screenshots.

## Recommended evidence

- **Replit:** project name, workflow/run command, V2 page or private preview, final published URL (only once active), same code revision as GitHub `main`.
- **RunPod:** Qwen model and GPU workload, serverless endpoint configuration without secrets, a timestamped synthetic input/output test, and FastAPI's validated `provider: runpod` response with separate model/dictionary counts.
- **Technology declaration:** the actual tech stack (FastAPI, V2 JavaScript/HTML, Replit, RunPod, Qwen, optional Claude, SQLite), clearly labelled external packages and AI-assisted development where required.
- **Preliminary:** correct team/domain/SDG, problem, solution and demo evidence meeting the official questions.

## Before submission

Confirm the required primary SDG, registered team name, team leader, members and institutions; verify the official deadline and upload mechanism separately. The GitHub README intentionally uses **TBD** instead of inventing this information.

See [SDC checklist](../docs/SDC_SUBMISSION_CHECKLIST.md) and the [Replit release runbook](../docs/REPLIT_RELEASE.md).
