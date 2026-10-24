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

async def extract_suggestions(content,provider,pdf=None,pages=None):
    """Return review-only skill suggestions; never return the internal scanned transcript."""
    if provider not in ('auto','claude','runpod','dictionary'):
        raise HTTPException(400,'Unknown AI provider')
    choices=([provider] if provider!='auto' else ['runpod','claude','dictionary'])
    issues=[]
    from ..providers.validation import quoted_in, is_interest_evidence

    def supplement(candidates,text):
        seen={item['skill_id'] for item in candidates}
        for item in suggest(text):
            sid, excerpt=item['skill_id'],item['excerpt']
            if sid in seen or not 3 <= len(excerpt) <= 300:
                continue
            if not quoted_in(excerpt,text) or is_interest_evidence(excerpt,text):
                continue
            candidates.append(item)
            seen.add(sid)
        return candidates

    for choice in choices:
        if choice=='runpod' and not integration_status()['runpod_enabled']:
            if provider=='auto':continue
            raise HTTPException(503,'RunPod is not configured')
        if choice=='claude' and not integration_status()['claude_enabled']:
            if provider=='auto':continue
            raise HTTPException(503,'Claude is not configured')
        if choice=='dictionary':
            return {'provider':'dictionary','candidates':supplement([],content),
                    'scanned':False,'profile_suggestions':{},'warnings':issues,
                    'requires_confirmation':True,'stored':False}
        try:
            if choice=='runpod':
                found={'candidates':await runpod_extract(content,SKILLS),'scanned':False}
            else:
                found=await (claude_extract_pdf(pdf,pages,SKILLS,include_details=True)
                             if pdf else claude_extract(content,SKILLS))
            source=found.pop('_source_text',content)
            found['candidates']=supplement(list(found['candidates']),source)
            found.setdefault('profile_suggestions',{})
            return {'provider':choice,**found,'warnings':issues,
                    'requires_confirmation':True,'stored':False}
        except (IntegrationError,ValueError,httpx.HTTPError) as e:
            issues.append(f'{choice}: '+str(e))
            if provider!='auto':raise HTTPException(502,str(e))
    raise HTTPException(503,'No extraction method available')
