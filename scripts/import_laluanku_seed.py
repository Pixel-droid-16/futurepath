"""Import LaluanKu's curated trend signals and checked courses into FuturePath's catalogue.

Run: python scripts/import_laluanku_seed.py C:/path/to/laluanku
Writes data/signals.json and data/courses.json. LaluanKu (same team, Apache-2.0) uses its own
role and skill slugs; the tables below map them to FuturePath IDs. Only clear equivalents are
mapped: a link to a career or skill FuturePath does not have is dropped, never guessed.
"""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parent.parent
# Curated signals were checked on this date (LaluanKu seed/README.md).
CURATED_FETCHED_AT='2026-10-20'

ROLE_MAP={
    'data-analyst':'data-analyst','bi-analyst':'bi-analyst','information-security-analyst':'cybersecurity-analyst',
    'ux-ui-designer':'ux-designer','renewable-energy-engineer':'renewable-engineer','sustainability-specialist':'sustainability-analyst',
}
SKILL_MAP={
    # same skill, same or near-identical name
    'sql':'SK001','statistics':'SK002','data-visualisation':'SK004','python-programming':'SK005','communication':'SK007',
    'network-security':'SK010','risk-assessment':'SK016','spreadsheets':'SK020','data-warehousing':'SK025',
    'esg-reporting':'SK043','carbon-accounting':'SK045','ux-research':'SK071','project-management':'SK078',
    # same skill, different name (team judgement)
    'bi-dashboards':'SK027','data-engineering':'SK026','cybersecurity':'SK011','data-protection':'SK034',
    'generative-ai-use':'SK077','prompt-writing':'SK077','stakeholder-management':'SK024',
    'bookkeeping':'SK019','electrical-systems':'SK049','solar-pv-systems':'SK048','energy-efficiency':'SK048',
    'environmental-regulations':'SK046','health-records':'SK030','graphic-design-tools':'SK076',
    'quality-control':'SK059','workplace-safety':'SK053','electronics-troubleshooting':'SK058',
    # transferable skills added to FuturePath's catalogue
    'leadership':'SK079','problem-solving':'SK082',
}

def unique(values):return list(dict.fromkeys(v for v in values if v))

def main(laluanku):
    seed=Path(laluanku)/'seed'
    signals=json.loads((seed/'signals.json').read_text(encoding='utf8'))
    courses=json.loads((seed/'courses.json').read_text(encoding='utf8'))
    out_signals=[{
        'external_id':'curated:'+s['external_id'],'title':s['title'],'source_name':s['source_name'],
        'source_type':s['source_type'],'url':s['url'],'published_date':s['published_date'],'fetched_at':CURATED_FETCHED_AT,
        'summary':s['summary'],'direction':s['direction'],'strength':s['strength'],
        'role_ids':unique(ROLE_MAP.get(r) for r in s.get('roles',[])),
        'skill_ids':unique(SKILL_MAP.get(k) for k in s.get('skills',[])),
        'tagged_by':'curated','feed_key':None} for s in signals]
    out_courses=[]
    for c in courses:
        skill_ids=unique(SKILL_MAP.get(k) for k in c.get('skills',[]))
        if not skill_ids:continue  # a course that teaches nothing in our catalogue can't appear in a pathway
        out_courses.append({'id':c['slug'],'title':c['title'],'provider':c['provider'],'url':c['url'],'cost':c['cost'],
            'hours':c['hours'],'hours_estimated':c.get('hours_estimated',False),'language':c.get('language','en'),
            'skill_ids':skill_ids,'notes':c.get('notes','')})
    for name,rows in (('signals.json',out_signals),('courses.json',out_courses)):
        (ROOT/'data'/name).write_text(json.dumps(rows,ensure_ascii=False,indent=1)+'\n',encoding='utf8')
    linked=sum(1 for s in out_signals if s['role_ids'] or s['skill_ids'])
    print(f'signals: {len(out_signals)} ({linked} linked to FuturePath careers/skills); courses: {len(out_courses)} of {len(courses)}')

if __name__=='__main__':
    if len(sys.argv)!=2:sys.exit('usage: python scripts/import_laluanku_seed.py <path to laluanku>')
    main(sys.argv[1])
