"""External daily evidence worker; cannot publish keyword-only candidates.

Runs in GitHub Actions on an ephemeral DB, seeds prior verified signals for
deduplication, exports only validated model-approved rows to durable git JSON.
"""
import asyncio
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from backend import storage
from backend.providers.claude import configured
from backend.signals import verification
from backend.signals.refresh import refresh_signals
from backend.signals.snapshot import validate_document, validate_signal

OUT = Path(__file__).resolve().parents[1] / 'data' / 'live_signals.json'
VERIFIED = ('claude', 'claude-verified')  # snapshot rows, and rows this run's AI verification published

def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')

def previous_document():
    data=json.loads(OUT.read_text(encoding='utf-8'))
    validate_document(data)
    return data

def last_ai_day(previous):
    """UTC day of the last paid verification run, from the committed snapshot."""
    if previous.get('last_ai_check_day'):
        return previous['last_ai_check_day']
    return (previous.get('checked_at') or '')[:10] if previous.get('ai_enabled') else None

def enable_verification(previous):
    """Opt this run into paid AI verification: needs the Actions variable and key, at most once per UTC day.

    Each run starts with a fresh database, so the daily budget the verifier keeps in SQLite would reset
    on every manual re-run. The committed snapshot records the day of the last paid run instead, which
    makes it the durable, single-writer budget record the verifier asks the operator to confirm.
    """
    requested=os.getenv('SIGNALS_AUTO_AI_ENABLED','').strip().lower() in ('1','true','yes')
    if not requested or not os.getenv('ANTHROPIC_API_KEY','').strip():
        return False
    if last_ai_day(previous)==verification.utc_day():
        return False
    os.environ['SIGNALS_PAID_AI_ENABLED']='1'
    os.environ.setdefault('SIGNALS_AI_DAILY_ITEMS',str(verification.MAX_DAILY_ITEMS))
    os.environ.setdefault('SIGNALS_AI_DAILY_CALLS',str(verification.MAX_DAILY_CALLS))
    os.environ['SIGNALS_AI_DURABLE_STORAGE_CONFIRMED']='1'
    return True

def exported(rows):
    signals=[]
    for row in rows:
        if row['tagged_by'] in VERIFIED and row.get('feed_key'):
            safe=validate_signal({**row,'tagged_by':'claude'})
            if safe:
                signals.append(safe)
    return signals

async def main():
    if os.getenv('FUTUREPATH_PUBLIC_DEMO','').strip().lower() in ('1','yes','true'):
        raise RuntimeError('Public demo mode cannot run the evidence worker')
    os.environ['SIGNALS_REMOTE_SNAPSHOT_ENABLED']='0'  # this worker writes the snapshot; never read it back
    previous=previous_document()
    requested=enable_verification(previous)
    # RUNNER_TEMP is outside /tmp, which the verifier treats as unconfirmed storage.
    with tempfile.TemporaryDirectory(prefix='futurepath-external-',dir=os.getenv('RUNNER_TEMP') or None,
                                     ignore_cleanup_errors=True) as temp:
        storage.DB=Path(temp)/'evidence.sqlite3'
        storage.init()
        ai_enabled=requested and verification.paid_enabled() and configured()
        with storage.connection() as con:
            for row in previous['signals']:
                safe=validate_signal(row)
                if safe:
                    storage.insert_signal(con,safe)
        report=await refresh_signals(automatic=True)
        if report['status'] not in ('ok','partial'):
            raise RuntimeError('Source checks failed; previous snapshot preserved')
        signals=exported(storage.get_signals())
    snapshot={'schema_version':1,'checked_at':utc_now(),
              'last_successful_at':utc_now(),'status':report['status'],
              'ai_enabled':ai_enabled,
              'last_ai_check_day':verification.utc_day() if ai_enabled else last_ai_day(previous),
              'signals':signals[:200]}
    validate_document(snapshot)
    tmp=OUT.with_suffix('.json.tmp')
    tmp.write_text(json.dumps(snapshot,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    tmp.replace(OUT)
    print('External check:',report['status'],
          'AI enabled:',snapshot['ai_enabled'],
          'approved publications:',len(signals),
          'pending:',report['pending'],'rejected:',report['rejected'])

if __name__=='__main__':
    asyncio.run(main())
