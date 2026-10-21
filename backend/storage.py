"""SQLite demo storage; one place to manage profiles, evidence and history."""
from pathlib import Path
import sqlite3, os, json
from fastapi import HTTPException
from .catalog import ROOT, load
DB=Path(os.getenv('FUTUREPATH_DB',str(ROOT/'futurepath_demo.sqlite3')))
def connection():
    c=sqlite3.connect(str(DB));c.row_factory=sqlite3.Row
    return c

def init():
    DB.parent.mkdir(parents=True,exist_ok=True)
    with connection() as c:
        c.executescript('''CREATE TABLE IF NOT EXISTS profiles(id TEXT PRIMARY KEY, payload TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS snapshots(id TEXT PRIMARY KEY, status TEXT NOT NULL,payload TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS history(id INTEGER PRIMARY KEY AUTOINCREMENT,profile_id TEXT NOT NULL,created_at TEXT NOT NULL,payload TEXT NOT NULL);
        -- Trend signals: curated reports (data/signals.json) plus items accepted by a feed refresh.
        CREATE TABLE IF NOT EXISTS signals(id INTEGER PRIMARY KEY AUTOINCREMENT,external_id TEXT UNIQUE NOT NULL,title TEXT NOT NULL,
            source_name TEXT NOT NULL,source_type TEXT NOT NULL,url TEXT NOT NULL,published_date TEXT NOT NULL,fetched_at TEXT NOT NULL,
            summary TEXT NOT NULL,direction TEXT NOT NULL,strength INTEGER NOT NULL,role_ids TEXT NOT NULL,skill_ids TEXT NOT NULL,
            tagged_by TEXT NOT NULL,feed_key TEXT,run_id INTEGER);
        -- Audit trail: every feed item checked (accepted, rejected or failed, with the reason) and every refresh run.
        CREATE TABLE IF NOT EXISTS feed_items(external_id TEXT PRIMARY KEY,feed_key TEXT NOT NULL,title TEXT NOT NULL,url TEXT NOT NULL,
            published_date TEXT NOT NULL,run_id INTEGER NOT NULL,status TEXT NOT NULL,reason TEXT NOT NULL,signal_id INTEGER,seen_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS refresh_runs(id INTEGER PRIMARY KEY AUTOINCREMENT,started_at TEXT NOT NULL,finished_at TEXT,status TEXT NOT NULL,
            tagger TEXT NOT NULL,model TEXT,feeds TEXT NOT NULL DEFAULT '[]',checked INTEGER NOT NULL DEFAULT 0,accepted INTEGER NOT NULL DEFAULT 0,
            rejected INTEGER NOT NULL DEFAULT 0,failed INTEGER NOT NULL DEFAULT 0,error TEXT);''')
        if not c.execute('SELECT 1 FROM profiles WHERE id=?',('demo',)).fetchone():
            c.execute('INSERT INTO profiles VALUES (?,?)',('demo',json.dumps(load('demo_profile.json'))))
        for s in load('snapshots.json'):
            if not c.execute('SELECT 1 FROM snapshots WHERE id=?',(s['id'],)).fetchone():
                c.execute('INSERT INTO snapshots VALUES(?,?,?)',(s['id'],s['status'],json.dumps(s)))
        # data/signals.json is the source of truth for curated signals: re-sync their links and text on start.
        for s in load('signals.json'):
            if insert_signal(c,s) is None:
                c.execute("UPDATE signals SET title=?,source_name=?,url=?,published_date=?,summary=?,direction=?,strength=?,role_ids=?,skill_ids=? WHERE external_id=? AND tagged_by='curated'",
                          (s['title'],s['source_name'],s['url'],s['published_date'],s['summary'],s['direction'],s['strength'],json.dumps(s['role_ids']),json.dumps(s['skill_ids']),s['external_id']))

SIGNAL_FIELDS=('external_id','title','source_name','source_type','url','published_date','fetched_at','summary','direction',
               'strength','role_ids','skill_ids','tagged_by','feed_key','run_id')
def insert_signal(c,s):
    """Adds a signal unless its external_id is already stored. Returns the new row id, or None."""
    if c.execute('SELECT 1 FROM signals WHERE external_id=?',(s['external_id'],)).fetchone():return None
    row={**s,'role_ids':json.dumps(s['role_ids']),'skill_ids':json.dumps(s['skill_ids']),'run_id':s.get('run_id')}
    cur=c.execute(f"INSERT INTO signals({','.join(SIGNAL_FIELDS)}) VALUES({','.join('?'*len(SIGNAL_FIELDS))})",[row.get(k) for k in SIGNAL_FIELDS])
    return cur.lastrowid

def get_signals():
    with connection() as c:
        rows=c.execute('SELECT * FROM signals ORDER BY published_date DESC,id DESC').fetchall()
    return [{**dict(r),'role_ids':json.loads(r['role_ids']),'skill_ids':json.loads(r['skill_ids'])} for r in rows]

def get_profile(pid='demo'):
    """One saved person. 'demo' is the original shared profile; others are created by the Start flow."""
    with connection() as c:
        row=c.execute('SELECT payload FROM profiles WHERE id=?',(pid,)).fetchone()
    if not row:raise HTTPException(404,'Profile not found')
    return json.loads(row['payload'])

def save_profile(pid,payload):
    with connection() as c:
        c.execute('INSERT INTO profiles(id,payload) VALUES(?,?) ON CONFLICT(id) DO UPDATE SET payload=excluded.payload',(pid,json.dumps(payload)))

def delete_profile(pid):
    """Removes a saved person. The shared 'demo' profile is reset to data/demo_profile.json instead (it has no name, so it leaves the list)."""
    with connection() as c:
        if not c.execute('SELECT 1 FROM profiles WHERE id=?',(pid,)).fetchone():raise HTTPException(404,'Profile not found')
        if pid=='demo':c.execute('UPDATE profiles SET payload=? WHERE id=?',(json.dumps(load('demo_profile.json')),'demo'))
        else:c.execute('DELETE FROM profiles WHERE id=?',(pid,))

def list_profiles():
    """Saved people (profiles with a name), most recently updated first."""
    with connection() as c:
        rows=[json.loads(r['payload']) for r in c.execute('SELECT payload FROM profiles').fetchall()]
    return sorted((p for p in rows if p.get('name')),key=lambda p:p.get('updated_at',''),reverse=True)

def get_snapshot(sid=None):
    with connection() as c:
        row=(c.execute('SELECT * FROM snapshots WHERE id=?',(sid,)).fetchone() if sid else
             c.execute("SELECT * FROM snapshots WHERE status='published' ORDER BY id DESC LIMIT 1").fetchone())
    if not row:raise HTTPException(404,'Snapshot not found')
    return json.loads(row['payload'])
