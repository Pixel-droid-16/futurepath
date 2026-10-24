"""Semantic and related-skill layer: cached vectors, transfer credit, profile fit and diversity."""
import json
from datetime import date
from pathlib import Path

import pytest

from backend import semantic
from backend.catalog import ROLES,SKILL_INDEX,RESOURCES
from backend.engine import rank_role,recommend
from backend.signals.demand import role_demand

ROOT=Path(__file__).resolve().parents[1]
SNAPSHOT=json.loads((ROOT/'data'/'snapshots.json').read_text(encoding='utf8'))[0]

def _jaccard(a,b):
    left={x['skill_id'] for x in a['gaps']};right={x['skill_id'] for x in b['gaps']}
    return len(left&right)/len(left|right)

def test_cached_vectors_cover_the_catalogue():
    data=json.loads((ROOT/'data'/'semantic_vectors.json').read_text(encoding='utf8'))
    assert data['model']==semantic.MODEL_NAME and data['dim']==384
    assert set(data['roles'])=={r['id'] for r in ROLES}
    assert set(data['skills'])==set(SKILL_INDEX)

def test_curated_related_skill_gives_partial_credit_not_readiness():
    profile={'skills':{'SK027':4}}  # Dashboard design confirmed, Data visualisation unknown
    row=recommend(ROLES,profile,SNAPSHOT,SKILL_INDEX,RESOURCES,selected_role='data-analyst')[0]
    gap=next(g for g in row['gaps'] if g['skill_id']=='SK004')
    assert gap['confirmed'] is None and gap['status']=='unknown'
    assert gap['transfer_from']=='Dashboard design' and gap['transfer_credit']>0
    assert row['match']['transfer_skill']>0
    assert row['readiness'] is None  # exact-only readiness is not inflated by related skills

def test_related_skill_pairs_are_symmetric_and_blocked_pairs_are_zero():
    assert semantic.transfer_similarity('SK004','SK027')==semantic.transfer_similarity('SK027','SK004')
    assert semantic.transfer_similarity('SK019','SK045')==0.0

@pytest.mark.skipif(not semantic.status()['runtime_available'],reason='fastembed not installed')
def test_profile_text_prefers_a_matching_career():
    text='Hospital nurse moving into health informatics and clinical data governance.'
    relevant,_=semantic.text_fit(text,'health-informatics')
    unrelated,_=semantic.text_fit(text,'animation-vfx-pipeline-td')
    assert relevant is not None and unrelated is not None
    assert relevant>unrelated+20

def test_published_base_formula_without_personalisation():
    row=recommend(ROLES,{'skills':{'SK001':3}},SNAPSHOT,SKILL_INDEX,RESOURCES,selected_role='data-analyst')[0]
    assert row['match']['weights']=={'skill':pytest.approx(0.55),'demand':pytest.approx(0.45)}
    assert row['match']['text_fit'] is None and row['match']['sector'] is None


def test_interest_sector_and_text_reserve_fixed_weights():
    interest=recommend(ROLES,{'skills':{'SK001':3},'riasec':{t:0.5 for t in 'RIASEC'}},SNAPSHOT,SKILL_INDEX,RESOURCES,selected_role='data-analyst')[0]
    assert interest['match']['weights']=={'skill':pytest.approx(0.45),'demand':pytest.approx(0.35),'interest':pytest.approx(0.20)}
    sector=recommend(ROLES,{'skills':{'SK001':3},'interests':['Technology & AI']},SNAPSHOT,SKILL_INDEX,RESOURCES,selected_role='data-analyst')[0]
    assert sector['match']['weights']['sector']==pytest.approx(0.05)
    assert sector['match']['weights']['skill']==pytest.approx(0.5225)
    assert sector['match']['weights']['demand']==pytest.approx(0.4275)


def test_weights_sum_to_one_and_formula_is_visible():
    profile={'skills':{'SK001':3,'SK002':2,'SK003':4},'interests':['Technology & AI'],'current_role':'Data analyst','goals':'Build dashboards and analyse data.'}
    row=recommend(ROLES,profile,SNAPSHOT,SKILL_INDEX,RESOURCES,selected_role='data-analyst')[0]
    weights=row['match']['weights']
    assert abs(sum(weights.values())-1)<1e-9
    assert weights['text']==pytest.approx(0.15) and weights['sector']==pytest.approx(0.05)
    assert '×' in row['match']['formula'] and '=' in row['match']['formula']

def test_near_duplicate_careers_are_not_both_in_the_first_ten():
    profile={'skills':{'SK018':4,'SK020':4,'SK001':3,'SK002':4,'SK082':3}}
    rows=recommend(ROLES,profile,SNAPSHOT,SKILL_INDEX,RESOURCES)
    top={r['role_id'] for r in rows[:10]}
    twin={'risk-modelling-analyst','actuarial-valuation-specialist'}
    assert len(top&twin)<=1
    for i,a in enumerate(rows[:10]):
        for b in rows[i+1:10]:
            assert _jaccard(a,b)<0.85

def test_thin_signal_evidence_is_pulled_toward_neutral():
    role=next(r for r in ROLES if r['id']=='data-analyst')
    signal={'title':'t','source_name':'s','published_date':date.today().isoformat(),'url':'u','direction':'emerging','strength':3,
            'role_ids':['data-analyst'],'skill_ids':[],'tagged_by':'curated'}
    demand=role_demand(role,[signal],date.today())
    assert demand['confidence']=='low' and demand['reliability']<1
    row=rank_role(role,{'skills':{}},SNAPSHOT,SKILL_INDEX,RESOURCES,demand=demand)
    assert 50<row['match']['demand']<demand['score']
