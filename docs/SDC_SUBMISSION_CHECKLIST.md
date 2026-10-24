# SDC Submission Mapping — FuturePath

Reviewed against the official SDC Hackathon Submission Template README (2026-10-24). The sample `src/main.py` and `runpod/handler.py` are instructional placeholders; FuturePath uses its own equivalent modules. **This list is a compliance worklist, not a declaration of final submission.**

| SDC README item | FuturePath implementation / location | Before submission |
|---|---|---|
| Project name and one-line overview | `README.md` | Verify team-approved wording |
| Team name, leader, institution, member count | `README.md` team table | Collect official registered details |
| Domain and SDG track | Domain 1; per-role SDG mappings | Select one primary SDG according to organizer instructions |
| GitHub repository URL | README | Confirm submitted public access and `main` revision |
| Working live Replit URL | `.replit`, deployment guide | Publish/test final URL; don't confuse private preview with production |
| RunPod endpoint | `runpod_worker/`, `backend/providers/runpod.py` | Verify genuine GPU test with sanitized evidence |
| Slide deck/demo video | README link table | Team provides links and verifies permissions |
| Problem, solution, key features | README | Keep consistent with actual demo |
| Technical stack | README and docs/ARCHITECTURE.md | Correct for final deployed code |
| Architecture and project structure | README, docs/ARCHITECTURE.md | Keep `backend/app.py` and `runpod_worker/handler.py`; no placeholder replacement |
| Local and Replit startup | `README.md`, `.replit` | Verify dependency install, Python versions and port 5000 in Replit |
| Tested CV/AI model | Backend/RunPod | Test fictional CV and record source counts, model IDs and limitations |
| Automated tests | `tests/`, `tests/browser/` | Rerun on final `main`, record summary and failing/skipped cases |
| Replit proof of use | `submission/` | Complete official PDF using actual screenshots |
| RunPod proof of use | `submission/` | Complete official PDF with real sanitized GPU evidence |
| Preliminary PDF | `submission/` | Complete official form |
| Technology declaration PDF | `submission/` | Complete actual implementation and disclosure fields |
| Challenges, learnings, future work | README | Edit team-authored descriptions and confirm attribution |
| Secrets not committed | `.gitignore`, `.env.example` | Audit Git history and live logs for secret leakage |
| License | LICENSE | Confirm compatibility with imported code/assets |
| Final status | Published Replit / GitHub `main` | Verify same revision, protected demo and working page links |

## Accuracy checks

- Do not describe the local keyword dictionary as model inference.
- Do not claim scanned OCR works without configured image-capable processing.
- Do not claim full private account authentication or persistent individual storage.
- Do not claim the 3-year Signals radar is a verified forecast.
- Distinguish all unit/browser regression tests from live RunPod extraction.
- Do not upload real CVs or sensitive documents into the shared demo.
- Verify every external evidence citation/course link before final claims.

## Final sign-off

- [ ] Registered team details received
- [ ] Primary SDG track chosen
- [ ] Four required PDFs filled from up-to-date official templates
- [ ] Screenshots show the exact final application version
- [ ] Full tests and isolated browser journeys pass
- [ ] Live RunPod/Qwen synthetic smoke test passes
- [ ] Published Replit site shows correct V2 pages and protected demo
- [ ] README and PDFs agree on application capabilities
- [ ] Every external slide/video/demo link is verified
- [ ] Team approves `main` and publication
