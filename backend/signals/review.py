"""Transactional administrative decisions; pending evidence never enters signals."""
import json
from datetime import datetime, timezone

from fastapi import HTTPException
from ..catalog import ROLES, SKILLS
from ..demo_security import public_demo
from ..storage import connection, insert_signal
from .guardrails import apply_guardrails, source_error


def timestamp():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def review_items(status='pending', limit=200):
    if status not in ('pending', 'approved', 'rejected', 'all'):
        raise HTTPException(400, 'Unknown review status')
    clause, args = ('', ()) if status == 'all' else (' WHERE status=?', (status,))
    with connection() as c:
        total = c.execute('SELECT COUNT(*) FROM signal_review' + clause, args).fetchone()[0]
        rows = c.execute('SELECT * FROM signal_review' + clause +
                         ' ORDER BY id DESC LIMIT ?', (*args, max(1, min(limit, 200)))).fetchall()
    return {'total': total, 'items': [
        {**{k: r[k] for k in ('id', 'status', 'created_at', 'reviewed_at',
                              'decision_reason', 'signal_id')},
         'signal': json.loads(r['signal']), 'validation_notes': r['validation_notes']}
        for r in rows]}


def decide(review_id, action, reason=''):
    if public_demo():
        raise HTTPException(403, 'Evidence review is disabled in public demo mode')
    if action not in ('approved', 'rejected'):
        raise HTTPException(400, 'Unknown decision')
    with connection() as c:
        c.execute('BEGIN IMMEDIATE')
        row = c.execute('SELECT * FROM signal_review WHERE id=?', (review_id,)).fetchone()
        if row is None:
            raise HTTPException(404, 'Review item not found')
        if row['status'] != 'pending':
            raise HTTPException(409, 'This evidence has already been reviewed')
        signal = json.loads(row['signal'])
        signal_id = None
        if action == 'approved':
            # Revalidate persisted evidence at approval, not just at ingestion.
            item = json.loads(row['source_item'])
            error = source_error(item)
            if any(signal.get(key) != item.get(key) for key in
                   ('external_id','feed_key','title','url','source_name','source_type','published_date')):
                error = 'Stored source provenance changed'
            proposal, _ = apply_guardrails(
                item, {**signal, 'relevant': True},
                {r['id'] for r in ROLES}, {s['id'] for s in SKILLS})
            if error or proposal is None:
                raise HTTPException(409, 'Stored evidence no longer passes validation')
            signal.update({k: proposal[k] for k in
                           ('role_ids', 'skill_ids', 'summary', 'strength', 'direction')})
            signal_id = insert_signal(c, signal)
            if signal_id is None:
                raise HTTPException(409, 'This evidence is already active')
        at = timestamp()
        c.execute('UPDATE signal_review SET status=?,reviewed_at=?,decision_reason=?,signal_id=? WHERE id=?',
                  (action, at, reason, signal_id, review_id))
        c.execute('INSERT INTO signal_review_events(review_id,action,created_at,actor,reason) VALUES(?,?,?,?,?)',
                  (review_id, action, at, 'administrator', reason))
        c.execute('UPDATE feed_items SET status=?,signal_id=?,reason=? WHERE external_id=?',
                  (action, signal_id, reason or 'Administrator ' + action, row['external_id']))
        column = 'accepted' if action == 'approved' else 'rejected'
        c.execute(f'UPDATE refresh_runs SET pending=MAX(0,pending-1),{column}={column}+1 WHERE id=?',
                  (row['run_id'],))
    return {'id': review_id, 'status': action, 'signal_id': signal_id}
