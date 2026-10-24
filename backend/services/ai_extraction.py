"""Choose provider and safely fall back to the local dictionary."""
import os, httpx
from fastapi import HTTPException
from ..catalog import SKILLS
from ..ai_providers import claude_extract,claude_extract_pdf,claude_configured,runpod_extract,IntegrationError
from .dictionary import suggest
from .cv_profile import extract_profile_hints

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
            candidates=supplement([],content)
            return {'provider':'dictionary','candidates':candidates,
                    'scanned':False,'profile_suggestions':extract_profile_hints(content),
                    'source_counts':{'ai':0,'dictionary':len(candidates)},
                    'warnings':issues,'requires_confirmation':True,'stored':False}
        try:
            if choice=='runpod':
                found={'candidates':await runpod_extract(content,SKILLS),'scanned':False}
            else:
                found=await (claude_extract_pdf(pdf,pages,SKILLS,include_details=True)
                             if pdf else claude_extract(content,SKILLS))
            source=found.pop('_source_text',content)
            ai_candidates=list(found['candidates'])
            found['candidates']=supplement(ai_candidates,source)
            found['source_counts']={
                'ai':len(ai_candidates),
                'dictionary':len(found['candidates'])-len(ai_candidates),
            }
            # Use grounded model hints when available. Fill missing fields from
            # explicit text sections, without storing a whole CV or assuming
            # an in-progress degree has been completed.
            extracted=extract_profile_hints(source)
            verified=found.get('profile_suggestions') or {}
            hints={**extracted,**verified}
            for key in ('projects','achievements','certifications'):
                if isinstance(extracted.get(key),list) and isinstance(verified.get(key),list):
                    combined=[];seen=set()
                    for item in verified[key]+extracted[key]:
                        value=item.get('value','').casefold()
                        if value and value not in seen:
                            combined.append(item);seen.add(value)
                    hints[key]=combined[:6]
            found['profile_suggestions']=hints
            return {'provider':choice,**found,'warnings':issues,
                    'requires_confirmation':True,'stored':False}
        except (IntegrationError,ValueError,httpx.HTTPError) as e:
            issues.append(f'{choice}: '+str(e))
            if provider!='auto':raise HTTPException(502,str(e))
    raise HTTPException(503,'No extraction method available')
