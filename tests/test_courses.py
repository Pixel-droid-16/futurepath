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
    # Known gaps: no open, currently running course was found on a provider page (checked 2026-10-22).
    # The 44-role catalogue added 17 skills (SK083-SK108) for which no verified course exists yet;
    # later phases should replace each with a provider-checked course. The claim set is data-driven,
    # so a new gap anywhere else fails this test on purpose.
    assert required-covered<={'SK051','SK067',
        'SK083','SK086','SK087','SK088','SK089','SK091','SK092','SK095',
        'SK097','SK098','SK100','SK103','SK104','SK105','SK106','SK107','SK108'}



def test_fullstack_role_has_linked_learning_resources():
    """New full-stack requirements must lead to real, checked learning links."""
    role = next(r for r in ROLES if r['id'] == 'fullstack-software-engineer')
    required = {s['skill_id'] for s in role['skills']}
    new_required = {'SK109', 'SK110', 'SK111', 'SK112', 'SK114', 'SK115'}
    assert new_required <= required
    for sid in new_required:
        learning = [c for c in COURSES if sid in c['skill_ids']]
        assert learning and all(c.get('checked') and c['url'].startswith('https://') for c in learning)
