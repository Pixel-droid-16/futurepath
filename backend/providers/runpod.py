"""RunPod Serverless queue endpoint adapter. Server-side credentials only."""
import os,re,httpx
from urllib.parse import urlparse
from .validation import SYSTEM,prompt_for,validate_candidates,IntegrationError
def runpod_url():
    endpoint_id=os.getenv('RUNPOD_ENDPOINT_ID','').strip()
    custom=os.getenv('RUNPOD_ENDPOINT_URL','').strip()
    if endpoint_id:
        if not re.fullmatch('[A-Za-z0-9_-]{3,100}',endpoint_id):raise IntegrationError('Invalid RunPod endpoint ID')
        return f'https://api.runpod.ai/v2/{endpoint_id}/runsync?wait=90000'
    if custom:
        p=urlparse(custom)
        if p.scheme!='https' or not p.hostname or p.username or p.password:
            raise IntegrationError('RunPod URL must be a valid HTTPS endpoint')
        if p.hostname!='api.runpod.ai':raise IntegrationError('Only api.runpod.ai endpoint URLs supported')
        return custom if custom.rstrip('/').endswith('/runsync') else custom.rstrip('/')+'/runsync'
    raise IntegrationError('RunPod endpoint ID not configured')
async def runpod_extract(text,skills,client=None):
    if not os.getenv('RUNPOD_API_KEY'):raise IntegrationError('RunPod key not configured')
    url=runpod_url()
    headers={'Authorization':'Bearer '+os.environ['RUNPOD_API_KEY'],'Content-Type':'application/json'}
    body={'input':{'task':'extract_skills','system':SYSTEM,'prompt':prompt_for(text,skills)}}
    if client is None:
        async with httpx.AsyncClient(timeout=110) as c:resp=await c.post(url,headers=headers,json=body)
    else:
        resp=await client.post(url,headers=headers,json=body)
    if resp.status_code>=400:raise IntegrationError(f'RunPod HTTP {resp.status_code}; check endpoint and worker logs')
    payload=resp.json()
    if payload.get('status')!='COMPLETED':
        raise IntegrationError('RunPod job did not complete: '+str(payload.get('status','unknown')))
    return validate_candidates(payload.get('output'),text,skills,'runpod')
