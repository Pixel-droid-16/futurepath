import asyncio
from unittest.mock import AsyncMock, patch

from backend.services.ai_extraction import extract_suggestions

CV = (
    "I developed Python applications, used SQL databases, "
    "created dashboards in Microsoft Excel, and performed data analysis."
)


def test_runpod_hybrid_adds_missing_dictionary_skills():
    ai_result = [{
        "skill_id": "SK027",
        "name": "Dashboard design",
        "excerpt": "created dashboards in Microsoft Excel",
        "method": "runpod AI suggestion (unconfirmed)",
        "proficiency": None,
    }]

    async def run():
        with patch(
            "backend.services.ai_extraction.runpod_extract",
            new_callable=AsyncMock,
            return_value=ai_result,
        ), patch(
            "backend.services.ai_extraction.integration_status",
            return_value={"runpod_enabled": True, "claude_enabled": True},
        ):
            return await extract_suggestions(CV, "runpod")

    result = asyncio.run(run())
    candidates = result["candidates"]
    by_id = {item["skill_id"]: item for item in candidates}

    assert {"SK001", "SK005", "SK020", "SK027"} <= set(by_id)
    assert len(candidates) == len(by_id)
    assert by_id["SK027"]["method"].startswith("runpod")
    assert by_id["SK005"]["method"] == "dictionary suggestion"
    assert result["provider"] == "runpod"
    assert result["requires_confirmation"] is True
    assert result["stored"] is False


def test_runpod_hybrid_deduplicates_and_preserves_ai_evidence():
    ai_result = [{
        "skill_id": "SK005",
        "name": "Python programming",
        "excerpt": "developed Python applications",
        "method": "runpod AI suggestion (unconfirmed)",
        "proficiency": None,
    }]

    async def run():
        with patch(
            "backend.services.ai_extraction.runpod_extract",
            new_callable=AsyncMock,
            return_value=ai_result,
        ), patch(
            "backend.services.ai_extraction.integration_status",
            return_value={"runpod_enabled": True, "claude_enabled": True},
        ):
            return await extract_suggestions(CV, "runpod")

    result = asyncio.run(run())
    python_skills = [
        item for item in result["candidates"]
        if item["skill_id"] == "SK005"
    ]

    assert len(python_skills) == 1
    assert python_skills[0]["excerpt"] == "developed Python applications"
    assert python_skills[0]["method"].startswith("runpod")



def test_hybrid_rejects_interest_only_skill_mentions():
    cv = "I am interested in Python and passionate about SQL."

    async def run():
        with patch(
            "backend.services.ai_extraction.runpod_extract",
            new_callable=AsyncMock,
            return_value=[],
        ), patch(
            "backend.services.ai_extraction.integration_status",
            return_value={"runpod_enabled": True, "claude_enabled": True},
        ):
            return await extract_suggestions(cv, "runpod")

    result = asyncio.run(run())
    ids = {item["skill_id"] for item in result["candidates"]}

    assert "SK005" not in ids
    assert "SK001" not in ids


def test_explicit_runpod_failure_does_not_claim_ai_success():
    from fastapi import HTTPException
    from backend.ai_providers import IntegrationError

    async def run():
        with patch(
            "backend.services.ai_extraction.runpod_extract",
            new_callable=AsyncMock,
            side_effect=IntegrationError("Simulated RunPod failure"),
        ), patch(
            "backend.services.ai_extraction.integration_status",
            return_value={"runpod_enabled": True, "claude_enabled": True},
        ):
            return await extract_suggestions(CV, "runpod")

    try:
        asyncio.run(run())
    except HTTPException as exc:
        assert exc.status_code == 502
    else:
        raise AssertionError("Expected HTTP 502 for explicit RunPod failure")



def test_dictionary_evidence_has_whole_word_boundaries():
    from backend.services.dictionary import suggest

    cv = (
        "I developed Python applications, used SQL databases, "
        "created dashboards in Microsoft Excel, and performed data analysis."
    )

    expected = {"SK001", "SK005", "SK020"}
    matched = set()

    for item in suggest(cv):
        if item["skill_id"] not in expected:
            continue

        excerpt = item["excerpt"]
        start = cv.find(excerpt)
        assert start >= 0
        end = start + len(excerpt)

        assert start == 0 or not cv[start - 1].isalnum()
        assert end == len(cv) or not cv[end].isalnum()

        matched.add(item["skill_id"])

    assert matched == expected
