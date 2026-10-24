"""Fault injection in disposable trees, never in the running application's data."""
import json
import shutil
import subprocess
import sys

import pytest

from scripts import check_modular_coverage as coverage


@pytest.fixture
def modular_tree(tmp_path):
    for directory in coverage.INVENTORIES:
        shutil.copytree(coverage.ROOT / directory, tmp_path / directory,
                        ignore=shutil.ignore_patterns('__pycache__'))
    for name in ('frontend/index.html', 'data/extra_courses.json',
                 'data/courses.json', 'data/skills.json'):
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(coverage.ROOT / name, target)
    return tmp_path


def test_current_modular_coverage():
    assert coverage.coverage_errors() == []


REQUIRED = [f'{folder}/{name}' for folder, names in coverage.INVENTORIES.items()
            for name in names] + ['data/extra_courses.json']


@pytest.mark.parametrize('name', REQUIRED)
def test_each_missing_file_fails(modular_tree, name):
    (modular_tree / name).unlink()
    errors = coverage.coverage_errors(modular_tree)
    assert errors and any(name in error for error in errors)


@pytest.mark.parametrize('directory', coverage.INVENTORIES)
def test_new_files_require_explicit_classification(modular_tree, directory):
    (modular_tree / directory / 'unreviewed.txt').write_text('new')
    assert any('UNCLASSIFIED' in e for e in coverage.coverage_errors(modular_tree))


def test_source_and_output_drift_fail_independently(modular_tree):
    path = modular_tree / 'frontend/mockup_source/pages/start.html'
    path.write_text(path.read_text() + '\n<!-- intentional test edit -->')
    assert any('OUTPUT DRIFT' in e for e in coverage.coverage_errors(modular_tree))
    # Legitimate source evolution plus rebuild is accepted by structural checks.
    output = modular_tree / 'frontend/index.html'
    output.write_text(coverage.assemble_home(modular_tree / 'frontend/mockup_source'))
    assert coverage.coverage_errors(modular_tree) == []
    output.write_text(output.read_text() + '\n<!-- generated-only edit -->')
    assert any('OUTPUT DRIFT' in e for e in coverage.coverage_errors(modular_tree))


@pytest.mark.parametrize('operation', ['omit', 'duplicate', 'reorder', 'retired'])
def test_recipe_drift_fails_even_when_output_matches(modular_tree, monkeypatch, operation):
    source = modular_tree / 'frontend/mockup_source'
    names = list(coverage.ACTIVE_FRAGMENTS)
    if operation == 'omit':
        names.pop(4)
    elif operation == 'duplicate':
        names.insert(4, names[4])
    elif operation == 'reorder':
        names[4], names[5] = names[5], names[4]
    else:
        names.append(coverage.RETIRED_FRAGMENTS[0])
    drifted = ''.join((source / n).read_text() for n in names)
    monkeypatch.setattr(coverage, 'assemble_home', lambda source: drifted)
    (modular_tree / 'frontend/index.html').write_text(drifted)
    assert any('RECIPE DRIFT' in e for e in coverage.coverage_errors(modular_tree))


def test_symlink_and_invalid_python_fail(modular_tree):
    path = modular_tree / 'backend/routes/meta.py'
    path.unlink()
    path.symlink_to(modular_tree / 'backend/routes/skills.py')
    assert any('NON-REGULAR: backend/routes/meta.py' in e
               for e in coverage.coverage_errors(modular_tree))
    path.unlink()
    path.write_text('def invalid(')
    assert any('INVALID PYTHON: backend/routes/meta.py' in e
               for e in coverage.coverage_errors(modular_tree))


@pytest.mark.parametrize('field,value', [
    ('id', ''), ('title', None), ('provider', ''),
    ('url', 'http://example.com'), ('url', 'https://'),
    ('cost', 'unknown'), ('hours', 0), ('hours', True), ('hours', float('nan')),
    ('hours_estimated', 'yes'), ('skill_ids', []), ('skill_ids', ['unknown']),
    ('checked', '2026-99-99'), ('notes', None),
])
def test_invalid_course_schema_fails(modular_tree, field, value):
    path = modular_tree / 'data/extra_courses.json'
    rows = json.loads(path.read_text())
    rows[0][field] = value
    path.write_text(json.dumps(rows))
    assert any('extra_courses.json row 0' in e
               for e in coverage.coverage_errors(modular_tree))


@pytest.mark.parametrize('kind', ['empty', 'object', 'malformed', 'duplicate', 'base_collision'])
def test_course_collection_failures(modular_tree, kind):
    path = modular_tree / 'data/extra_courses.json'
    rows = json.loads(path.read_text())
    if kind == 'duplicate':
        rows.append(rows[0])
    elif kind == 'base_collision':
        rows[0]['id'] = json.loads((modular_tree / 'data/courses.json').read_text())[0]['id']
    elif kind == 'empty':
        rows = []
    elif kind == 'object':
        rows = {}
    path.write_text('{' if kind == 'malformed' else json.dumps(rows))
    assert coverage.coverage_errors(modular_tree)


def test_cli_has_nonzero_exit_on_missing_module(modular_tree):
    scripts = modular_tree / 'scripts'
    scripts.mkdir()
    for name in ('check_modular_coverage.py', 'build_frontend.py'):
        shutil.copyfile(coverage.ROOT / 'scripts' / name, scripts / name)
    command = [sys.executable, str(scripts / 'check_modular_coverage.py')]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    (modular_tree / 'backend/services/cv_profile.py').unlink()
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 1
    assert 'backend/services/cv_profile.py' in result.stdout
