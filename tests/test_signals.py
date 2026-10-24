"""Trend signal layer: feed parsing, guardrails, taggers, demand formula and the refresh pipeline."""
import asyncio,json
from datetime import date,timedelta
import httpx,pytest
from fastapi.testclient import TestClient
from backend import storage
from backend.app import app
from backend.catalog import ROLES,SKILLS
from backend.signals.demand import role_demand,recency_decay,is_ai_related
from backend.signals.fetch import parse_feed_xml
from backend.signals.guardrails import apply_guardrails
from backend.signals.refresh import refresh_signals
from backend.signals.tagging import ClaudeTagger,KeywordTagger
from tests.fake_claude import FakeClaude

TODAY=date(2026,10,22)
RSS_FEED={'kind':'rss','key':'test-rss','name':'Test feed','url':'https://feeds.test/rss','source_type':'news','max_items':10,'max_age_days':45}
RSS=f'''<rss><channel>
<item><title>Malaysia faces cybersecurity talent shortage as attacks rise - The Star</title><link>https://news.test/a</link><guid>a</guid>
 <pubDate>Mon, 20 Oct 2026 08:00:00 GMT</pubDate><description>&lt;b&gt;Employers&lt;/b&gt; need 12,000 more security staff.</description><source>The Star</source></item>
<item><title>Old story about jobs</title><link>https://news.test/b</link><pubDate>Mon, 01 Jan 2024 08:00:00 GMT</pubDate></item>
</channel></rss>'''
ATOM='''<feed xmlns="http://www.w3.org/2005/Atom"><entry><id>x1</id><title>Generative AI and labor markets</title>
<link href="https://arxiv.test/x1"/><published>2026-10-10T00:00:00Z</published><summary>Exposure of clerical tasks.</summary></entry></feed>'''
ROLE_IDS={r['id'] for r in ROLES};SKILL_IDS={s['id'] for s in SKILLS}
ITEM={'title':'Malaysia needs 12,000 cybersecurity workers','snippet':'Employers report a shortage.'}

def test_parses_rss_and_atom_and_drops_old_items():
    items=parse_feed_xml(RSS,RSS_FEED,today=TODAY)
    assert [i['title'] for i in items]==['Malaysia faces cybersecurity talent shortage as attacks rise']  # publisher suffix removed, 2024 item too old
    assert items[0]['source_name']=='The Star' and items[0]['published_date']=='2026-10-20' and items[0]['snippet'].startswith('Employers need')
    atom=parse_feed_xml(ATOM,{**RSS_FEED,'key':'test-atom','source_type':'research'},today=TODAY)
    assert atom[0]['url']=='https://arxiv.test/x1' and atom[0]['published_date']=='2026-10-10'

def test_guardrails_keep_catalogue_ids_and_reject_invented_numbers():
    base={'relevant':True,'reason':'r','direction':'emerging','strength':5,'summary':'Malaysia needs 12,000 workers.','role_ids':['cybersecurity-analyst','space-pilot'],'skill_ids':['SK011','SK999']}
    p,notes=apply_guardrails(ITEM,base,ROLE_IDS,SKILL_IDS)
    assert p['role_ids']==['cybersecurity-analyst'] and p['skill_ids']==['SK011'] and p['strength']==3 and 'dropped 2' in notes[0]
    p,notes=apply_guardrails(ITEM,{**base,'summary':'Malaysia needs 50,000 workers.'},ROLE_IDS,SKILL_IDS)
    assert p['summary']==ITEM['title'] and any('50000' in n for n in notes)
    assert apply_guardrails(ITEM,{**base,'role_ids':['space-pilot'],'skill_ids':[]},ROLE_IDS,SKILL_IDS)[0] is None
    assert apply_guardrails(ITEM,{**base,'relevant':False},ROLE_IDS,SKILL_IDS)[0] is None

def test_keyword_tagger_links_malaysian_items_and_skips_foreign_ones():
    catalog={'roles':ROLES,'skills':SKILLS}
    items=[{'title':'Malaysia faces cybersecurity talent shortage','snippet':''},
           {'title':'Philippines hires more cybersecurity workers','snippet':''},
           {'title':'Malaysian factories cut jobs as industrial automation spreads','snippet':''}]
    a,b,c=[o['proposal'] for o in asyncio.run(KeywordTagger().tag(items,catalog))]
    assert a['relevant'] and 'cybersecurity-analyst' in a['role_ids'] and a['direction']=='emerging'
    assert not b['relevant'] and 'another country' in b['reason']
    assert c['direction']=='declining' and 'automation-engineer' not in c['role_ids']  # the cause of a decline is not itself declining

def signal(**kw):
    return {'title':'t','source_name':'s','published_date':TODAY.isoformat(),'url':'u','direction':'emerging','strength':3,
            'role_ids':[],'skill_ids':[],'tagged_by':'curated',**kw}

def test_demand_formula_decay_skill_weight_and_caps():
    role=next(r for r in ROLES if r['id']=='data-analyst')
    assert recency_decay((TODAY-timedelta(days=365)).isoformat(),TODAY)==pytest.approx(0.5)
    assert role_demand(role,[],TODAY)['score']==50  # no signals: neutral
    direct=role_demand(role,[signal(role_ids=['data-analyst'])],TODAY)
    via_skill=role_demand(role,[signal(skill_ids=['SK001'])],TODAY)
    falling=role_demand(role,[signal(role_ids=['data-analyst'],direction='declining')],TODAY)
    assert direct['score']>via_skill['score']>50>falling['score']
    assert direct['cited'][0]['via']=='names this career'
    burst=role_demand(role,[signal(role_ids=['data-analyst'],tagged_by='claude',title=str(i)) for i in range(10)],TODAY)
    assert burst['raw']==pytest.approx(3)  # feed items naming a career add at most +3 together

def test_ai_related_signals_are_found_by_keyword():
    assert is_ai_related(signal(title='Generative AI reshapes banking'))
    assert is_ai_related(signal(title='Budget 2027', summary='Funding for robotics and automation training.'))
    assert not is_ai_related(signal(title='Malaysia trains sustainability staff'))  # "ai" inside words doesn't count
    assert not is_ai_related(signal(title='Green jobs grow', summary=None))

def test_rapid_scenario_counts_ai_signals_double_and_leaves_others():
    role=next(r for r in ROLES if r['id']=='data-analyst')
    ai=signal(role_ids=['data-analyst'],title='AI adoption grows')
    green=signal(role_ids=['data-analyst'],title='Green jobs grow')
    moderate=role_demand(role,[ai,green],TODAY)
    rapid=role_demand(role,[ai,green],TODAY,scenario='rapid')
    assert moderate['raw']==pytest.approx(6) and rapid['raw']==pytest.approx(9)
    assert rapid['baseline_score']==moderate['score']==moderate['baseline_score'] and rapid['score']>moderate['score']
    assert rapid['ai_signal_count']==1 and rapid['cited'][0]['ai_related']
    assert role_demand(role,[green],TODAY,scenario='rapid')['score']==role_demand(role,[green],TODAY)['score']
    falling=signal(role_ids=['data-analyst'],title='Automation cuts analyst jobs',direction='declining')
    assert role_demand(role,[falling],TODAY,scenario='rapid')['score']<role_demand(role,[falling],TODAY)['score']<50

def test_claude_tagger_tolerates_omitted_fields_for_irrelevant_items(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY','test-only')
    reply={'items':[{'index':0,'relevant':False,'reason':'stock news'},
                    {'index':1,'relevant':True,'reason':'r','direction':'emerging','strength':2,'summary':'s','role_ids':['data-analyst'],'skill_ids':[]}]}
    fake=FakeClaude(reply)
    item={'title':'a','source_name':'s','source_type':'news','published_date':'2026-10-01','snippet':''}
    first,second=asyncio.run(ClaudeTagger(client=fake).tag([item]*2,{'roles':ROLES,'skills':SKILLS}))
    assert first['ok'] and first['proposal']['relevant'] is False
    assert second['ok'] and second['proposal']['role_ids']==['data-analyst']
    sent=fake.requests[0]
    assert sent['output_config']['effort']=='low'
    role_enum=sent['output_config']['format']['schema']['properties']['items']['items']['properties']['role_ids']['items']['enum']
    assert set(role_enum)=={r['id'] for r in ROLES}

@pytest.fixture
def temp_db(tmp_path,monkeypatch):
    monkeypatch.setattr(storage,'DB',tmp_path/'signals_test.sqlite3')
    storage.init()
    return tmp_path

def test_refresh_pipeline_stores_audits_and_moves_ranking(temp_db,monkeypatch):
    monkeypatch.delenv('ADMIN_TOKEN',raising=False)
    recent=(date.today()-timedelta(days=2)).strftime('%a, %d %b %Y 08:00:00 GMT')
    rss=f'''<rss><channel>
    <item><title>Malaysia faces cybersecurity talent shortage as hiring jumps</title><link>https://news.test/1</link><pubDate>{recent}</pubDate></item>
    <item><title>Malaysia faces cybersecurity talent shortage as hiring jumps again</title><link>https://news.test/2</link><pubDate>{recent}</pubDate></item>
    <item><title>Celebrity wedding draws crowds</title><link>https://news.test/3</link><pubDate>{recent}</pubDate></item></channel></rss>'''
    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(lambda r:httpx.Response(200,text=rss))) as c:
            return await refresh_signals(feeds=[RSS_FEED],tagger=KeywordTagger(),client=c)
    summary=asyncio.run(run())
    assert summary['status']=='ok' and summary['pending']==1 and summary['accepted']==0 and summary['rejected']==2
    with storage.connection() as c:
        statuses=sorted(r[0] for r in c.execute('SELECT status FROM feed_items'))
        assert statuses==['pending','rejected','rejected']
        assert c.execute('SELECT accepted FROM refresh_runs').fetchone()[0]==0
    api=TestClient(app)
    assert not any(s['tagged_by']=='keyword' for s in api.get('/api/signals').json())
    assert api.get('/api/what-changed').json()['has_change'] is False
    monkeypatch.setenv('ADMIN_TOKEN','review-test-token')
    headers={'Authorization':'Bearer review-test-token'}
    queued=api.get('/api/signals/review',headers=headers).json()['items']
    assert len(queued)==1
    assert api.post(f"/api/signals/review/{queued[0]['id']}/approve",headers=headers).status_code==200
    stored=api.get('/api/signals').json()
    assert any(s['tagged_by']=='keyword' and 'cybersecurity-analyst' in s['role_ids'] for s in stored)
    changed=api.get('/api/what-changed').json()
    assert changed['has_change'] and changed['new_signal_count']==1
    assert any(m['role_id']=='cybersecurity-analyst' and m['after_trend']>m['before_trend'] for m in changed['moves'])
    again=asyncio.run(run())  # already-seen items are not checked twice
    assert again['checked']==0 and again['accepted']==0

def test_refresh_requires_admin_token_when_set(temp_db,monkeypatch):
    monkeypatch.setenv('ADMIN_TOKEN','secret-for-test')
    assert TestClient(app).post('/api/signals/refresh').status_code==401

def add_run(started,finished,status):
    with storage.connection() as c:
        c.execute('INSERT INTO refresh_runs(started_at,finished_at,status,tagger) VALUES(?,?,?,?)',(started,finished,status,'keyword'))

def test_automatic_refresh_schedule(temp_db,monkeypatch):
    from datetime import datetime,timezone
    from backend.signals import schedule
    now=datetime(2026,10,22,12,0,tzinfo=timezone.utc)
    monkeypatch.setenv('SIGNALS_REFRESH_HOURS','24')
    assert schedule.next_due(now) is None  # GET never activates a schedule
    expected=now+timedelta(hours=24)
    assert schedule.initialize_schedule(now)==expected
    add_run('2026-10-22T02:00:00+00:00','2026-10-22T02:01:00+00:00','ok')
    assert schedule.next_due(now)==expected
    add_run('2026-10-23T02:01:00+00:00','2026-10-23T02:02:00+00:00','failed')
    assert schedule.next_due(now)==expected  # status reads never move the persisted due time
    monkeypatch.setenv('SIGNALS_REFRESH_HOURS','0')
    assert schedule.next_due(now) is None
    outlook=TestClient(app).get('/api/skill-outlook').json()
    assert outlook['updated_at']=='2026-10-22T02:01:00+00:00' and outlook['auto_refresh_hours']==0 and outlook['next_refresh_at'] is None

def test_scheduler_runs_refresh_when_due(temp_db,monkeypatch):
    from backend.signals import schedule
    from datetime import datetime,timezone
    calls=[];current=[datetime(2026,10,22,12,tzinfo=timezone.utc)]
    async def fake_refresh(**kwargs):
        calls.append(kwargs);raise asyncio.CancelledError
    async def no_sleep(seconds):current[0]+=timedelta(seconds=seconds)
    monkeypatch.setattr(schedule,'clock',lambda:current[0])
    monkeypatch.setattr(schedule,'refresh_signals',fake_refresh)
    monkeypatch.setattr(schedule.asyncio,'sleep',no_sleep)
    monkeypatch.setenv('SIGNALS_REFRESH_HOURS','24')
    with pytest.raises(asyncio.CancelledError):asyncio.run(schedule.run_forever())
    assert calls==[{'automatic':True}]
    assert current[0]==datetime(2026,10,23,12,tzinfo=timezone.utc)

def test_skill_trend_cards(temp_db):
    from backend.catalog import load
    curated={s['external_id']:s for s in load('signals.json')}
    for job in load('declining_jobs.json'):  # every declining job is backed only by curated declining reports
        assert job['signal_ids'] and all(curated[i]['direction']=='declining' for i in job['signal_ids'])
    d=TestClient(app).get('/api/skill-trends').json()
    assert d['rising'] and d['declining'] and len(d['months'])==36
    assert all(c['net']>0 and c['kind']=='skill' for c in d['rising'])
    assert all(c['net']<0 for c in d['declining']) and any(c['kind']=='job' for c in d['declining'])
    nets=[c['net'] for c in d['rising']];assert nets==sorted(nets,reverse=True)
    for c in d['rising']+d['declining']:
        assert c['latest']['url'] and c['latest']['date'] and c['signal_count']>=1 and len(c['line'])==36
    data_entry=next(c for c in d['declining'] if c['title']=='Data entry clerks')
    assert 'data entry' in data_entry['latest']['title'].lower()  # leads with the report naming the job
