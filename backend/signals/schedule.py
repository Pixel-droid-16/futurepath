"""Best-effort daily source checks while this server remains running.

State survives process restarts in the configured SQLite DB, not DB loss.
First activation and overdue restarts defer a full interval; no catch-up fetch.
Public demo always disables this task, independently of environment settings.
"""
import asyncio
import logging
import math
import os
from datetime import datetime, timedelta, timezone

from ..demo_security import public_demo
from ..storage import connection
from .refresh import refresh_signals, RefreshInProgress

log = logging.getLogger('futurepath.signals')
DEFAULT_HOURS = 0
STARTUP_DELAY_SECONDS = 60


def clock():
    return datetime.now(timezone.utc)


def interval_hours():
    if public_demo():
        return 0.0
    try:
        hours = float(os.getenv('SIGNALS_REFRESH_HOURS', DEFAULT_HOURS))
        return hours if math.isfinite(hours) and hours > 0 else 0.0
    except ValueError:
        return 0.0


def parse(ts):
    return datetime.fromisoformat(ts) if ts else None


def last_runs():
    with connection() as c:
        done = c.execute("SELECT finished_at FROM refresh_runs WHERE status IN ('ok','partial') "
                         "AND finished_at IS NOT NULL ORDER BY id DESC LIMIT 1").fetchone()
        attempt = c.execute("SELECT finished_at FROM refresh_runs WHERE status!='running' "
                            "AND finished_at IS NOT NULL ORDER BY id DESC LIMIT 1").fetchone()
    return parse(done[0] if done else None), parse(attempt[0] if attempt else None)


def initialize_schedule(now=None):
    """Called on startup; preserve future due times, defer overdue/missing ones."""
    now = now or clock()
    hours = interval_hours()
    with connection() as c:
        c.execute('BEGIN IMMEDIATE')
        row = c.execute('SELECT * FROM signal_schedule WHERE id=1').fetchone()
        old_due = parse(row['next_due']) if row else None
        keep = bool(hours and row and row['interval_hours'] == hours
                    and old_due and old_due > now)
        due = old_due if keep else (now + timedelta(hours=hours) if hours else None)
        activated = row['activated_at'] if keep else now.isoformat()
        c.execute('INSERT INTO signal_schedule(id,interval_hours,activated_at,next_due) VALUES(1,?,?,?) '
                  'ON CONFLICT(id) DO UPDATE SET interval_hours=excluded.interval_hours,'
                  'activated_at=excluded.activated_at,next_due=excluded.next_due',
                  (hours, activated, due.isoformat() if due else None))
    return due


def next_due(now=None, hours=None):
    """Read-only: permission/status GET requests must never activate a schedule."""
    effective = interval_hours()
    if not effective or hours == 0:
        return None
    with connection() as c:
        row = c.execute('SELECT next_due FROM signal_schedule WHERE id=1').fetchone()
    return parse(row[0]) if row else None


def record_check():
    hours = interval_hours()
    if hours:
        with connection() as c:
            c.execute('UPDATE signal_schedule SET next_due=? WHERE id=1',
                      ((clock() + timedelta(hours=hours)).isoformat(),))


async def run_forever():
    # Also initialize for standalone callers; this does not shift a future due time.
    initialize_schedule()
    await asyncio.sleep(STARTUP_DELAY_SECONDS)
    while interval_hours():
        due = next_due()
        if due is None:
            return
        wait = (due - clock()).total_seconds()
        if wait > 0:
            await asyncio.sleep(min(wait, 3600))
            continue
        try:
            out = await refresh_signals(automatic=True)
            log.info('Automatic source check %s: %s quarantined, %s AI-validated published',
                     out['status'], out['pending'], out['accepted'])
        except RefreshInProgress:
            await asyncio.sleep(300)
        except Exception:
            # No raw provider/feed response or secret-bearing exception logs.
            log.error('Automatic source check failed; next daily interval will retry')
            record_check()
