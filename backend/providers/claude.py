"""Anthropic Messages API adapter. Server-side credentials only."""
import os,httpx
from .validation import SYSTEM,prompt_for,validate_candidates,IntegrationError
async def claude_extract(text,skills,client=None):
    key=os.getenv('ANTHROPIC_API_KEY')
    if not key:raise IntegrationError('Claude API key not configured')
    body={'model':os.getenv('ANTHROPIC_MODEL','claude-haiku-4-5'),'max_tokens':1600,
          'system':SYSTEM,'messages':[{'role':'user','content':prompt_for(text,skills)}]}
    headers={'x-api-key':key,'anthropic-version':'2023-06-01','content-type':'application/json'}
    if client is None:
        async with httpx.AsyncClient(timeout=75) as c:
            resp=await c.post('https://api.anthropic.com/v1/messages',headers=headers,json=body)
    else:
        resp=await client.post('https://api.anthropic.com/v1/messages',headers=headers,json=body)
    if resp.status_code>=400:raise IntegrationError(f'Claude HTTP {resp.status_code}; check model, key and account access')
    payload=resp.json()
    text_response='\n'.join(c.get('text','') for c in payload.get('content',[]) if c.get('type')=='text')
    return validate_candidates(text_response,text,skills,'claude')
