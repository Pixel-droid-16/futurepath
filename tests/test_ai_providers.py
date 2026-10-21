import json, pytest, httpx
from backend.ai_providers import (validate_candidates, IntegrationError, claude_extract, runpod_extract, runpod_url)
SK=[{'id':'sql','name':'SQL querying','aliases':['SQL']}]
CV='I used SQL for queries.'

def test_grounding_and_no_proficiency():
    result=validate_candidates({'candidates':[{'skill_id':'sql','excerpt':'SQL','proficiency':5},
      {'skill_id':'other','excerpt':'SQL'},{'skill_id':'sql','excerpt':'invented'}]},CV,SK,'claude')
    assert len(result)==1 and result[0]['proficiency'] is None

def test_rejects_fake_excerpt():
    assert validate_candidates({'candidates':[{'skill_id':'sql','excerpt':'Invented certificate'}]},CV,SK,'runpod')==[]

def test_rejects_invalid_payload():
    with pytest.raises(IntegrationError):validate_candidates('not json',CV,SK,'claude')

@pytest.mark.asyncio
async def test_claude_live_adapter_with_mock(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY','test-only')
    def handler(request):
        assert 'x-api-key' in request.headers
        return httpx.Response(200,json={'content':[{'type':'text','text':json.dumps({'candidates':[{'skill_id':'sql','excerpt':'SQL'}]})}]})
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as c:
        result=await claude_extract(CV,SK,c)
    assert result[0]['method'].startswith('claude')

@pytest.mark.asyncio
async def test_runpod_live_adapter_with_mock(monkeypatch):
    monkeypatch.setenv('RUNPOD_API_KEY','test-only')
    monkeypatch.setenv('RUNPOD_ENDPOINT_ID','abc123')
    def handler(request):
        assert request.url.path.endswith('/runsync')
        return httpx.Response(200,json={'status':'COMPLETED','output':{'text':json.dumps({'candidates':[{'skill_id':'sql','excerpt':'SQL'}]})}})
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as c:
        result=await runpod_extract(CV,SK,c)
    assert result[0]['skill_id']=='sql'

def test_runpod_rejects_untrusted_host(monkeypatch):
    monkeypatch.delenv('RUNPOD_ENDPOINT_ID',raising=False)
    monkeypatch.setenv('RUNPOD_ENDPOINT_URL','https://evil.example/run')
    with pytest.raises(IntegrationError):runpod_url()
