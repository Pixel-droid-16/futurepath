"""Explicit post-manifest coverage; no hash generation, app import or network."""
import ast
from datetime import date
import json
import math
from pathlib import Path
import sys
from urllib.parse import urlsplit

try:
    from scripts.build_frontend import assemble_home
except ModuleNotFoundError:
    from build_frontend import assemble_home

ROOT = Path(__file__).resolve().parents[1]
# Independent of the builder: deleting a fragment from its list must not make
# the coverage check silently forget it.
ACTIVE_FRAGMENTS = (
    'shell/document_before_css.html', 'styles/v2_theme.css',
    'shell/document_after_css.html',
    'pages/home.html', 'pages/start.html', 'pages/results.html',
    'pages/pathway.html', 'pages/signals.html', 'pages/about.html',
    'shell/after_pages.html',
    'logic/translations.js', 'logic/sdg_colors.js', 'logic/career_cards.js',
    'logic/declining_careers.js', 'logic/navigation_labels.js',
    'logic/live_career_adapter.js', 'logic/state_and_actions.js',
    'logic/state_values_start.js', 'logic/career_ranking_view.js',
    'logic/start_confirm_view.js', 'logic/signal_filters_view.js',
    'logic/skill_trends_view.js', 'logic/home_signal_feed_view.js',
    'logic/sdg_mapping_view.js', 'logic/live_scenario_comparison_view.js',
    'logic/page_bindings_view.js', 'shell/document_end.html',
)
RETIRED_FRAGMENTS = (
    'pages/intake.html', 'pages/login.html',
    'logic/intake_sample_skills.js', 'logic/intake_skill_view.js',
)
ROUTES = (
    '__init__', 'ai', 'careers', 'history', 'learning', 'matches', 'pages',
    'profiles', 'radar', 'scenarios', 'skills', 'snapshots', 'curator',
    'cv_upload', 'meta', 'signals',
)
SERVICES = (
    '__init__', 'documents', 'cv_profile', 'ai_extraction', 'dictionary',
    'recommendations',
)
INVENTORIES = {
    'frontend/mockup_source': ACTIVE_FRAGMENTS + RETIRED_FRAGMENTS,
    'backend/routes': tuple(f'{name}.py' for name in ROUTES),
    'backend/services': tuple(f'{name}.py' for name in SERVICES),
}


def course_errors(root):
    """Validate raw rows before catalogue merging can hide missing extra data."""
    rows = json.loads((root / 'data/extra_courses.json').read_text(encoding='utf8'))
    base = json.loads((root / 'data/courses.json').read_text(encoding='utf8'))
    skills = {row['id'] for row in json.loads(
        (root / 'data/skills.json').read_text(encoding='utf8'))}
    if not isinstance(rows, list) or not rows:
        return ['data/extra_courses.json must be a nonempty list']
    errors = []
    seen = {row['id'] for row in base}
    for i, row in enumerate(rows):
        try:
            assert isinstance(row, dict), 'row must be an object'
            for field in ('id', 'title', 'provider', 'url', 'language', 'notes', 'checked'):
                assert isinstance(row.get(field), str) and row[field].strip(), field
            assert row['id'] not in seen, 'duplicate course id'
            seen.add(row['id'])
            url = urlsplit(row['url'])
            assert url.scheme == 'https' and url.hostname, 'HTTPS URL'
            assert not url.username and not url.password, 'URL credentials'
            assert row.get('cost') in ('free', 'low', 'hrdc_claimable'), 'cost'
            hours = row.get('hours')
            assert type(hours) in (int, float) and math.isfinite(hours) and hours > 0, 'hours'
            assert type(row.get('hours_estimated')) is bool, 'hours_estimated'
            ids = row.get('skill_ids')
            assert isinstance(ids, list) and ids, 'skill_ids'
            assert all(isinstance(s, str) and s in skills for s in ids), 'unknown skill'
            assert len(ids) == len(set(ids)), 'duplicate skill'
            assert date.fromisoformat(row['checked']).isoformat() == row['checked'], 'checked date'
        except (AssertionError, ValueError, TypeError) as exc:
            errors.append(f'data/extra_courses.json row {i}: {exc}')
    return errors


def coverage_errors(root=ROOT):
    root = Path(root)
    errors = []
    for directory, names in INVENTORIES.items():
        folder = root / directory
        expected = set(names)
        actual = {p.relative_to(folder).as_posix() for p in folder.rglob('*')
                  if (p.is_file() or p.is_symlink())
                  and '__pycache__' not in p.parts and p.suffix != '.pyc'}
        for name in sorted(actual - expected):
            errors.append(f'UNCLASSIFIED: {directory}/{name}')
        for name in names:
            path = folder / name
            if not path.is_file() or any(p.is_symlink() for p in (path, *path.parents)):
                errors.append(f'MISSING OR NON-REGULAR: {directory}/{name}')
            elif path.suffix == '.py':
                try:
                    ast.parse(path.read_text(encoding='utf8'), filename=str(path))
                except (OSError, SyntaxError, UnicodeError) as exc:
                    errors.append(f'INVALID PYTHON: {directory}/{name}: {exc}')
    try:
        source = root / 'frontend/mockup_source'
        expected = ''.join((source / name).read_text(encoding='utf8')
                           for name in ACTIVE_FRAGMENTS)
        built = assemble_home(source)
        if built != expected:
            errors.append('ASSEMBLY RECIPE DRIFT: builder differs from reviewed fragment order')
        if built != (root / 'frontend/index.html').read_text(encoding='utf8'):
            errors.append('ASSEMBLY OUTPUT DRIFT: frontend/index.html differs from source')
    except (OSError, UnicodeError) as exc:
        errors.append(f'ASSEMBLY INPUT ERROR: {exc}')
    try:
        path = root / 'data/extra_courses.json'
        if any(p.is_symlink() for p in (path, *path.parents)):
            errors.append('NON-REGULAR: data/extra_courses.json')
        else:
            errors.extend(course_errors(root))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f'COURSE INPUT ERROR: {exc}')
    return errors


def main():
    errors = coverage_errors()
    if errors:
        print('\n'.join(errors))
        return 1
    print('PASS: explicit modular inventory, assembly and extra-course schema.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
