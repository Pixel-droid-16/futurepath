from backend.catalog import RESOURCES, ROLES, SKILLS, SKILL_INDEX, load
from backend.engine import rank_role

VALID_SDGS=set(range(1,18))

def test_every_skill_has_valid_sdg_tags_and_explanation():
    assert SKILLS
    for skill in SKILLS:
        assert skill.get('sdgs')
        assert set(skill['sdgs']) <= VALID_SDGS
        assert skill.get('sdg_justification','').strip()

def test_recommendation_pathway_skills_have_sdg_metadata():
    recommendation=rank_role(ROLES[0],load('demo_profile.json'),load('snapshots.json')[0],SKILL_INDEX,RESOURCES)
    for step in recommendation['pathway']:
        skill=SKILL_INDEX[step['skill_id']]
        assert step['skill'] == skill['name']
        assert skill['sdgs']
        assert skill['sdg_justification']
