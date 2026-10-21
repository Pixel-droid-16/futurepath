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
        CREATE TABLE IF NOT EXISTS history(id INTEGER PRIMARY KEY AUTOINCREMENT,profile_id TEXT NOT NULL,created_at TEXT NOT NULL,payload TEXT NOT NULL);''')
        if not c.execute('SELECT 1 FROM profiles WHERE id=?',('demo',)).fetchone():
            c.execute('INSERT INTO profiles VALUES (?,?)',('demo',json.dumps(load('demo_profile.json'))))
        for s in load('snapshots.json'):
            if not c.execute('SELECT 1 FROM snapshots WHERE id=?',(s['id'],)).fetchone():
                c.execute('INSERT INTO snapshots VALUES(?,?,?)',(s['id'],s['status'],json.dumps(s)))

def get_profile():
    with connection() as c:
        return json.loads(c.execute('SELECT payload FROM profiles WHERE id=?',('demo',)).fetchone()['payload'])

def get_snapshot(sid=None):
    with connection() as c:
        row=(c.execute('SELECT * FROM snapshots WHERE id=?',(sid,)).fetchone() if sid else
             c.execute("SELECT * FROM snapshots WHERE status='published' ORDER BY id DESC LIMIT 1").fetchone())
    if not row:raise HTTPException(404,'Snapshot not found')
    return json.loads(row['payload'])
