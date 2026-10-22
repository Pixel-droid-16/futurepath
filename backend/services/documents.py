"""Parse text-only documents used in the synthetic CV demo."""
import io
from fastapi import HTTPException,UploadFile
MAX_BYTES=2_000_000

async def read_upload(file:UploadFile):
    """The uploaded file's lower-cased name and bytes, within the demo size limit."""
    raw=await file.read(MAX_BYTES+1)
    if len(raw)>MAX_BYTES:raise HTTPException(413,'Synthetic demo files must be <=2MB')
    return (file.filename or '').lower(),raw

def parse_cv(name,raw,strict=True):
    """Text from a PDF, DOCX or TXT CV. With strict=False an unreadable PDF gives '' (Claude can still read the file)."""
    if name.endswith('.pdf'):
        from pypdf import PdfReader
        try:return ' '.join(page.extract_text() or '' for page in PdfReader(io.BytesIO(raw)).pages[:8])
        except Exception:
            if strict:raise HTTPException(400,'Could not parse text PDF')
            return ''
    elif name.endswith('.docx'):
        from docx import Document
        try:return ' '.join(p.text for p in Document(io.BytesIO(raw)).paragraphs)
        except Exception:raise HTTPException(400,'Could not parse DOCX')
    elif name.endswith('.txt'):
        return raw.decode('utf8',errors='replace')
    raise HTTPException(400,'Supported demo file types: PDF, DOCX, TXT')

async def read_cv(file:UploadFile):
    name,raw=await read_upload(file)
    return parse_cv(name,raw)
