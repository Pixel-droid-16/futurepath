"""Review-only profile hints from plain CV text, never automatic identity or proficiency.

This parser intentionally reads explicit document sections and exact evidence
snippets. It is independent of provider/model availability and does not return
contact details, scanned-image bytes or the entire CV transcription.
"""
import re


HEADERS = {
    'SUMMARY', 'PROFILE', 'ABOUT ME', 'EDUCATION', 'TECHNICAL SKILLS',
    'SKILLS', 'PROJECTS', 'AWARDS & ACHIEVEMENTS', 'ACHIEVEMENTS',
    'CERTIFICATIONS', 'CERTIFICATES', 'LEADERSHIP', 'EXPERIENCE',
    'WORK EXPERIENCE', 'BUSINESS EXPERIENCE', 'CAREER FOCUS', 'REFERENCES',
    'INTERESTS', 'CONTACT', 'TECHNICAL STACK',
}


def sections_from(text):
    sections, current = {}, None
    for raw in (text or '').splitlines():
        line = raw.strip().strip('\x7f•*- ').strip()
        if not line:
            continue
        key = re.sub(r'\s+', ' ', line).strip(':').upper()
        if key in HEADERS:
            current = key
            sections.setdefault(key, [])
        elif current:
            sections[current].append(line)
    return sections


def _claim(value, excerpt):
    if not value or not excerpt or len(value) > 160 or len(excerpt) > 300:
        return None
    if '@' in excerpt or 'http://' in excerpt or 'https://' in excerpt:
        return None
    return {'value': value, 'excerpt': excerpt}


def extract_profile_hints(text):
    parts = sections_from(text)
    result = {}

    # A CV summary can describe a role without proving a current job. The
    # editable review panel treats this as a suggestion, never employment proof.
    profile_lines = parts.get('SUMMARY', []) + parts.get('PROFILE', [])
    for line in profile_lines:
        match = re.search(r'\b(full[- ]stack builder|full[- ]stack developer|software developer|'
                          r'web developer|data analyst|frontend developer|backend developer)\b',
                          line, re.I)
        if match:
            result['current_role'] = _claim(match.group(0), match.group(0))
            break

    education = parts.get('EDUCATION', [])
    for i, line in enumerate(education):
        if re.search(r'\b(bachelor|master|doctor|phd)\b', line, re.I):
            upcoming = ' '.join(education[i:i+3])
            is_current = bool(re.search(r'\b(?:to|[-–])\s*present\b|\bongoing\b', upcoming, re.I))
            value = line + (' (in progress)' if is_current else '')
            result['education'] = _claim(value, line)
            break

    for line in education:
        if re.search(r'\bMatriculation Certificate\b', line, re.I):
            result['completed_qualification'] = _claim(
                'Malaysian Matriculation Certificate', line,
            )
            break
        if re.search(r'\b(?:Diploma|STPM)\b', line, re.I):
            # Expose the literal qualification for review, without guessing an equivalence.
            result['completed_qualification'] = _claim(line, line)
            break

    for section, key, max_items in [
        ('PROJECTS', 'projects', 6),
        ('AWARDS & ACHIEVEMENTS', 'achievements', 4),
        ('CERTIFICATIONS', 'certifications', 4),
    ]:
        rows = []
        for line in parts.get(section, []):
            if key == 'projects':
                if ' | ' not in line:
                    continue
                value = line.split(' | ', 1)[0].strip()
            elif key == 'achievements':
                if not re.search(r'\b(award|place|gold|silver|bronze|champion|platinum)\b', line, re.I):
                    continue
                value = line
            else:
                if len(line) < 10 or re.fullmatch(r'\d{4}', line):
                    continue
                value = line.split(':', 1)[0].strip()
            item = _claim(value[:160], line)
            if item and item['value'] not in [p['value'] for p in rows]:
                rows.append(item)
            if len(rows) >= max_items:
                break
        if rows:
            result[key] = rows

    return result
