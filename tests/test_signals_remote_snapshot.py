"""Remote snapshot safety, no network or paid models."""
from datetime import date
import httpx
import pytest
from backend.signals import snapshot

def example():
    return {
        'external_id':'fictional:verified-source','feed_key':'fictional',
        'title':'Malaysia cybersecurity jobs expand','source_name':'Fictional source',
        'source_type':'news','url':'https://example.org/article',
        'published_date':date.today().isoformat(),'fetched_at':date.today().isoformat(),
        'summary':'Evidence-backed cybersecurity jobs expansion',
        'direction':'emerging','strength':2,'role_ids':['cybersecurity-analyst'],
        'skill_ids':['SK011'],'tagged_by':'claude'
    }

def test_remote_validator_keeps_only_structured_verified_sources():
    approved=example()
    assert snapshot.validate_signal(approved)['strength']==2
    for variant in ({**approved,'tagged_by':'keyword'},
                    {**approved,'strength':5},
                    {**approved,'role_ids':['invented']},
                    {**approved,'url':'http://localhost/article'},
                    {**approved,'direction':'increasing'}):
        assert snapshot.validate_signal(variant) is None

def test_snapshot_document_rejects_invalid_schema_and_deduplicates():
    row=example()
    good={'schema_version':1,'checked_at':None,'status':'ok',
          'last_successful_at':None,'ai_enabled':True,'signals':[row,row]}
    rows,meta=snapshot.validate_document(good)
    assert len(rows)==1 and meta['ai_enabled']
    with pytest.raises(ValueError):
        snapshot.validate_document({**good,'schema_version':2})

def test_opt_in_and_no_network_when_disabled(monkeypatch):
    monkeypatch.delenv('SIGNALS_REMOTE_SNAPSHOT_ENABLED',raising=False)
    monkeypatch.setattr(snapshot.httpx,'get',lambda *a,**kw: pytest.fail('network called'))
    assert snapshot.read_snapshot()==([],None)
