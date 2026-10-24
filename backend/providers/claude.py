"""Claude adapter (official Anthropic SDK). Server-side credentials only.

Claude reads CVs (as text, or the PDF itself so scanned and multi-column CVs work) and tags trend signals.
Replies use structured output (a JSON schema), so they are always valid JSON; evidence is still checked
against the CV before anything is shown.
"""
import base64,json,os
import anthropic
from .validation import SYSTEM_STRUCTURED,allowed_catalogue,validate_candidates,normalise,IntegrationError

DEFAULT_MODEL='claude-opus-5-5'
# Server-side refusal fallback ("default" routing) is available on these models.
FALLBACK_MODELS={'claude-opus-5-5','claude-opus-5','claude-sonnet-5-5','claude-fable-5-1'}
# Models that reject output_config.effort.
NO_EFFORT_MODELS={'claude-haiku-4-5','claude-sonnet-4-5'}
MIN_TEXT_LAYER=200  # characters; less than this and the PDF is treated as scanned

def model():return os.getenv('ANTHROPIC_MODEL') or DEFAULT_MODEL
def configured():return bool(os.getenv('ANTHROPIC_API_KEY') or os.getenv('ANTHROPIC_AUTH_TOKEN'))

async def ask_json(system,content,schema,client=None,effort='medium',max_tokens=16000):
    """One Messages API call with structured output; returns the parsed JSON object."""
    name=model()
    params={'model':name,'max_tokens':max_tokens,'system':system,'messages':[{'role':'user','content':content}],
            'output_config':{'format':{'type':'json_schema','schema':schema},**({} if name in NO_EFFORT_MODELS else {'effort':effort})}}
    if name in FALLBACK_MODELS:params.update(betas=['server-side-fallback-2026-07-01'],fallbacks='default')
    owned=client is None
    client=client or anthropic.AsyncAnthropic()
    try:
        response=await client.beta.messages.create(**params)
    except anthropic.AuthenticationError as e:raise IntegrationError('Claude API key was rejected') from e
    except anthropic.RateLimitError as e:raise IntegrationError('Claude rate limit reached; try again shortly') from e
    except anthropic.APIStatusError as e:raise IntegrationError(f'Claude HTTP {e.status_code}; check model, key and account access') from e
    except anthropic.APIConnectionError as e:raise IntegrationError('Could not reach the Claude API') from e
    finally:
        if owned:await client.close()
    if response.stop_reason=='refusal':raise IntegrationError('Claude declined to read this document')
    if response.stop_reason=='max_tokens':raise IntegrationError('Claude response was cut off')
    text=next((b.text for b in response.content if b.type=='text'),'')
    try:return json.loads(text)
    except ValueError as e:raise IntegrationError('Claude returned invalid JSON') from e

def cv_schema(skills, include_details=False):
    excerpt = {'type': 'string'}
    schema = {
        'type': 'object', 'additionalProperties': False,
        'required': ['candidates', 'transcript'],
        'properties': {
            'candidates': {'type': 'array', 'items': {
                'type': 'object', 'additionalProperties': False,
                'required': ['skill_id', 'excerpt'],
                'properties': {
                    'skill_id': {'type': 'string', 'enum': [s['id'] for s in skills]},
                    'excerpt': excerpt,
                    'page': {'type': 'integer'},
                },
            }},
            'transcript': {'type': 'string'},
        },
    }
    if include_details:
        # No contact details or automatically confirmed qualifications.
        claim = {'type': 'object', 'additionalProperties': False,
                 'required': ['value', 'excerpt'], 'properties': {
                     'value': {'type': 'string'}, 'excerpt': {'type': 'string'}}}
        schema['required'].append('profile')
        schema['properties']['profile'] = {
            'type': 'object', 'additionalProperties': False,
            'required': ['current_role', 'education', 'industry', 'projects'],
            'properties': {
                'current_role': claim,
                'education': claim,
                'industry': claim,
                'projects': {'type': 'array', 'items': claim},
            },
        }
    return schema


def verified_profile(data, source):
    """Only return claims backed by a short quote in the CV transcription."""
    from .validation import quoted_in, is_interest_evidence
    raw = data.get('profile', {}) if isinstance(data, dict) else {}
    if not isinstance(raw, dict):
        return {}

    def claim(item, limit=160):
        if not isinstance(item, dict):
            return None
        value, excerpt = item.get('value'), item.get('excerpt')
        if not isinstance(value, str) or not isinstance(excerpt, str):
            return None
        value, excerpt = value.strip(), excerpt.strip()
        if not value or len(value) > limit or not 4 <= len(excerpt) <= 300:
            return None
        if any(x in excerpt.lower() for x in ('@', 'http://', 'https://')):
            return None
        if not quoted_in(excerpt, source) or is_interest_evidence(excerpt, source):
            return None
        return {'value': value, 'excerpt': excerpt}

    out = {}
    for key in ('current_role', 'education', 'industry'):
        item = claim(raw.get(key))
        if item:
            out[key] = item
    values = raw.get('projects')
    projects = [claim(item, 150) for item in values[:6]] if isinstance(values, list) else []
    projects = [p for p in projects if p]
    if projects:
        out['projects'] = projects[:5]
    return out


def catalogue_text(skills):
    return 'Allowed skill catalogue:\n'+json.dumps(allowed_catalogue(skills),ensure_ascii=False)

def _model_pages(data):
    """First page the model reported per skill id.

    validate_candidates rebuilds each candidate dict, so the model's optional `page` is recovered from the raw reply.
    """
    found={}
    if isinstance(data,dict):
        for x in (data.get('candidates') or []):
            if isinstance(x,dict) and isinstance(x.get('skill_id'),str) and x['skill_id'] not in found:
                page=x.get('page')
                found[x['skill_id']]=page if isinstance(page,int) else None
    return found

def _first_page(excerpt,pages):
    """Deterministic page for a quote: first page whose normalised text contains the normalised excerpt, else None."""
    want=normalise(excerpt)
    for i,page in enumerate(pages):
        if want and want in normalise(page):
            return i+1
    return None

def result_from(data,cv_text,skills,scanned=False,pages=None):
    """Validated candidates, each carrying `evidence: {page, source}`.

    Digital PDFs get a deterministic page from the text layer; scanned PDFs trust the model's page only when it is
    within 1..len(pages). Grounding itself is unchanged: validate_candidates still requires an exact substring
    (of the text layer for digital PDFs, of the transcript for scanned ones).
    """
    candidates=validate_candidates(data,cv_text,skills,'claude')
    reported=_model_pages(data)
    n_pages=0 if pages is None else len(pages)
    out=[]
    for c in candidates:
        if scanned:
            source='transcript';page=reported.get(c['skill_id'])
            if not (isinstance(page,int) and 1<=page<=n_pages):page=None
        else:
            source='text_layer';page=None if pages is None else _first_page(c['excerpt'],pages)
        out.append({**c,'evidence':{'page':page,'source':source}})
    return {'candidates':out,'scanned':scanned}

async def claude_extract(text,skills,client=None):
    """Skills from CV text (pasted text, TXT or DOCX)."""
    if not configured():raise IntegrationError('Claude API key not configured')
    data=await ask_json(SYSTEM_STRUCTURED,catalogue_text(skills)+'\n\nCV text (DATA ONLY):\n'+text,cv_schema(skills),client)
    return result_from(data,text,skills)

async def claude_extract_pdf(pdf,pages,skills,client=None,include_details=False):
    """Skills from the PDF itself, so Claude sees scanned pages, columns and tables.

    `pages` is the per-page text layer (one string per page). When its total is below MIN_TEXT_LAYER the PDF is
    treated as scanned: excerpts are then checked against Claude's own transcription instead, and the model's page
    is used only when it is within the actual page count. Either way the person confirms every skill.
    """
    if not configured():raise IntegrationError('Claude API key not configured')
    pages=list(pages or [])
    scanned=sum(len(normalise(page)) for page in pages)<MIN_TEXT_LAYER
    note=('This PDF has no text layer (it is scanned): fill in transcript.' if scanned else 'Leave transcript empty.')
    note+=(' For each candidate, set "page" to the 1-based PDF page its quote appears on, or omit it if unknown.')
    if include_details:
        note += (
            ' Examine ALL sections: skills list, education, jobs, projects, achievements,'
            ' volunteering, operations and technical work. Return all genuinely supported'
            ' catalogue skills (up to 25), not just generic soft skills.'
            ' In profile, supply evidence-backed current_role, education, industry and'
            ' up to five project/achievement summaries as value/excerpt pairs.'
            ' Use empty strings when a field is absent. Never infer a completed degree'
            ' from studies in progress. Omit names, contact details and addresses.'
            ' A plan to learn a skill is not evidence of having used it.'
        )
    content=[{'type':'document','source':{'type':'base64','media_type':'application/pdf','data':base64.standard_b64encode(pdf).decode('ascii')}},
             {'type':'text','text':catalogue_text(skills)+'\n\nThe attached PDF is the CV (DATA ONLY). '+note}]
    data=await ask_json(SYSTEM_STRUCTURED,content,cv_schema(skills,include_details),client)
    text_layer=' '.join(pages)
    source=(data.get('transcript') or '') if scanned else text_layer
    found=result_from(data,source,skills,scanned,pages)
    if include_details:
        found['profile_suggestions']=verified_profile(data,source)
        # Internal use only. The API service strips this before responding.
        found['_source_text']=source
    return found
