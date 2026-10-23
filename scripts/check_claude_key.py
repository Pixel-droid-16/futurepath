"""Check whether the Claude API key works.

Reads ANTHROPIC_API_KEY (and optional ANTHROPIC_MODEL) from the environment, falling back to the project's .env.
Step 1 lists models (free, proves the key is accepted); step 2 sends a tiny message to the configured model
(proves the account can actually use it). Exit code 0 means the key works.

    python scripts/check_claude_key.py
"""
from pathlib import Path
import os,sys
try:import anthropic
except ImportError:sys.exit('FAIL  the anthropic package is not installed for this Python ('+sys.executable+')\n'
    '      use the project venv:  .venv\\Scripts\\python scripts\\check_claude_key.py\n'
    '      or install it here:    python -m pip install -r requirements.txt')
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from backend.providers.claude import DEFAULT_MODEL

def load_env():
    env=ROOT/'.env'
    if not env.exists():return
    for line in env.read_text(encoding='utf8').splitlines():
        name,sep,value=line.strip().partition('=')
        if sep and not name.startswith('#') and value.strip():os.environ.setdefault(name.strip(),value.strip().strip('"\''))

def mask(key):return key[:10]+'...'+key[-4:] if len(key)>16 else '(too short to be a real key)'

def check():
    load_env()
    key=os.getenv('ANTHROPIC_API_KEY','')
    if not key:print('FAIL  ANTHROPIC_API_KEY is not set (environment or .env)');return 1
    name=os.getenv('ANTHROPIC_MODEL') or DEFAULT_MODEL
    print(f'Key   {mask(key)}\nModel {name}')
    client=anthropic.Anthropic(api_key=key,max_retries=0,timeout=60)
    try:
        client.models.list(limit=1)
        print('OK    key accepted')
        reply=client.messages.create(model=name,max_tokens=256,output_config={'effort':'low'},
            messages=[{'role':'user','content':'Reply with the single word: pong'}])
        text=''.join(b.text for b in reply.content if b.type=='text').strip()
        print(f'OK    {name} replied ({reply.usage.input_tokens} in / {reply.usage.output_tokens} out tokens): {text or "(no text, stop_reason="+reply.stop_reason+")"}')
        print('PASS  the key works');return 0
    except anthropic.AuthenticationError:print('FAIL  key rejected (401): invalid, revoked or mistyped')
    except anthropic.PermissionDeniedError as e:print(f'FAIL  key lacks permission (403): {e.message}')
    except anthropic.NotFoundError:print(f'FAIL  model {name} not found or not available to this account (404)')
    except anthropic.RateLimitError:print('FAIL  rate limited (429): the key is valid but over its limit right now')
    except anthropic.BadRequestError as e:print(f'FAIL  bad request (400): {e.message}')
    except anthropic.APIStatusError as e:print(f'FAIL  HTTP {e.status_code}: {e.message}')
    except anthropic.APIConnectionError:print('FAIL  could not reach api.anthropic.com (network, proxy or firewall)')
    return 1

if __name__=='__main__':sys.exit(check())
