"""API key configuration status and grounded Claude/RunPod skill suggestions."""
from fastapi import APIRouter
from ..schemas import AIExtractRequest
from ..services.ai_extraction import integration_status,extract_suggestions
router=APIRouter(prefix='/api',tags=['ai'])
@router.get('/integrations')
def integrations():return integration_status()
@router.post('/ai/skills')
async def ai_skill_suggestions(payload:AIExtractRequest):
    return await extract_suggestions(payload.text,payload.provider)
