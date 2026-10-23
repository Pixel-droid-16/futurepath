<<<<<<< HEAD
"""Automatic signal refresh while the server runs: once every SIGNALS_REFRESH_HOURS (default 24; 0 turns it off).

The next run is due a full interval after the last run that finished (ok or partial). A failed run is retried after
RETRY_MINUTES so a feed outage does not cause a tight loop. The manual Refresh button still works at any time.
"""
import asyncio,logging,os
from datetime import datetime,timedelta,timezone
from ..storage import connection
from .refresh import refresh_signals,RefreshInProgress

log=logging.getLogger('futurepath.signals')
DEFAULT_HOURS=24
RETRY_MINUTES=60
STARTUP_DELAY_SECONDS=60  # let the server finish starting before the first fetch

def interval_hours():
    try:return max(0.0,float(os.getenv('SIGNALS_REFRESH_HOURS',DEFAULT_HOURS)))
    except ValueError:return float(DEFAULT_HOURS)

def parse(ts):return datetime.fromisoformat(ts) if ts else None

def last_runs():
    """(finished_at of the last ok/partial run, finished_at of the last run of any outcome)."""
    with connection() as c:
        done=c.execute("SELECT finished_at FROM refresh_runs WHERE status IN ('ok','partial') AND finished_at IS NOT NULL ORDER BY id DESC LIMIT 1").fetchone()
        any_=c.execute("SELECT finished_at FROM refresh_runs WHERE status!='running' AND finished_at IS NOT NULL ORDER BY id DESC LIMIT 1").fetchone()
    return parse(done[0] if done else None),parse(any_[0] if any_ else None)

def next_due(now=None,hours=None):
    """When the next automatic refresh should start, or None when it is turned off."""
    hours=interval_hours() if hours is None else hours
    if not hours:return None
    now=now or datetime.now(timezone.utc)
    success,attempt=last_runs()
    due=success+timedelta(hours=hours) if success else now
    if attempt and attempt!=success:due=max(due,attempt+timedelta(minutes=RETRY_MINUTES))
    return due

async def run_forever():
    await asyncio.sleep(STARTUP_DELAY_SECONDS)
    while True:
        due=next_due()
        if due is None:return
        wait=(due-datetime.now(timezone.utc)).total_seconds()
        if wait>0:
            await asyncio.sleep(min(wait,3600))  # re-check hourly, in case a manual refresh moved the schedule
            continue
        try:
            out=await refresh_signals()
            log.info('Automatic signal refresh %s: %s accepted, %s rejected',out['status'],out['accepted'],out['rejected'])
        except RefreshInProgress:
            await asyncio.sleep(300)
        except Exception:
            log.exception('Automatic signal refresh failed')  # recorded in refresh_runs; retried after RETRY_MINUTES
=======
"""Automatic signal refresh while the server runs: once every SIGNALS_REFRESH_HOURS (default 24; 0 turns it off).

The next run is due a full interval after the last run that finished (ok or partial). A failed run is retried after
RETRY_MINUTES so a feed outage does not cause a tight loop. The manual Refresh button still works at any time.
"""
import asyncio,logging,os
from datetime import datetime,timedelta,timezone
from ..storage import connection
from .refresh import refresh_signals,RefreshInProgress

log=logging.getLogger('futurepath.signals')
DEFAULT_HOURS=24
RETRY_MINUTES=60
STARTUP_DELAY_SECONDS=60  # let the server finish starting before the first fetch

def interval_hours():
    try:return max(0.0,float(os.getenv('SIGNALS_REFRESH_HOURS',DEFAULT_HOURS)))
    except ValueError:return float(DEFAULT_HOURS)

def parse(ts):return datetime.fromisoformat(ts) if ts else None

def last_runs():
    """(finished_at of the last ok/partial run, finished_at of the last run of any outcome)."""
    with connection() as c:
        done=c.execute("SELECT finished_at FROM refresh_runs WHERE status IN ('ok','partial') AND finished_at IS NOT NULL ORDER BY id DESC LIMIT 1").fetchone()
        any_=c.execute("SELECT finished_at FROM refresh_runs WHERE status!='running' AND finished_at IS NOT NULL ORDER BY id DESC LIMIT 1").fetchone()
    return parse(done[0] if done else None),parse(any_[0] if any_ else None)

def next_due(now=None,hours=None):
    """When the next automatic refresh should start, or None when it is turned off."""
    hours=interval_hours() if hours is None else hours
    if not hours:return None
    now=now or datetime.now(timezone.utc)
    success,attempt=last_runs()
    due=success+timedelta(hours=hours) if success else now
    if attempt and attempt!=success:due=max(due,attempt+timedelta(minutes=RETRY_MINUTES))
    return due

async def run_forever():
    await asyncio.sleep(STARTUP_DELAY_SECONDS)
    while True:
        due=next_due()
        if due is None:return
        wait=(due-datetime.now(timezone.utc)).total_seconds()
        if wait>0:
            await asyncio.sleep(min(wait,3600))  # re-check hourly, in case a manual refresh moved the schedule
            continue
        try:
            out=await refresh_signals()
            log.info('Automatic signal refresh %s: %s accepted, %s rejected',out['status'],out['accepted'],out['rejected'])
        except RefreshInProgress:
            await asyncio.sleep(300)
        except Exception:
            log.exception('Automatic signal refresh failed')  # recorded in refresh_runs; retried after RETRY_MINUTES
>>>>>>> da0787dab49148d066631b796b12e2b882c85231
