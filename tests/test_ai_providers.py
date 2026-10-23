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
    assert result['candidates'][0]['evidence']=={'page':None,'source':'text_layer'}
    assert schema['properties']['candidates']['items']['properties']['page']=={'type':'integer'}

@pytest.mark.asyncio
async def test_claude_reads_the_pdf_itself(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY','test-only')
    # Pages 2 and 3 both repeat the achievement line; the page must resolve to the first hit.
    para='Data officer. Wrote SQL queries for monthly reports and led a team of four volunteers. '
    pages=['Cover letter: applying for a data role. '*8, para*5, para*2+'Coursework and references. '*6]
    fake=FakeClaude({'candidates':[{'skill_id':'sql','excerpt':'Wrote SQL  queries'}],'transcript':''})  # spacing differs from the text layer
    result=await claude_extract_pdf(b'%PDF-fake',pages,SK,fake)
    assert [c['skill_id'] for c in result['candidates']]==['sql'] and set(result)=={'candidates','scanned'}
    assert result['candidates'][0]['evidence']=={'page':2,'source':'text_layer'}
    doc=fake.requests[0]['messages'][0]['content'][0]
    assert doc['type']=='document' and doc['source']['media_type']=='application/pdf'
    schema=fake.requests[0]['output_config']['format']['schema']['properties']
    assert 'other_skills' not in schema and schema['candidates']['items']['properties']['page']=={'type':'integer'}
    assert '1-based' in fake.requests[0]['messages'][0]['content'][1]['text']

@pytest.mark.asyncio
async def test_scanned_pdf_is_checked_against_claudes_transcript(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY','test-only')
    fake=FakeClaude({'candidates':[{'skill_id':'sql','excerpt':'SQL reports'}],'transcript':'Clerk. Built SQL reports weekly.'})
    result=await claude_extract_pdf(b'%PDF-scan',[''],SK,fake)
    assert result['scanned'] is True and result['candidates'][0]['excerpt']=='SQL reports'
    assert result['candidates'][0]['evidence']=={'page':None,'source':'transcript'}
    prompt=fake.requests[0]['messages'][0]['content'][1]['text']
    assert 'no text layer' in prompt and '1-based' in prompt

@pytest.mark.asyncio
async def test_scanned_page_is_trusted_only_within_page_count(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY','test-only')
    reply=lambda page:{'candidates':[{'skill_id':'sql','excerpt':'SQL reports','page':page}],'transcript':'Clerk. Built SQL reports weekly.'}
    in_range=await claude_extract_pdf(b'%PDF-scan',['','',''],SK,FakeClaude(reply(2)))
    assert in_range['candidates'][0]['evidence']=={'page':2,'source':'transcript'}
    out_of_range=await claude_extract_pdf(b'%PDF-scan',['','',''],SK,FakeClaude(reply(99)))
    assert out_of_range['candidates'][0]['evidence']=={'page':None,'source':'transcript'}

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

def test_cv_schema_uses_only_keywords_claude_structured_output_accepts():
    # The fake client accepts any schema; the real API rejects e.g. 'minimum' on integers (HTTP 400), which made
    # every Claude CV reading fail silently into keyword matching.
    from backend.providers.claude import cv_schema
    unsupported={'minimum','maximum','exclusiveMinimum','exclusiveMaximum','multipleOf','minLength','maxLength','pattern','format'}
    def walk(node):
        if isinstance(node,dict):
            assert not unsupported & set(node), node
            for v in node.values():walk(v)
        elif isinstance(node,list):
            for v in node:walk(v)
    walk(cv_schema([{'id':'sql','name':'SQL'}]))
