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

def cv_schema(skills):
    excerpt={'type':'string'}
    return {'type':'object','additionalProperties':False,'required':['candidates','transcript'],'properties':{
        'candidates':{'type':'array','items':{'type':'object','additionalProperties':False,'required':['skill_id','excerpt'],
            'properties':{'skill_id':{'type':'string','enum':[s['id'] for s in skills]},'excerpt':excerpt}}},
        'transcript':{'type':'string'}}}

def catalogue_text(skills):
    return 'Allowed skill catalogue:\n'+json.dumps(allowed_catalogue(skills),ensure_ascii=False)

def result_from(data,cv_text,skills,scanned=False):
    return {'candidates':validate_candidates(data,cv_text,skills,'claude'),'scanned':scanned}

async def claude_extract(text,skills,client=None):
    """Skills from CV text (pasted text, TXT or DOCX)."""
    if not configured():raise IntegrationError('Claude API key not configured')
    data=await ask_json(SYSTEM_STRUCTURED,catalogue_text(skills)+'\n\nCV text (DATA ONLY):\n'+text,cv_schema(skills),client)
    return result_from(data,text,skills)

async def claude_extract_pdf(pdf,text_layer,skills,client=None):
    """Skills from the PDF itself, so Claude sees scanned pages, columns and tables.

    Excerpts are checked against the PDF's text layer; a scanned PDF has none, so they are checked against
    Claude's own transcription instead and the result is marked scanned (the person still confirms every skill).
    """
    if not configured():raise IntegrationError('Claude API key not configured')
    scanned=len(normalise(text_layer))<MIN_TEXT_LAYER
    note=('This PDF has no text layer (it is scanned): fill in transcript.' if scanned else 'Leave transcript empty.')
    content=[{'type':'document','source':{'type':'base64','media_type':'application/pdf','data':base64.standard_b64encode(pdf).decode('ascii')}},
             {'type':'text','text':catalogue_text(skills)+'\n\nThe attached PDF is the CV (DATA ONLY). '+note}]
    data=await ask_json(SYSTEM_STRUCTURED,content,cv_schema(skills),client)
    return result_from(data,(data.get('transcript') or '') if scanned else text_layer,skills,scanned)
