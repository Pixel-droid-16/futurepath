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
from backend.signals.refresh import refresh_signals, automatic_ai_allowed
from backend.signals.snapshot import validate_document, validate_signal

OUT = Path(__file__).resolve().parents[1] / 'data' / 'live_signals.json'

def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')

def previous_document():
    data=json.loads(OUT.read_text(encoding='utf-8'))
    validate_document(data)
    return data

async def main():
    if os.getenv('FUTUREPATH_PUBLIC_DEMO','').strip().lower() in ('1','yes','true'):
        raise RuntimeError('Public demo mode cannot run the evidence worker')
    previous=previous_document()
    with tempfile.TemporaryDirectory(prefix='futurepath-external-') as temp:
        storage.DB=Path(temp)/'evidence.sqlite3'
        storage.init()
        with storage.connection() as con:
            for row in previous['signals']:
                safe=validate_signal(row)
                if safe:
                    storage.insert_signal(con,safe)
        report=await refresh_signals(automatic=True)
        if report['status'] not in ('ok','partial'):
            raise RuntimeError('Source checks failed; previous snapshot preserved')
        signals=[]
        for row in storage.get_signals():
            if row['tagged_by'] == 'claude' and row.get('feed_key'):
                safe=validate_signal(row)
                if safe:
                    signals.append(safe)
    snapshot={'schema_version':1,'checked_at':utc_now(),
              'last_successful_at':utc_now(),'status':report['status'],
              'ai_enabled':automatic_ai_allowed(),'signals':signals[:200]}
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
