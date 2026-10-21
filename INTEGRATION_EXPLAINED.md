# Explain the integrations to your group

1. **Browser:** The original v2 mockup stays visually unchanged. A separate `/ai-lab` form collects a *synthetic* CV paragraph and the provider selection. It sends JSON to `/api/ai/skills`.
2. **Python API:** `backend/app.py` verifies the selected provider and calls `backend/ai_providers.py`. `auto` tries RunPod (only if configured), then Claude, then a local dictionary.
3. **Claude:** Sends a system instruction and the allowed canonical skill catalogue to Anthropic's `/v1/messages`. The model suggests skill IDs and exact evidence snippets. The key stays on the server.
4. **RunPod:** Sends the same task to an authenticated `/runsync` RunPod Serverless endpoint. A separately deployed GPU worker runs an instruction model and returns generated JSON-like text.
5. **Validation:** The backend parses the response, keeps only allowed skill IDs with exact substrings of the CV, deduplicates skills and removes any proficiency predictions. Invalid model outputs are rejected.
6. **Review:** The form presents suggested skills, a checkbox for user confirmation and a self-assessed 0–5 level. Unchecked skills cannot enter the user profile.
7. **Persistence:** Only explicit user-confirmed levels are stored in the local demo profile. They can then influence backend career matching. The original mockup's hard-coded calculations are not yet linked.
8. **Scenario separation:** Moderate and Rapid AI are independent deterministic scenario calculations in `backend/scenarios.py`. Claude/RunPod extract CV skills; they do not invent score changes.
9. **What is live?** Provider adapters perform real network calls **when credentials and a deployed endpoint exist**. Included automated tests are mocked and therefore cannot confirm connection to your account.
