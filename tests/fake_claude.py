"""A stand-in for anthropic.AsyncAnthropic: records each request and returns a canned JSON reply."""
import json
from types import SimpleNamespace

class FakeClaude:
    def __init__(self,reply,stop_reason='end_turn'):
        self.reply,self.stop_reason,self.requests=reply,stop_reason,[]
        self.beta=SimpleNamespace(messages=SimpleNamespace(create=self.create))
    async def create(self,**params):
        self.requests.append(params)
        text=self.reply if isinstance(self.reply,str) else json.dumps(self.reply)
        return SimpleNamespace(stop_reason=self.stop_reason,content=[SimpleNamespace(type='thinking',thinking=''),SimpleNamespace(type='text',text=text)])
    async def close(self):pass
