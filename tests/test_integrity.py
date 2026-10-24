"""Isolated fixtures: never mutate real app assets to test integrity failures."""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.verify_integrity import ROOT, verify


@pytest.fixture
def tree(tmp_path):
    for name in ('ORIGINAL_FILE_HASHES.json', 'REVIEWED_FILE_HASHES.json'):
        path = tmp_path / 'docs' / name
        path.parent.mkdir(exist_ok=True)
        shutil.copyfile(ROOT / 'docs' / name, path)
    baseline = json.loads((ROOT / 'docs/ORIGINAL_FILE_HASHES.json').read_text())
    for name in baseline:
        dest = tmp_path / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, dest)
    return tmp_path


def test_reviewed_tree_passes(tree):
    assert verify(tree)


def test_cli_rejects_reviewed_mutation(tree):
    """Exercise the same command/exit status used by the repository check."""
    script = tree / 'scripts' / 'verify_integrity.py'
    script.parent.mkdir(exist_ok=True)
    shutil.copyfile(ROOT / 'scripts/verify_integrity.py', script)
    command = [sys.executable, str(script)]
    before = subprocess.run(command, capture_output=True, text=True)
    # Other release files can already be out of review. The mutation must
    # introduce this specific failure, not merely observe an existing red check.
    assert 'backend/app.py' not in before.stdout
    path = tree / 'backend/app.py'
    path.write_bytes(path.read_bytes() + b'\n# unreviewed mutation\n')
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 1
    assert 'CHANGED (reviewed baseline): backend/app.py' in result.stdout


@pytest.mark.parametrize('name', [
    'frontend/style.css', 'frontend/support.js',
    'frontend/assets/hero-career-growth.svg',
    'data/snapshots.json', 'data/roles.json', 'backend/engine.py',
    'backend/app.py', 'backend/ai_providers.py', 'README.md', 'frontend/index.html',
])
@pytest.mark.parametrize('operation', ['change', 'remove'])
def test_regressions_fail(tree, name, operation, capsys):
    path = tree / name
    if operation == 'remove':
        path.unlink()
    else:
        path.write_bytes(path.read_bytes() + b'\nchanged')
    assert not verify(tree)
    assert name in capsys.readouterr().out


@pytest.mark.parametrize('kind', ['protected', 'unknown', 'redundant', 'digest', 'path',
                                  'duplicate', 'json', 'missing'])
def test_invalid_review_manifest_fails(tree, kind):
    path = tree / 'docs/REVIEWED_FILE_HASHES.json'
    manifest = json.loads(path.read_text())
    original = json.loads((tree / 'docs/ORIGINAL_FILE_HASHES.json').read_text())
    if kind == 'protected':
        manifest['frontend/style.css'] = '0' * 64
    elif kind == 'unknown':
        manifest['unreviewed.txt'] = '0' * 64
    elif kind == 'redundant':
        manifest['README.md'] = original['README.md']
    elif kind == 'digest':
        manifest['README.md'] = None
    elif kind == 'path':
        manifest['../outside'] = '0' * 64
    elif kind == 'duplicate':
        path.write_text('{"README.md":"' + '0' * 64 + '","README.md":"' + '1' * 64 + '"}')
    elif kind == 'json':
        path.write_text('{')
    elif kind == 'missing':
        path.unlink()
    if kind not in {'duplicate', 'json', 'missing'}:
        path.write_text(json.dumps(manifest))
    assert not verify(tree)


def test_every_override_is_a_changed_file_and_documented():
    reviewed = json.loads((ROOT / 'docs/REVIEWED_FILE_HASHES.json').read_text())
    report = (ROOT / 'docs/INTEGRITY_REVIEW.md').read_text()
    assert len(reviewed) == 20
    for name, digest in reviewed.items():
        assert f'`{name}`' in report
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest
