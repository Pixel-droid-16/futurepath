"""RunPod Serverless adapter with bounded queue polling and grounded skill validation."""
import asyncio
import os
import re
import time
from urllib.parse import urlparse

import httpx

from .validation import SYSTEM, prompt_for, validate_candidates, IntegrationError

# A cold-started GPU may take longer than RunPod's synchronous wait window.
MAX_POLL_SECONDS = 210
POLL_INTERVAL_SECONDS = 3


def runpod_url():
    endpoint_id = os.getenv("RUNPOD_ENDPOINT_ID", "").strip()
    custom = os.getenv("RUNPOD_ENDPOINT_URL", "").strip()
    if endpoint_id:
        if not re.fullmatch(r"[A-Za-z0-9_-]{3,100}", endpoint_id):
            raise IntegrationError("Invalid RunPod endpoint ID")
        return f"https://api.runpod.ai/v2/{endpoint_id}/runsync?wait=90000"
    if custom:
        p = urlparse(custom)
        if p.scheme != "https" or not p.hostname or p.username or p.password:
            raise IntegrationError("RunPod URL must be a valid HTTPS endpoint")
        if p.hostname != "api.runpod.ai":
            raise IntegrationError("Only api.runpod.ai endpoint URLs supported")
        if p.query or p.fragment:
            raise IntegrationError("RunPod URL must not contain a query or fragment")
        path = p.path.rstrip("/")
        if path.endswith("/runsync"):
            return custom
        if path.endswith("/run"):
            return custom[:-4] + "/runsync"
        return custom.rstrip("/") + "/runsync"
    raise IntegrationError("RunPod endpoint ID not configured")


def _status_url(sync_url, job_id):
    if not isinstance(job_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{3,160}", job_id):
        raise IntegrationError("RunPod returned an invalid job ID")
    return sync_url.split("/runsync", 1)[0] + "/status/" + job_id


async def _extract_with_client(client, url, headers, body, cv, skills):
    resp = await client.post(url, headers=headers, json=body)
    if resp.status_code >= 400:
        raise IntegrationError(f"RunPod HTTP {resp.status_code}; check endpoint and worker logs")
    try:
        payload = resp.json()
    except ValueError as e:
        raise IntegrationError("RunPod returned invalid JSON") from e

    # runsync is allowed to return IN_QUEUE/IN_PROGRESS at its wait limit.
    start = time.monotonic()
    while payload.get("status") in ("IN_QUEUE", "IN_PROGRESS"):
        if time.monotonic() - start >= MAX_POLL_SECONDS:
            raise IntegrationError("RunPod job is still processing; retry status instead of submitting duplicate work")
        status_url = _status_url(url, payload.get("id"))
        await asyncio.sleep(POLL_INTERVAL_SECONDS)
        resp = await client.get(status_url, headers=headers)
        if resp.status_code >= 400:
            raise IntegrationError(f"RunPod status HTTP {resp.status_code}")
        try:
            payload = resp.json()
        except ValueError as e:
            raise IntegrationError("RunPod status returned invalid JSON") from e

    if payload.get("status") != "COMPLETED":
        raise IntegrationError("RunPod job did not complete: " + str(payload.get("status", "unknown")))
    return validate_candidates(payload.get("output"), cv, skills, "runpod")


async def runpod_extract(text, skills, client=None):
    key = os.getenv("RUNPOD_API_KEY")
    if not key:
        raise IntegrationError("RunPod key not configured")
    url = runpod_url()
    headers = {"Authorization": "Bearer " + key, "Content-Type": "application/json"}
    body = {"input": {"task": "extract_skills", "system": SYSTEM, "prompt": prompt_for(text, skills)},
            "policy": {"ttl": 600000}}
    if client is not None:
        return await _extract_with_client(client, url, headers, body, text, skills)
    async with httpx.AsyncClient(timeout=httpx.Timeout(110.0, connect=15.0)) as c:
        return await _extract_with_client(c, url, headers, body, text, skills)
