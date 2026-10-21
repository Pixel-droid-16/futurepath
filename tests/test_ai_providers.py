import json, pytest, httpx
from backend.ai_providers import (validate_candidates, IntegrationError, claude_extract, claude_extract_pdf, runpod_extract, runpod_url)
from tests.fake_claude import FakeClaude
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

def test_accepts_json_block_followed_by_explanation():
    # Claude's real reply shape when nothing matches: fenced JSON, then a sentence.
    empty='```json\n{\n  "candidates": []\n}\n```\n\nThe CV contains no skills from the catalogue.'
    assert validate_candidates(empty,CV,SK,'claude')==[]
    found='Here are the skills:\n```json\n{"candidates":[{"skill_id":"sql","excerpt":"SQL"}]}\n```\nOnly SQL matched.'
    assert validate_candidates(found,CV,SK,'claude')[0]['skill_id']=='sql'

@pytest.mark.asyncio
async def test_claude_live_adapter_with_mock(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY','test-only');monkeypatch.setenv('ANTHROPIC_MODEL','claude-opus-5-5')
    fake=FakeClaude({'candidates':[{'skill_id':'sql','excerpt':'SQL'}],'transcript':''})
    result=await claude_extract(CV,SK,fake)
    assert result['candidates'][0]['method'].startswith('claude') and result['scanned'] is False
    sent=fake.requests[0]
    assert sent['model']=='claude-opus-5-5' and sent['fallbacks']=='default' and sent['betas']==['server-side-fallback-2026-07-01']
    schema=sent['output_config']['format']['schema']
    assert schema['properties']['candidates']['items']['properties']['skill_id']['enum']==['sql']  # only catalogue ids are possible

@pytest.mark.asyncio
async def test_claude_reads_the_pdf_itself(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY','test-only')
    text_layer='Data officer. Wrote SQL queries for monthly reports and led a team of four volunteers. '*4
    fake=FakeClaude({'candidates':[{'skill_id':'sql','excerpt':'Wrote SQL  queries'}],'transcript':''})  # spacing differs from the text layer
    result=await claude_extract_pdf(b'%PDF-fake',text_layer,SK,fake)
    assert [c['skill_id'] for c in result['candidates']]==['sql'] and set(result)=={'candidates','scanned'}
    doc=fake.requests[0]['messages'][0]['content'][0]
    assert doc['type']=='document' and doc['source']['media_type']=='application/pdf'
    assert 'other_skills' not in fake.requests[0]['output_config']['format']['schema']['properties']

@pytest.mark.asyncio
async def test_scanned_pdf_is_checked_against_claudes_transcript(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY','test-only')
    fake=FakeClaude({'candidates':[{'skill_id':'sql','excerpt':'SQL reports'}],'transcript':'Clerk. Built SQL reports weekly.'})
    result=await claude_extract_pdf(b'%PDF-scan','',SK,fake)
    assert result['scanned'] is True and result['candidates'][0]['excerpt']=='SQL reports'
    assert 'no text layer' in fake.requests[0]['messages'][0]['content'][1]['text']

@pytest.mark.asyncio
async def test_claude_refusal_becomes_integration_error(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY','test-only')
    with pytest.raises(IntegrationError):
        await claude_extract(CV,SK,FakeClaude({},stop_reason='refusal'))

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

def test_interests_are_not_evidence():
    cv='University student interested in artificial intelligence. I wrote SQL queries for the club.'
    sk=[{'id':'sql','name':'SQL querying','aliases':['SQL']},{'id':'ai','name':'AI literacy','aliases':[]}]
    got=validate_candidates({'candidates':[{'skill_id':'ai','excerpt':'interested in artificial intelligence'},
                                           {'skill_id':'sql','excerpt':'wrote SQL queries'}]},cv,sk,'claude')
    assert [c['skill_id'] for c in got]==['sql']  # an interest is not evidence of a skill

def test_transferable_skills_are_in_the_catalogue_and_scored():
    from backend.catalog import SKILL_INDEX,ROLES
    assert {SKILL_INDEX[s]['name'] for s in ('SK079','SK080','SK081','SK082')}=={'Leadership','Teamwork','Event management','Problem solving'}
    needs=lambda sid:{r['id'] for r in ROLES if any(x['skill_id']==sid for x in r['skills'])}
    assert 'clinical-research' in needs('SK079') and 'cybersecurity-analyst' in needs('SK082') and needs('SK081')=={'instructional-designer'}
    assert all(x['importance']==1 for r in ROLES for x in r['skills'] if x['skill_id'] in ('SK079','SK080','SK081','SK082'))
