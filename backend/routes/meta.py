"""About the application and catalogue counts."""
from fastapi import APIRouter
from ..catalog import SKILLS,ROLES,RESOURCES
router=APIRouter(prefix='/api',tags=['meta'])
@router.get('/meta')
def meta():
    return {'name':'FuturePath Prism','disclaimer':'All trend values and sample scores are synthetic, not predictions or live market evidence','skills_count':len(SKILLS),'careers_count':len(ROLES),'resources_count':len(RESOURCES),'ai_status':'manual/rule fallback; RunPod not connected'}
