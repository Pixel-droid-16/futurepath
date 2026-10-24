"""CV upload for synthetic PDF, DOCX and TXT files.

Text-based CVs can be sent to Qwen on RunPod. Image-only PDFs must go
to the PDF-capable Claude provider (when configured) or be rejected clearly.
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from ..ai_providers import claude_configured
from ..services.documents import read_upload, parse_cv_pages
from ..services.dictionary import suggest
from ..services.ai_extraction import extract_suggestions

router = APIRouter(prefix='/api', tags=['cv-upload'])


@router.post('/extract')
async def extract(file: UploadFile = File(...), provider: str = Form('dictionary')):
    if provider not in ('auto', 'runpod', 'claude', 'dictionary'):
        raise HTTPException(400, 'Unknown AI provider')

    name, raw = await read_upload(file)
    is_pdf = name.endswith('.pdf')
    pages = parse_cv_pages(name, raw, strict=not is_pdf)
    content = ' '.join(pages)

    if not is_pdf and not content.strip():
        raise HTTPException(
            422,
            'No readable text found. Upload a CV with selectable text or use the manual skills form.',
        )

    # Qwen and the dictionary only receive extracted text, not page images.
    # Avoid presenting an image-only PDF as a successful zero-skill extraction.
    if is_pdf and not content.strip():
        if provider == 'claude' or (provider == 'auto' and claude_configured()):
            provider = 'claude'
        else:
            raise HTTPException(
                422,
                'This PDF has no readable text. Upload a text-based PDF, '
                'use the manual skills form, or configure Claude for scanned PDFs.',
            )

    if provider == 'dictionary':
        return {
            'provider': 'dictionary',
            'candidates': suggest(content, 45, 55),
            'scanned': False,
            'requires_confirmation': True,
            'stored': False,
            'warning': 'Rule-based fallback, not GPU AI. Synthetic CVs only. '
                       'Review and confirm each skill; no extracted skill is scored automatically.',
        }

    result = await extract_suggestions(
        content, provider,
        pdf=raw if is_pdf else None,
        pages=pages if is_pdf else None,
    )
    return {
        **result,
        'warning': 'AI suggestions are unconfirmed. Review and confirm each skill before saving.',
    }
