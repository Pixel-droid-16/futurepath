"""Career catalogue. Edit data/roles.json to change roles."""
from fastapi import APIRouter
from ..catalog import ROLES
router=APIRouter(prefix='/api',tags=['careers'])
@router.get('/roles')
def roles():return ROLES
