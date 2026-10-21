"""Learning resources. Edit data/learning_resources.json to change them."""
from fastapi import APIRouter
from ..catalog import RESOURCES
router=APIRouter(prefix='/api',tags=['learning'])
@router.get('/resources')
def resources():return RESOURCES
