"""Synthetic PDF, DOCX and TXT rule-based upload extraction."""
from fastapi import APIRouter,UploadFile,File
from ..services.documents import read_cv
from ..services.dictionary import suggest
router=APIRouter(prefix='/api',tags=['cv-upload'])
@router.post('/extract')
async def extract(file:UploadFile=File(...)):
    content=await read_cv(file)
    return {'candidates':suggest(content,45,55),
            'warning':'Rule-based fallback, not GPU AI. Synthetic CVs only. Review and confirm each skill; no extracted skill is scored automatically.'}
