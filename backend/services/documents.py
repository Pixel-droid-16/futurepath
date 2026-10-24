"""Parse text-only documents used in the synthetic CV demo."""
import io
from fastapi import HTTPException,UploadFile
MAX_BYTES=2_000_000

async def read_upload(file:UploadFile):
    """The uploaded file's lower-cased name and bytes, within the demo size limit."""
    raw=await file.read(MAX_BYTES+1)
    if len(raw)>MAX_BYTES:raise HTTPException(413,'Synthetic demo files must be <=2MB')
    return (file.filename or '').lower(),raw

def parse_cv_pages(name, raw, strict=True):
    """Per-page text from a PDF, DOCX or TXT CV.

    Returns a list[str] where each element is one page for PDFs
    (up to 8 pages) or a single-element list for DOCX/TXT.
    Image-only but otherwise valid PDFs return empty text for optional
    image-capable Claude support; corrupt PDFs raise a clear error.
    """
    if name.endswith('.pdf'):
        from pypdf import PdfReader
        try:
            return [
                page.extract_text() or ''
                for page in PdfReader(io.BytesIO(raw)).pages[:8]
            ]
        except Exception:
            # Bad PDF bytes must not be treated as a scanned document and
            # needlessly sent to a potentially paid external AI service.
            raise HTTPException(400, 'Could not read PDF. Export a valid PDF file.')
    elif name.endswith('.docx'):
        from docx import Document
        try:
            # CV authors frequently use tables for tool lists, work history
            # and certifications; preserve their position among paragraphs.
            lines = []
            for block in Document(io.BytesIO(raw)).iter_inner_content():
                if hasattr(block, 'rows'):
                    for row in block.rows:
                        fields = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                        if fields:
                            lines.append(' | '.join(fields))
                elif block.text.strip():
                    lines.append(block.text.strip())
            return ['\\n'.join(lines)]
        except Exception:
            raise HTTPException(400, 'Could not parse DOCX')
    elif name.endswith('.txt'):
        return [raw.decode('utf8', errors='replace')]
    raise HTTPException(400, 'Supported demo file types: PDF, DOCX, TXT')


def parse_cv(name, raw, strict=True):
    """Text from a PDF, DOCX or TXT CV — joined into a single string.

    Only valid image-only PDFs may produce an empty text layer; malformed
    documents raise a descriptive error.
    """
    return ' '.join(parse_cv_pages(name, raw, strict=strict))

async def read_cv(file:UploadFile):
    name,raw=await read_upload(file)
    return parse_cv(name,raw)
