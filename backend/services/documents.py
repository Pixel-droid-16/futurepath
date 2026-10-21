"""Parse text-only documents used in the synthetic CV demo."""
import io
from fastapi import HTTPException,UploadFile
async def read_cv(file:UploadFile):
    name=(file.filename or '').lower()
    raw=await file.read(2_000_001)
    if len(raw)>2_000_000:raise HTTPException(413,'Synthetic demo files must be <=2MB')
    if name.endswith('.pdf'):
        from pypdf import PdfReader
        try:return ' '.join(page.extract_text() or '' for page in PdfReader(io.BytesIO(raw)).pages[:8])
        except Exception:raise HTTPException(400,'Could not parse text PDF')
    elif name.endswith('.docx'):
        from docx import Document
        try:return ' '.join(p.text for p in Document(io.BytesIO(raw)).paragraphs)
        except Exception:raise HTTPException(400,'Could not parse DOCX')
    elif name.endswith('.txt'):
        return raw.decode('utf8',errors='replace')
    raise HTTPException(400,'Supported demo file types: PDF, DOCX, TXT')
