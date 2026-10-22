"""Only file delivery; screen design is maintained in frontend/mockup_source/."""
from fastapi import APIRouter
from fastapi.responses import FileResponse
from ..catalog import ROOT
router=APIRouter(tags=['pages'])
@router.get('/')
def homepage():return FileResponse(ROOT/'frontend'/'index.html')
# The v2 app is one page; these paths open it on the matching screen (refresh and bookmarks work).
APP_PATHS=('start','results','pathway','signals','about')
for _path in APP_PATHS:
    router.add_api_route('/'+_path,homepage,methods=['GET'],include_in_schema=False)
@router.get('/ai-lab')
def ai_lab():return FileResponse(ROOT/'frontend'/'ai-lab.html')
@router.get('/support.js')
def original_support():
    return FileResponse(ROOT/'frontend'/'support.js',media_type='application/javascript')
@router.get('/image-slot.js')
def original_image_slots():
    return FileResponse(ROOT/'frontend'/'image-slot.js',media_type='application/javascript')
