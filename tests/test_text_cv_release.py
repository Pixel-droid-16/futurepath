"""Synthetic full-stack CV regression tests; no personal CVs or contact details."""
import asyncio
from unittest.mock import AsyncMock, patch

from backend.catalog import SKILLS, ROLES
from backend.services.cv_profile import extract_profile_hints
from backend.services.dictionary import suggest
from backend.services.ai_extraction import extract_suggestions

SYNTHETIC_CV = """SUMMARY
Computer Science student and full-stack builder. Builds web apps with Laravel,
React, Vue and PostgreSQL, integrates AI APIs, and prototypes with Arduino
and ESP32.
EDUCATION
Example University
Bachelor of Computer Science (Artificial Intelligence)
2026 to Present
Example Matriculation College
Matriculation Certificate
2024 to 2026
TECHNICAL SKILLS
Languages: Python, Java, C++, JavaScript, PHP, HTML, CSS, SQL
Frameworks: Laravel, React, Vue
Databases: PostgreSQL
Other: web development, cybersecurity fundamentals
PROJECTS
Gym Check-in App | Laravel, PostgreSQL
Replaced manual check-ins with QR scanning.
Smart Door Lock | ESP32, RFID
Lets users unlock doors using a card.
AWARDS & ACHIEVEMENTS
Gold, National Technology Competition 2025
CERTIFICATIONS
Foundations of Cybersecurity, Example Academy: Security basics and frameworks
LEADERSHIP
President, student computer club
"""


def test_expanded_catalogue_recognises_explicit_technical_skills():
    candidates = suggest(SYNTHETIC_CV)
    ids = {item['skill_id'] for item in candidates}
    expected = {
        'SK001', 'SK005', 'SK011', 'SK109', 'SK110', 'SK111',
        'SK112', 'SK113', 'SK114', 'SK115', 'SK116', 'SK117',
        'SK118', 'SK119',
    }
    assert expected <= ids
    for item in candidates:
        assert item['excerpt'] in SYNTHETIC_CV
        assert item['proficiency'] is None


def test_fullstack_role_uses_development_skills_not_generic_data_cleaning():
    fullstack = next(r for r in ROLES if r['id'] == 'fullstack-software-engineer')
    needs = {item['skill_id'] for item in fullstack['skills']}
    assert {'SK109', 'SK110', 'SK111', 'SK112', 'SK115', 'SK114'} <= needs
    assert 'SK003' not in needs
    assert 4 <= len(needs) <= 10


def test_text_cv_profile_hints_and_ongoing_education():
    details = extract_profile_hints(SYNTHETIC_CV)
    assert details['current_role']['value'] == 'full-stack builder'
    assert details['education']['value'].endswith('(in progress)')
    assert details['completed_qualification']['value'] == 'Malaysian Matriculation Certificate'
    assert {'Gym Check-in App', 'Smart Door Lock'} <= {
        item['value'] for item in details['projects']
    }
    assert 'Gold' in details['achievements'][0]['value']
    assert 'Cybersecurity' in details['certifications'][0]['value']


def test_qwen_zero_suggestions_report_dictionary_coverage_correctly():
    async def run():
        with patch('backend.services.ai_extraction.runpod_extract',
                   new_callable=AsyncMock, return_value=[]), \\
             patch('backend.services.ai_extraction.integration_status',
                   return_value={'runpod_enabled': True, 'claude_enabled': True}):
            return await extract_suggestions(SYNTHETIC_CV, 'runpod')

    result = asyncio.run(run())
    assert result['provider'] == 'runpod'
    assert result['source_counts']['ai'] == 0
    assert result['source_counts']['dictionary'] == len(result['candidates'])
    assert len(result['candidates']) >= 14
    assert result['requires_confirmation'] is True and result['stored'] is False
    assert 'projects' in result['profile_suggestions']


def test_qwen_and_dictionary_counts_preserve_deduplication():
    generated = [{
        'skill_id': 'SK115', 'name': 'JavaScript programming',
        'excerpt': 'JavaScript', 'method': 'runpod AI suggestion (unconfirmed)',
        'proficiency': None,
    }]
    async def run():
        with patch('backend.services.ai_extraction.runpod_extract',
                   new_callable=AsyncMock, return_value=generated), \\
             patch('backend.services.ai_extraction.integration_status',
                   return_value={'runpod_enabled': True, 'claude_enabled': True}):
            return await extract_suggestions(SYNTHETIC_CV, 'runpod')

    result = asyncio.run(run())
    ids = [x['skill_id'] for x in result['candidates']]
    assert len(ids) == len(set(ids))
    assert result['source_counts']['ai'] == 1
    assert result['source_counts']['dictionary'] == len(ids) - 1
    assert next(x for x in result['candidates'] if x['skill_id'] == 'SK115')['method'].startswith('runpod')


def test_text_cv_profile_hints_do_not_include_contact_data():
    cv = SYNTHETIC_CV + '\nCONTACT\nexample@example.org\nhttps://example.org/'
    suggestions = extract_profile_hints(cv)
    serialized = str(suggestions)
    assert 'example@example.org' not in serialized
    assert 'https://example.org' not in serialized
