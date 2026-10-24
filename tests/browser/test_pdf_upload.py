"""Real multipart uploads and parsing, with only paid providers stubbed."""
import io
import re

import pytest
from playwright.sync_api import expect
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    DecodedStreamObject, DictionaryObject, NameObject, NumberObject,
)

from test_journey import continue_to_quiz, finish, manual, profiles


def synthetic_pdf(image_only=False):
    """Build tiny valid PDFs in memory; image fixture has no hidden text layer."""
    writer = PdfWriter()
    page = writer.add_blank_page(width=300, height=200)
    stream = DecodedStreamObject()
    if image_only:
        image = DecodedStreamObject()
        image.set_data(bytes([40, 80, 120]))
        image.update({
            NameObject("/Type"): NameObject("/XObject"),
            NameObject("/Subtype"): NameObject("/Image"),
            NameObject("/Width"): NumberObject(1),
            NameObject("/Height"): NumberObject(1),
            NameObject("/ColorSpace"): NameObject("/DeviceRGB"),
            NameObject("/BitsPerComponent"): NumberObject(8),
        })
        page[NameObject("/Resources")] = DictionaryObject({
            NameObject("/XObject"): DictionaryObject({
                NameObject("/Im0"): writer._add_object(image),
            }),
        })
        stream.set_data(b"q 100 0 0 100 20 20 cm /Im0 Do Q")
    else:
        font = DictionaryObject({
            NameObject("/Type"): NameObject("/Font"),
            NameObject("/Subtype"): NameObject("/Type1"),
            NameObject("/BaseFont"): NameObject("/Helvetica"),
        })
        page[NameObject("/Resources")] = DictionaryObject({
            NameObject("/Font"): DictionaryObject({
                NameObject("/F1"): writer._add_object(font),
            }),
        })
        stream.set_data(b"BT /F1 12 Tf 20 150 Td (TECHNICAL SKILLS: Python) Tj ET")
    page[NameObject("/Contents")] = writer._add_object(stream)
    output = io.BytesIO()
    writer.write(output)
    raw = output.getvalue()
    parsed = PdfReader(io.BytesIO(raw)).pages[0]
    assert parsed.extract_text() == ("" if image_only else "TECHNICAL SKILLS: Python")
    if image_only:
        assert len(parsed.images) == 1
    return raw


def upload(page, name, raw, mime="application/pdf"):
    page.goto("/start")
    page.get_by_role("button", name=re.compile("Upload a CV")).click()
    page.locator('input[type="file"]').set_input_files({
        "name": name, "mimeType": mime, "buffer": raw,
    })
    expect(page.get_by_text(name, exact=True)).to_be_visible()
    with page.expect_response("**/api/extract") as response:
        page.get_by_text("Read my CV", exact=True).click()
    return response.value


NO_TEXT = (
    "This PDF has no readable text. Upload a text-based PDF, "
    "use the manual skills form, or configure Claude for scanned PDFs."
)


@pytest.mark.parametrize("kind,status,message", [
    ("image", 422, NO_TEXT),
    ("invalid_pdf", 422, NO_TEXT),
    ("invalid_docx", 400, "Could not parse DOCX"),
    ("unsupported", 400, "Supported demo file types: PDF, DOCX, TXT"),
    ("oversized", 413, "Synthetic demo files must be <=2MB"),
])
def test_upload_failure_recovers_via_manual_form(page, kind, status, message):
    name, raw, mime = {
        "image": ("synthetic-scan.pdf", synthetic_pdf(True), "application/pdf"),
        "invalid_pdf": ("broken.pdf", b"not a PDF", "application/pdf"),
        "invalid_docx": ("broken.docx", b"not a ZIP document",
                         "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
        "unsupported": ("unsupported.bin", b"invalid document", "application/octet-stream"),
        "oversized": ("oversized.pdf", b"x" * 2_000_001, "application/pdf"),
    }[kind]
    shared_before = page.request.get("/api/profile").json()
    response = upload(page, name, raw, mime)
    assert response.status == status
    assert response.json()["detail"] == message
    expect(page.get_by_role("alert")).to_have_text(message)
    expect(page.get_by_text("Read my CV", exact=True)).to_be_visible()
    expect(page.get_by_text("Check your profile", exact=True)).to_have_count(0)
    assert profiles(page) == []
    assert page.request.get("/api/profile").json() == shared_before
    # Stay in this journey: no reload or direct navigation to hide stale state.
    page.get_by_text("Back", exact=True).click()
    saved = manual(page, "Synthetic Recovery", navigate=False)
    assert saved["skills"] == {"SK005": 4}
    assert saved["current_role"] == "Synthetic Analyst"
    assert len(profiles(page)) == 1
    expect(page.get_by_role("alert")).to_have_count(0)


@pytest.mark.parametrize("server,image_only", [("0", False), ("scanned", True)],
                         indirect=["server"])
def test_pdf_extraction_is_review_only_until_confirmed(page, image_only):
    response = upload(page, "synthetic.pdf", synthetic_pdf(image_only))
    assert response.status == 200
    result = response.json()
    assert result["provider"] == ("claude" if image_only else "runpod")
    assert result["scanned"] is image_only
    assert result["requires_confirmation"] is True
    assert result["stored"] is False
    assert "_source_text" not in result
    expect(page.get_by_text("Check your profile", exact=True)).to_be_visible()
    if image_only:
        expect(page.get_by_text(
            "Claude reviewed a PDF with little or no extractable text, and the local "
            "dictionary checked its transcription. Verify the suggested details, "
            "skills and evidence.", exact=True
        )).to_be_visible()
    else:
        expect(page.get_by_text(re.compile("Qwen on RunPod suggested 1 skills"))).to_be_visible()
    origin = "Claude AI" if image_only else "Qwen AI"
    expect(page.get_by_text(
        f"CV evidence ({origin}): “Python” (page 1)", exact=True
    )).to_be_visible()
    assert profiles(page) == []
    page.get_by_text("Continue to the interest quiz →", exact=True).click()
    expect(page.get_by_role("alert")).to_have_text(
        "Tick the box to confirm these skills describe you."
    )
    page.get_by_label("I have checked these skills").check()
    page.get_by_text("Continue to the interest quiz →", exact=True).click()
    expect(page.get_by_role("alert")).to_have_text(
        "Choose Basic, Working or Strong for every AI-suggested skill before continuing."
    )
    assert profiles(page) == []
    page.get_by_role("button", name="Working", exact=True).click()
    page.get_by_label("Profile name").fill("Synthetic PDF")
    continue_to_quiz(page)
    saved = finish(page)
    assert saved["skills"] == {"SK005": 3}
    assert saved["name"] == "Synthetic PDF"
