"""RunPod Serverless adapter with bounded queue polling and grounded skill validation."""
import asyncio
import logging
import json
import os
import re
import time
from urllib.parse import urlparse

import httpx

from .validation import SYSTEM, prompt_for, validate_candidates, IntegrationError

# A cold-started GPU may take longer than RunPod's synchronous wait window.
MAX_POLL_SECONDS = 210
POLL_INTERVAL_SECONDS = 3


def runpod_model():
    """Name shown to users for the RunPod worker's model. Keep RUNPOD_MODEL_ID equal to the worker's MODEL_ID."""
    return os.getenv("RUNPOD_MODEL_ID", "").strip() or "Qwen/Qwen2.5-3B-Instruct"


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



def runpod_prompt(text, skills):
    """Provide CV evidence first, with a compact skill catalogue."""
    import json

    catalogue = [
        {"id": s["id"], "name": s["name"], "aliases": s.get("aliases", [])[:3]}
        for s in skills
    ]

    return (
        "Return ONLY compact JSON: "
        "{\"candidates\":[{\"skill_id\":\"allowed-id\",\"excerpt\":\"literal CV quote\"}]}. "
        "At most 8 distinct skills; each quote 3-80 characters copied exactly from CV TEXT. "
        "Prioritize demonstrated tools and work; interests/goals are not skills evidence. "
        "Use only allowed IDs. No markdown, explanations, proficiency or contact details. "
        "If none is supported return {\"candidates\":[]}. "
        "\n\nCV TEXT:\n"
        + text
        + "\n\nALLOWED SKILLS:\n"
        + json.dumps(catalogue, ensure_ascii=False, separators=(",", ":"))
    )


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
    if not isinstance(payload,dict):
        raise IntegrationError("RunPod returned an unexpected envelope")

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
        if not isinstance(payload,dict):
            raise IntegrationError("RunPod returned an unexpected envelope")

    if payload.get("status") != "COMPLETED":
        raise IntegrationError("RunPod job did not complete")
    output = payload.get("output")

    try:
        return validate_candidates(output, cv, skills, "runpod")
    except IntegrationError as error:
        logger = logging.getLogger(__name__)
        logger.error(
            "RunPod extraction validation failed: job_id=[MASKED], "
            "status=COMPLETED, error_class=%s, output_type=%s, output_length=%s",
            type(error).__name__,
            type(output).__name__,
            len(str(output)) if output is not None else 0,
        )
        raise


async def runpod_extract(text, skills, client=None):
    key = os.getenv("RUNPOD_API_KEY")
    if not key:
        raise IntegrationError("RunPod key not configured")
    url = runpod_url()
    headers = {"Authorization": "Bearer " + key, "Content-Type": "application/json"}
    body = {"input": {"task": "extract_skills", "system": SYSTEM, "prompt": runpod_prompt(text, skills)},
            "policy": {"ttl": 600000}}
    if client is not None:
        return await _extract_with_client(client, url, headers, body, text, skills)
    async with httpx.AsyncClient(timeout=httpx.Timeout(110.0, connect=15.0)) as c:
        return await _extract_with_client(c, url, headers, body, text, skills)
