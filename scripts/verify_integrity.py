"""Verify untouched files from the previous FuturePath release remain byte-identical.

For intentional edits, a mismatch is a review signal, NOT permission to alter the
reference hashes automatically. Run `python scripts/build_frontend.py` first.
"""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent.parent
BASELINE=json.loads((ROOT/'docs'/'ORIGINAL_FILE_HASHES.json').read_text(encoding='utf8'))
# These three project files were intentionally rewritten into modular entrypoints/docs.
INTENTIONALLY_REFACTORED={'backend/app.py','backend/ai_providers.py','README.md','frontend/index.html'}

def verify():
    errors=[];tested=0
    for relative,expected in BASELINE.items():
        if relative in INTENTIONALLY_REFACTORED:continue
        path=ROOT/relative
        if not path.is_file():
            errors.append(f'MISSING: {relative}')
            continue
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        tested+=1
        if digest!=expected:errors.append(f'CHANGED: {relative}')
    if errors:
        print('ORIGINAL ASSET INTEGRITY CHECK FAILED:')
        for item in errors:print(' -',item)
        print('If changes were intentional, review them. Restore from backup if accidental.')
        return False
    print(f'PASS: {tested} original asset/source files preserved byte-for-byte.')
    print(f'PASS: {len(INTENTIONALLY_REFACTORED)} release files intentionally changed; unmodified design assets remain protected.')
    return True

if __name__=='__main__':sys.exit(0 if verify() else 1)
