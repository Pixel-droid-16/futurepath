<<<<<<< HEAD
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS = ROOT / "frontend" / "mockup_source" / "logic" / "translations.js"


def _entries(source, name, end_marker):
    start = source.index(f"const {name} = {{")
    block = source[start:source.index(end_marker, start)]
    entries = []
    for line in block.splitlines():
        match = re.match(r'\s*"((?:[^"\\]|\\.)+)": (\[.*\]),?\s*$', line)
        if match:
            key = json.loads(f'"{match.group(1)}"')
            entries.append((key, json.loads(match.group(2))))
    return entries


def test_translation_catalogue_has_complete_locale_values_without_duplicate_keys():
    source = TRANSLATIONS.read_text(encoding="utf-8")
    assert 'const FP_LOCALES = ["en", "ms", "zh"]' in source

    entries = _entries(source, "FP_TEXT", "const FP_SKILL_SDG_TEXT")
    assert entries
    assert all(len(values) == 3 for _, values in entries)
    assert not [key for key, count in Counter(key for key, _ in entries).items() if count > 1]
    translated = dict(entries)
    assert all(translated["Choose a career on the results page"][1:])
    assert all(translated["Select a career to see its SDG connection."][1:])


def test_every_skill_sdg_explanation_is_translated():
    source = TRANSLATIONS.read_text(encoding="utf-8")
    entries = _entries(source, "FP_SKILL_SDG_TEXT", "const fpLocaleIndex")
    translated = {key: values for key, values in entries}
    skills = json.loads((ROOT / "data" / "skills.json").read_text(encoding="utf-8"))

    assert len(translated) == len(entries)
    assert all(len(values) == 2 and all(values) for values in translated.values())
    assert all(skill["sdg_justification"] in translated for skill in skills)


def test_generated_main_and_ai_lab_pages_include_translation_runtime():
    for path in (ROOT / "frontend" / "index.html", ROOT / "frontend" / "ai-lab.html"):
        assert "FP_SKILL_SDG_TEXT" in path.read_text(encoding="utf-8")


def test_start_profile_form_places_questions_in_check_step_and_uses_malaysian_education_options():
    source = (ROOT / "frontend" / "mockup_source" / "pages" / "start.html").read_text(encoding="utf-8")
    form_start = source.index('value="{{ isFormStep }}"')
    check_start = source.index('value="{{ isCheckStep }}"')
    quiz_start = source.index('value="{{ isQuizStep }}"')
    form = source[form_start:check_start]
    check = source[check_start:quiz_start]

    assert "Quick Questionnaire" not in form
    assert check.count("Quick Questionnaire") == 1
    assert "Headline" not in check
    assert 'Education Level<select' in form and 'Education Level<select' in check
    for qualification in ("UPSR", "PT3", "SPM", "STPM", "Diploma", "Bachelor's Degree", "Master's Degree", "Doctoral Degree (PhD)"):
        assert qualification in source
=======
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS = ROOT / "frontend" / "mockup_source" / "logic" / "translations.js"


def _entries(source, name, end_marker):
    start = source.index(f"const {name} = {{")
    block = source[start:source.index(end_marker, start)]
    entries = []
    for line in block.splitlines():
        match = re.match(r'\s*"((?:[^"\\]|\\.)+)": (\[.*\]),?\s*$', line)
        if match:
            key = json.loads(f'"{match.group(1)}"')
            entries.append((key, json.loads(match.group(2))))
    return entries


def test_translation_catalogue_has_complete_locale_values_without_duplicate_keys():
    source = TRANSLATIONS.read_text(encoding="utf-8")
    assert 'const FP_LOCALES = ["en", "ms", "zh"]' in source

    entries = _entries(source, "FP_TEXT", "const FP_SKILL_SDG_TEXT")
    assert entries
    assert all(len(values) == 3 for _, values in entries)
    assert not [key for key, count in Counter(key for key, _ in entries).items() if count > 1]
    translated = dict(entries)
    assert all(translated["Choose a career on the results page"][1:])
    assert all(translated["Select a career to see its SDG connection."][1:])


def test_every_skill_sdg_explanation_is_translated():
    source = TRANSLATIONS.read_text(encoding="utf-8")
    entries = _entries(source, "FP_SKILL_SDG_TEXT", "const fpLocaleIndex")
    translated = {key: values for key, values in entries}
    skills = json.loads((ROOT / "data" / "skills.json").read_text(encoding="utf-8"))

    assert len(translated) == len(entries)
    assert all(len(values) == 2 and all(values) for values in translated.values())
    assert all(skill["sdg_justification"] in translated for skill in skills)


def test_generated_main_and_ai_lab_pages_include_translation_runtime():
    for path in (ROOT / "frontend" / "index.html", ROOT / "frontend" / "ai-lab.html"):
        assert "FP_SKILL_SDG_TEXT" in path.read_text(encoding="utf-8")
>>>>>>> da0787dab49148d066631b796b12e2b882c85231
