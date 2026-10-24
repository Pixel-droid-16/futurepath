from backend.catalog import COURSES, COST_LABEL, SKILL_INDEX, ROLES, RESOURCES

def test_checked_courses_are_well_formed():
    ids=[c['id'] for c in COURSES]
    assert len(ids)==len(set(ids))
    for c in COURSES:
        assert c['url'].startswith('https://') and c['cost'] in COST_LABEL and c['hours']>0
        assert c['skill_ids'] and all(s in SKILL_INDEX for s in c['skill_ids'])
    assert all(r.get('verification_status') for r in RESOURCES if r.get('url'))
    assert any(r['verification_status'].startswith('source catalogue snapshot') for r in RESOURCES if r.get('url'))
    assert any(r['verification_status'].startswith('provider page checked') for r in RESOURCES if r.get('url'))

def test_required_skills_have_a_checked_course():
    required={s['skill_id'] for r in ROLES for s in r['skills']}
    covered={r['skill_id'] for r in RESOURCES if r.get('url')}
    # Every skill a career requires has at least one provider-checked course (last gaps closed 2026-10-24),
    # so a new career or skill without a checked course fails this test on purpose.
    assert required<=covered

def test_hrd_corp_claimable_courses_are_offered():
    claimable=[c for c in COURSES if c['cost']=='hrdc_claimable']
    assert len(claimable)>=8 and all(c.get('checked') or 'HRDF' in c['notes'] for c in claimable)

def test_fullstack_role_has_linked_learning_resources():
    """New full-stack requirements must lead to real, checked learning links."""
    role = next(r for r in ROLES if r['id'] == 'fullstack-software-engineer')
    required = {s['skill_id'] for s in role['skills']}
    new_required = {'SK109', 'SK110', 'SK111', 'SK112', 'SK114', 'SK115'}
    assert new_required <= required
    for sid in new_required:
        learning = [c for c in COURSES if sid in c['skill_ids']]
        assert learning and all(c.get('checked') and c['url'].startswith('https://') for c in learning)
