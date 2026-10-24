"""Offline RunPod envelope, truncation and cost-safe fallback contracts."""
import json
import logging

import httpx
import pytest
from fastapi import HTTPException

from backend.providers.runpod import runpod_extract, runpod_prompt
from backend.providers.validation import IntegrationError, validate_candidates
from backend.services import ai_extraction

SK = [{'id': 'sql', 'name': 'SQL querying', 'aliases': ['SQL']}]
CV = 'I wrote SQL queries, Python scripts and built Excel dashboards'
ONE = {'skill_id': 'sql', 'excerpt': 'SQL queries'}
GOOD = {'candidates': [ONE]}
PARTIAL = '{"candidates":[' + json.dumps(ONE) + ',{"skill_id":"unfinished'


@pytest.fixture(autouse=True)
def synthetic_config(monkeypatch):
    monkeypatch.setenv('RUNPOD_API_KEY', 'offline-test-only')
    monkeypatch.setenv('RUNPOD_ENDPOINT_ID', 'offline-test-endpoint')


async def adapt(output, skills=SK, envelope=None):
    requests = []

    def handler(request):
        requests.append(request)
        assert request.method == 'POST'
        return httpx.Response(200, json=envelope if envelope is not None else {
            'id': 'private-test-job', 'status': 'COMPLETED', 'output': output,
        })

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await runpod_extract(CV, skills, client)
    assert len(requests) == 1
    return result


@pytest.mark.asyncio
@pytest.mark.parametrize('output', [
    GOOD,
    {'text': json.dumps(GOOD)},
    {'output': {'result': {'response': {'text': json.dumps(GOOD)}}}},
    {'generated_text': [{'role': 'user', 'content': 'untrusted prompt'},
                        {'role': 'assistant', 'content': json.dumps(GOOD)}]},
    {'choices': [{'message': {'role': 'assistant', 'content': json.dumps(GOOD)}}]},
    {'content': [{'type': 'text', 'text': json.dumps(GOOD)}]},
    {'text': '```json\n' + json.dumps(GOOD) + '\n```'},
    {'text': 'Here is the result:\n' + json.dumps(GOOD) + '\nExplanation.'},
    {'text': PARTIAL},
    {'text': '{"candidates":[' + json.dumps(ONE)},
    {'text': '{"candidates":[' + json.dumps(ONE) + ','},
    {'text': '{"candidates":[' + json.dumps(ONE) + ']'},
], ids=['object', 'worker-text', 'nested', 'hf-chat', 'choices', 'content-block',
        'fenced', 'explanation', 'cut-string', 'cut-after-object', 'cut-after-comma',
        'cut-root-brace'])
async def test_mocked_runpod_supported_responses(output):
    result = await adapt(output)
    assert [c['skill_id'] for c in result] == ['sql']
    assert result[0]['excerpt'] == 'SQL queries'
    assert result[0]['proficiency'] is None


@pytest.mark.asyncio
@pytest.mark.parametrize('output', [
    {'text': 'not JSON'},
    {'candidates': 'wrong type'},
    {'unexpected': GOOD},
    {'text': '{"candidates":[{"skill_id":"sql","excerpt":"SQL'},
    {'text': '{"candidates":[' + json.dumps(ONE) + ',BROKEN'},
    {'text': '{"candidates":[' + json.dumps(ONE) + ' garbage'},
    {'text': '{"candidates":[{"skill_id":"unknown","excerpt":"SQL queries"},'},
    {'text': '{"candidates":[{"skill_id":"sql","excerpt":"invented"},'},
    {'generated_text': [{'role': 'user', 'content': json.dumps(GOOD)}]},
    {'text': 'null'},
    {'text': json.dumps('scalar')},
    {'text': 'x' * 100_001},
    {'text': '{"candidates":[' + json.dumps(ONE) + ',{"skill_id":BAD'},
], ids=['not-json', 'wrong-list', 'unknown-wrapper', 'no-complete-object',
        'malformed-tail', 'missing-delimiter', 'unknown-id', 'ungrounded',
        'prompt-echo', 'null', 'scalar', 'oversized', 'malformed-object'])
async def test_mocked_runpod_rejects_irrecoverable_responses(output):
    with pytest.raises(IntegrationError):
        await adapt(output)


@pytest.mark.asyncio
async def test_invalid_envelope_is_controlled():
    with pytest.raises(IntegrationError):
        await adapt(None, envelope=['not a RunPod envelope'])


@pytest.mark.asyncio
async def test_sanitized_log_never_contains_output_or_job(caplog):
    marker = 'PRIVATE-OUTPUT-MUST-NOT-BE-LOGGED'
    with caplog.at_level(logging.ERROR), pytest.raises(IntegrationError):
        await adapt({'text': marker})
    assert marker not in caplog.text and 'private-test-job' not in caplog.text
    assert 'job_id=[MASKED]' in caplog.text
    assert 'status=COMPLETED' in caplog.text
    assert 'error_class=IntegrationError' in caplog.text
    assert 'output_type=dict' in caplog.text and 'output_length=' in caplog.text


def test_recovery_does_not_weaken_grounding_or_claude():
    candidates = [
        ONE, ONE, {'skill_id': 'unknown', 'excerpt': 'SQL queries'},
        {'skill_id': 'sql', 'excerpt': 'invented experience'},
    ]
    text = '{"candidates":' + json.dumps(candidates)[:-1] + ',{"excerpt":"cut'
    result = validate_candidates(text, CV, SK, 'runpod')
    assert len(result) == 1 and result[0]['excerpt'] == 'SQL queries'
    with pytest.raises(IntegrationError):
        validate_candidates(text, CV, SK, 'claude')
    assert validate_candidates({'candidates': []}, CV, SK, 'runpod') == []


def test_recursive_wrappers_are_bounded():
    output = GOOD
    for _ in range(30):
        output = {'text': output}
    with pytest.raises(IntegrationError):
        validate_candidates(output, CV, SK, 'runpod')


def test_prompt_is_concise_and_output_bounded():
    prompt = runpod_prompt(CV, SK)
    assert 'At most 8' in prompt and '3-80 characters' in prompt
    assert 'ONLY compact JSON' in prompt and CV in prompt
    assert 'proficiency or contact details' in prompt


@pytest.mark.asyncio
@pytest.mark.parametrize('provider', ['auto', 'runpod'])
async def test_service_invalid_mocked_runpod_never_calls_claude(monkeypatch, provider):
    async def invalid(text, skills):
        return await adapt({'text': 'invalid JSON'}, skills)

    async def forbidden(*args, **kwargs):
        pytest.fail('Text failure must not call optional paid Claude')

    monkeypatch.setattr(ai_extraction, 'runpod_extract', invalid)
    monkeypatch.setattr(ai_extraction, 'claude_extract', forbidden)
    monkeypatch.setattr(ai_extraction, 'claude_extract_pdf', forbidden)
    monkeypatch.setattr(ai_extraction, 'claude_configured', lambda: True)
    if provider == 'runpod':
        with pytest.raises(HTTPException) as error:
            await ai_extraction.extract_suggestions(CV, provider)
        assert error.value.status_code == 502
        assert 'invalid data' in error.value.detail
    else:
        result = await ai_extraction.extract_suggestions(CV, provider)
        assert result['provider'] == 'dictionary' and result['model'] is None
        assert result['source_counts']['ai'] == 0
        assert result['source_counts']['dictionary'] == len(result['candidates']) > 0
        assert result['requires_confirmation'] is True and result['stored'] is False
        assert 'local dictionary, not AI' in result['warnings'][0]


@pytest.mark.asyncio
async def test_recovered_service_result_is_runpod_not_dictionary(monkeypatch):
    from backend.catalog import SKILLS
    skill = next(s for s in SKILLS if 'SQL' in s.get('aliases', []) or s['name'] == 'SQL querying')
    item = {'skill_id': skill['id'], 'excerpt': 'SQL queries'}

    async def recovered(text, skills):
        return await adapt({'text': '{"candidates":[' + json.dumps(item) + ','}, skills)

    monkeypatch.setattr(ai_extraction, 'runpod_extract', recovered)
    result = await ai_extraction.extract_suggestions(CV, 'runpod')
    assert result['provider'] == 'runpod'
    assert result['source_counts']['ai'] == 1
    assert result['requires_confirmation'] is True and result['stored'] is False


@pytest.mark.asyncio
async def test_scanned_pdf_still_eligible_for_claude(monkeypatch):
    async def scanned(*args, **kwargs):
        return {'candidates': [], 'scanned': True, '_source_text': ''}

    monkeypatch.setattr(ai_extraction, 'claude_configured', lambda: True)
    monkeypatch.setattr(ai_extraction, 'claude_extract_pdf', scanned)
    result = await ai_extraction.extract_suggestions('', 'auto', pdf=b'%PDF', pages=[''])
    assert result['provider'] == 'claude' and result['scanned'] is True
    assert result['stored'] is False


@pytest.mark.asyncio
async def test_provider_exception_text_not_exposed(monkeypatch):
    async def invalid(*args):
        raise IntegrationError('PRIVATE-RAW-OUTPUT')

    monkeypatch.setattr(ai_extraction, 'runpod_extract', invalid)
    result = await ai_extraction.extract_suggestions(CV, 'auto')
    assert 'PRIVATE-RAW-OUTPUT' not in json.dumps(result)
    with pytest.raises(HTTPException) as error:
        await ai_extraction.extract_suggestions(CV, 'runpod')
    assert 'PRIVATE-RAW-OUTPUT' not in error.value.detail
