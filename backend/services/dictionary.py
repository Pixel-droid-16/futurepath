"""Offline catalogue matches backed by CV quotes; never infer proficiency."""
import re
from ..catalog import SKILLS
from ..providers.validation import is_interest_evidence


def suggest(text, excerpt_before=35, excerpt_after=45):
    """Find each skill's first non-aspirational occurrence with sentence-bounded evidence."""
    candidates = []
    for skill in SKILLS:
        selected = None
        for alias in [skill['name']] + skill.get('aliases', []):
            expression = re.compile(r'(?<!\w)' + re.escape(alias) + r'(?!\w)', re.I)
            for hit in expression.finditer(text):
                left = max((text.rfind(char, 0, hit.start()) + 1 for char in '.!?\n•'), default=0)
                right_positions = [text.find(char, hit.end()) for char in '.!?\n•']
                right = min((pos for pos in right_positions if pos >= 0), default=len(text))
                start = max(left, hit.start() - excerpt_before)
                end = min(right, hit.end() + excerpt_after)
                while start > left and text[start - 1].isalnum():
                    start -= 1
                while end < right and text[end].isalnum():
                    end += 1
                excerpt = text[start:end].strip()
                if not excerpt or is_interest_evidence(excerpt, text):
                    continue
                selected = excerpt
                break
            if selected:
                break
        if selected:
            candidates.append({
                'skill_id': skill['id'], 'name': skill['name'],
                'excerpt': selected, 'method': 'dictionary suggestion',
                'proficiency': None,
            })
    return candidates
