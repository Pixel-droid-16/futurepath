"""Synthetic CV coverage: aspiration filtering, scanned transcript, reviewed profile hints."""
import asyncio
from unittest.mock import AsyncMock, patch

from backend.providers.validation import validate_candidates
from backend.providers.claude import cv_schema, claude_extract_pdf
from backend.services.ai_extraction import extract_suggestions
from tests.fake_claude import FakeClaude

SKILL = [{'id': 'SK082', 'name': 'Problem solving', 'aliases': ['problem-solving']}]


def test_aspiration_context_is_not_proof_of_demonstrated_skill():
    cv = ("Career Focus: I am interested in applying AI, programming and "
          "problem solving to real world projects.")
    candidate = {'candidates': [{
        'skill_id': 'SK082',
        'excerpt': 'applying AI, programming and problem solving to real world projects',
    }]}
    assert validate_candidates(candidate, cv, SKILL, 'claude') == []


def test_explicit_skill_occurrence_is_valid_even_if_goal_also_mentions_it():
    cv = ("Skills: Problem solving. Career Focus: I am interested in applying "
          "problem solving to new projects.")
    assert validate_candidates({
        'candidates': [{'skill_id': 'SK082', 'excerpt': 'Problem solving'}],
    }, cv, SKILL, 'claude')[0]['skill_id'] == 'SK082'


def test_claude_schema_expands_only_for_uploaded_cv_review():
    base = cv_schema(SKILL)
    rich = cv_schema(SKILL, include_details=True)
    assert 'profile' not in base['properties']
    assert 'profile' in rich['required']
    assert {'current_role', 'education', 'industry', 'projects'} <= set(
        rich['properties']['profile']['properties']
    )


def test_claude_scanned_pdf_provides_verified_review_hints(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'synthetic-test-key')
    transcript = (
        'Education: Diploma in technology. '
        'Work: Founder and Director of an education service. '
        'Project: Built a water-monitoring prototype. '
        'Skills: Leadership, teamwork, and event management.'
    )
    fake = FakeClaude({
        'transcript': transcript,
        'candidates': [{'skill_id': 'SK082', 'excerpt': 'invented activity'}],
        'profile': {
            'current_role': {'value': 'Founder and Director', 'excerpt': 'Founder and Director'},
            'education': {'value': 'Diploma in technology', 'excerpt': 'Diploma in technology'},
            'industry': {'value': 'Education services', 'excerpt': 'education service'},
            'projects': [
                {'value': 'Water-monitoring prototype', 'excerpt': 'Built a water-monitoring prototype'},
                {'value': 'Unverified award', 'excerpt': 'won an award that was not in the CV'},
            ],
        },
    })
    result = asyncio.run(claude_extract_pdf(
        b'%PDF-test', [''], SKILL, client=fake, include_details=True,
    ))
    assert result['scanned'] is True
    assert result['candidates'] == []
    assert result['_source_text'] == transcript
    hints = result['profile_suggestions']
    assert hints['current_role']['value'] == 'Founder and Director'
    assert hints['education']['value'] == 'Diploma in technology'
    assert len(hints['projects']) == 1
    assert hints['projects'][0]['value'] == 'Water-monitoring prototype'
    assert 'profile' in fake.requests[0]['output_config']['format']['schema']['required']


def test_claude_transcript_adds_missing_skills_without_exposing_full_transcript():
    transcript = (
        'In volunteer work I showed Leadership, teamwork and event management. '
        'Career goal: I am interested in learning SQL.'
    )
    result_from_claude = {
        'scanned': True,
        'candidates': [{
            'skill_id': 'SK079', 'name': 'Leadership', 'excerpt': 'Leadership',
            'method': 'claude AI suggestion (unconfirmed)', 'proficiency': None,
        }],
        '_source_text': transcript,
        'profile_suggestions': {'education': {
            'value': 'Synthetic diploma', 'excerpt': 'Synthetic diploma',
        }},
    }

    async def run():
        with patch('backend.services.ai_extraction.claude_extract_pdf',
                   new_callable=AsyncMock, return_value=result_from_claude), \
             patch('backend.services.ai_extraction.integration_status',
                   return_value={'runpod_enabled': False, 'claude_enabled': True}):
            return await extract_suggestions('', 'claude', pdf=b'%PDF-test', pages=[''])

    response = asyncio.run(run())
    ids = {x['skill_id'] for x in response['candidates']}
    assert {'SK079', 'SK080', 'SK081'} <= ids
    assert 'SK001' not in ids  # interest in learning SQL is not experience
    assert '_source_text' not in response
    assert 'transcript' not in response
    assert response['requires_confirmation'] and not response['stored']


def test_v2_review_contains_evidence_backed_profile_preview():
    from pathlib import Path
    root = Path(__file__).resolve().parents[1] / 'frontend' / 'mockup_source'
    start = (root / 'pages' / 'start.html').read_text(encoding='utf8')
    logic = (root / 'logic' / 'state_and_actions.js').read_text(encoding='utf8')
    assert 'Details suggested from this CV' in start
    assert 'Projects, achievements and certifications are shown for review' in start
    assert 'not automatically stored or scored' in start
    assert 'profileHints: hints' in logic
    assert 'hints.current_role?.value' in logic



def test_dictionary_ignores_goal_occurrence_but_finds_demonstrated_work():
    from backend.services.dictionary import suggest
    cv = (
        'I am interested in learning SQL. '
        'I used SQL to query monthly reports for the team.'
    )
    sql = [x for x in suggest(cv) if x['skill_id'] == 'SK001']
    assert len(sql) == 1
    assert 'used SQL' in sql[0]['excerpt']
    assert 'interested in' not in sql[0]['excerpt']


def test_dictionary_only_goal_does_not_claim_a_skill():
    from backend.services.dictionary import suggest
    cv = 'My goal is to learn SQL. I am interested in Python programming.'
    found = {x['skill_id'] for x in suggest(cv)}
    assert 'SK001' not in found
    assert 'SK005' not in found



def test_scanned_pdf_without_transcript_fails_instead_of_hiding_missing_content(monkeypatch):
    import pytest
    from backend.providers.validation import IntegrationError
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'synthetic-test-key')
    fake = FakeClaude({
        'transcript': '', 'candidates': [],
        'profile': {
            'current_role': {'value': '', 'excerpt': ''},
            'education': {'value': '', 'excerpt': ''},
            'industry': {'value': '', 'excerpt': ''},
            'projects': [],
        },
    })
    with pytest.raises(IntegrationError, match='could not transcribe'):
        asyncio.run(claude_extract_pdf(
            b'%PDF-test', [''], SKILL, client=fake, include_details=True,
        ))
