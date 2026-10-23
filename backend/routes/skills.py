"""Canonical skills catalogue. Edit data/skills.json to change skills."""
from fastapi import APIRouter
from ..catalog import SKILLS
router=APIRouter(prefix='/api',tags=['skills'])
@router.get('/skills')
def skills():return SKILLS
