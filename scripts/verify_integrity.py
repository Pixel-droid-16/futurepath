"""Check original hashes plus explicitly reviewed evolution; never refresh hashes.

See docs/INTEGRITY_REVIEW.md. This checks listed files, not the entire repository.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent.parent


def protected_design(relative):
    return (relative.startswith(('frontend/assets/', 'frontend/uploads/'))
            or relative in {'frontend/style.css', 'frontend/app.js',
                            'frontend/hero.svg', 'frontend/image-slot.js',
                            'frontend/support.js'})


def load_manifest(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'duplicate entry: {key}')
            result[key] = value
        return result

    manifest = json.loads(path.read_text(encoding='utf8'), object_pairs_hook=unique)
    if not isinstance(manifest, dict):
        raise ValueError(f'{path.name} must be an object')
    for relative, digest in manifest.items():
        parts = PurePosixPath(relative)
        if (parts.is_absolute() or '..' in parts.parts or '\\' in relative
                or str(parts) != relative or not parts.parts):
            raise ValueError(f'unsafe path: {relative}')
        if not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest):
            raise ValueError(f'invalid SHA256: {relative}')
    return manifest


def verify(root=ROOT):
    root = Path(root)
    try:
        baseline = load_manifest(root / 'docs/ORIGINAL_FILE_HASHES.json')
        reviewed = load_manifest(root / 'docs/REVIEWED_FILE_HASHES.json')
        for relative, digest in reviewed.items():
            if relative not in baseline:
                raise ValueError(f'reviewed entry not in original manifest: {relative}')
            if protected_design(relative):
                raise ValueError(f'protected design cannot be overridden: {relative}')
            if digest == baseline[relative]:
                raise ValueError(f'redundant reviewed entry: {relative}')
    except (OSError, ValueError) as exc:
        print(f'INTEGRITY MANIFEST ERROR: {exc}')
        return False

    errors = []
    original_count = reviewed_count = 0
    for relative, original in baseline.items():
        path = root / relative
        if not path.is_file() or path.is_symlink():
            errors.append(f'MISSING OR NON-REGULAR: {relative}')
            continue
        try:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError as exc:
            errors.append(f'UNREADABLE: {relative}: {exc}')
            continue
        expected = reviewed.get(relative, original)
        if digest != expected:
            kind = 'reviewed' if relative in reviewed else 'original'
            errors.append(f'CHANGED ({kind} baseline): {relative}')
        elif relative in reviewed:
            reviewed_count += 1
        else:
            original_count += 1
    if errors:
        print('INTEGRITY CHECK FAILED:')
        for error in errors:
            print(' -', error)
        print('Review the diff and docs/INTEGRITY_REVIEW.md; do not auto-refresh hashes.')
        return False
    print(f'PASS: {original_count} listed files match the original hashes.')
    print(f'PASS: {reviewed_count} listed files match documented reviewed hashes.')
    print('Protected original design assets remain byte-identical; no files are skipped.')
    return True


if __name__ == '__main__':
    sys.exit(0 if verify() else 1)
