"""Choose provider and safely fall back to the local dictionary."""
import os, httpx
from fastapi import HTTPException
from ..catalog import SKILLS
from ..ai_providers import claude_extract,claude_extract_pdf,claude_configured,runpod_extract,IntegrationError
from .dictionary import suggest

def integration_status():
    return {'claude_enabled':claude_configured(),
            'runpod_enabled':bool(os.getenv('RUNPOD_API_KEY') and (os.getenv('RUNPOD_ENDPOINT_ID') or os.getenv('RUNPOD_ENDPOINT_URL'))),
            'provider_order':['runpod','claude','dictionary'],
            'disclaimer':'Configured does not prove a successful API connection.'}

async def extract_suggestions(content,provider,pdf=None):
    """Skill suggestions from CV text. With `pdf` (the uploaded file's bytes), Claude reads the PDF itself, so
    scanned or multi-column CVs still work; RunPod and the dictionary only ever see the extracted text."""
    if provider not in ('auto','claude','runpod','dictionary'):
        raise HTTPException(400,'Unknown AI provider')
    choices=([provider] if provider!='auto' else ['runpod','claude','dictionary'])
    issues=[]
    for choice in choices:
        if choice=='runpod' and not integration_status()['runpod_enabled']:
            if provider=='auto':continue
            raise HTTPException(503,'RunPod is not configured')
        if choice=='claude' and not integration_status()['claude_enabled']:
            if provider=='auto':continue
            raise HTTPException(503,'Claude is not configured')
        if choice=='dictionary':
            return {'provider':'dictionary','candidates':suggest(content),'scanned':False,
                    'warnings':issues,'requires_confirmation':True,'stored':False}
        try:
            if choice=='runpod':
                found={'candidates':await runpod_extract(content,SKILLS),'scanned':False}
            else:
                found=await (claude_extract_pdf(pdf,content,SKILLS) if pdf else claude_extract(content,SKILLS))
            return {'provider':choice,**found,'warnings':issues,'requires_confirmation':True,'stored':False}
        except (IntegrationError,ValueError,httpx.HTTPError) as e:
            issues.append(f'{choice}: '+str(e))
            if provider!='auto':raise HTTPException(502,str(e))
    raise HTTPException(503,'No extraction method available')
