"""Regression tests for image-only PDFs and non-image CV routing."""
import io
from unittest.mock import AsyncMock, patch

from docx import Document
from fastapi.testclient import TestClient
from pypdf import PdfWriter

from backend.app import app


def blank_pdf():
    data = io.BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    writer.write(data)
    return data.getvalue()


def test_image_only_pdf_requires_pdf_capable_provider():
    client = TestClient(app)
    with patch('backend.routes.cv_upload.claude_configured', return_value=False), \
         patch('backend.routes.cv_upload.extract_suggestions', new_callable=AsyncMock) as extract:
        response = client.post(
            '/api/extract',
            files={'file': ('synthetic_scan.pdf', blank_pdf(), 'application/pdf')},
            data={'provider': 'auto'},
        )

    assert response.status_code == 422
    assert 'no readable text' in response.json()['detail'].lower()
    extract.assert_not_awaited()


def test_image_only_pdf_uses_claude_in_auto_mode():
    client = TestClient(app)
    with patch('backend.routes.cv_upload.claude_configured', return_value=True), \
         patch(
             'backend.routes.cv_upload.extract_suggestions',
             new_callable=AsyncMock,
             return_value={'provider': 'claude', 'candidates': [], 'scanned': True,
                           'requires_confirmation': True, 'stored': False},
         ) as extract:
        response = client.post(
            '/api/extract',
            files={'file': ('synthetic_scan.pdf', blank_pdf(), 'application/pdf')},
            data={'provider': 'auto'},
        )

    assert response.status_code == 200
    assert response.json()['provider'] == 'claude'
    assert response.json()['scanned'] is True
    assert extract.await_args.args[1] == 'claude'


def test_explicit_runpod_rejects_image_only_pdf():
    client = TestClient(app)
    response = client.post(
        '/api/extract',
        files={'file': ('synthetic_scan.pdf', blank_pdf(), 'application/pdf')},
        data={'provider': 'runpod'},
    )
    assert response.status_code == 422


def test_text_docx_keeps_auto_provider_selection():
    doc = Document()
    doc.add_paragraph('I wrote SQL queries and Python scripts for reports.')
    data = io.BytesIO()
    doc.save(data)
    client = TestClient(app)

    with patch(
        'backend.routes.cv_upload.extract_suggestions',
        new_callable=AsyncMock,
        return_value={'provider': 'dictionary', 'candidates': [], 'scanned': False,
                      'requires_confirmation': True, 'stored': False},
    ) as extract:
        response = client.post(
            '/api/extract',
            files={'file': ('synthetic_cv.docx', data.getvalue(),
                            'application/vnd.openxmlformats-officedocument.wordprocessingml.document')},
            data={'provider': 'auto'},
        )

    assert response.status_code == 200
    assert 'Python scripts' in extract.await_args.args[0]
    assert extract.await_args.args[1] == 'auto'
