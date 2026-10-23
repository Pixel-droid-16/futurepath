"""CV upload: PDF, DOCX and TXT. Claude reads PDFs directly; the dictionary is the offline fallback."""
from fastapi import APIRouter,UploadFile,File,Form
from ..services.documents import read_upload,parse_cv,parse_cv_pages
from ..services.dictionary import suggest
from ..services.ai_extraction import extract_suggestions
router=APIRouter(prefix='/api',tags=['cv-upload'])
@router.post('/extract')
async def extract(file:UploadFile=File(...),provider:str=Form('dictionary')):
    name,raw=await read_upload(file)
    if provider=='dictionary':
        return {'provider':'dictionary','candidates':suggest(parse_cv(name,raw),45,55),'scanned':False,
                'warning':'Rule-based fallback, not GPU AI. Synthetic CVs only. Review and confirm each skill; no extracted skill is scored automatically.'}
    # Same provider chain as /api/ai/skills (auto: RunPod -> Claude -> dictionary); Claude gets the PDF itself and
    # its per-page text layer (for deterministic page-level evidence). The CV body is not stored.
    is_pdf=name.endswith('.pdf')
    pages=parse_cv_pages(name,raw,strict=not is_pdf)
    result=await extract_suggestions(' '.join(pages),provider,pdf=raw if is_pdf else None,pages=pages if is_pdf else None)
    return {**result,'warning':'AI suggestions are unconfirmed. Review and confirm each skill before it is saved.'}
