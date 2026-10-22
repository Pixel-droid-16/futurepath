"""About the application and catalogue counts."""
from fastapi import APIRouter
from ..catalog import SKILLS,ROLES,RESOURCES,COURSES
router=APIRouter(prefix='/api',tags=['meta'])
@router.get('/meta')
def meta():
    return {'name':'FuturePath Prism','disclaimer':'Trend scores come from dated, sourced signals (curated reports plus refreshed news, research and dataset feeds). Scores are estimates, not predictions.','skills_count':len(SKILLS),'careers_count':len(ROLES),'resources_count':len(RESOURCES),'courses_count':len(COURSES),'ai_status':'manual/rule fallback; RunPod not connected'}
