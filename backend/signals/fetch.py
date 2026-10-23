<<<<<<< HEAD
"""Download configured feeds and turn them into dated feed items (newest first)."""
import hashlib,html,json,re
from datetime import datetime,timedelta,timezone
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree
import httpx

USER_AGENT='FuturePath/0.1 (career navigator demo)'
TIMEOUT=15
MAX_SNIPPET=1500
ATOM='{http://www.w3.org/2005/Atom}'

def short_hash(value):return hashlib.sha1(value.encode()).hexdigest()[:16]

def strip_html(value):
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]*>',' ',value or ''))).strip()

def iso_date(value):
    if not value:return None
    try:dt=parsedate_to_datetime(value)  # RSS: "Tue, 21 Oct 2026 08:00:00 GMT"
    except (TypeError,ValueError):
        try:dt=datetime.fromisoformat(value.replace('Z','+00:00'))  # Atom: ISO 8601
        except ValueError:return None
    return dt.date().isoformat()

def text_of(node,tag):
    found=node.find(tag)
    return (found.text or '').strip() if found is not None else ''

def item(feed,external,title,url,source_name,published,snippet):
    return {'external_id':f"{feed['key']}:{short_hash(external)}",'feed_key':feed['key'],'title':title,'url':url,'source_name':source_name,
            'source_type':feed['source_type'],'published_date':published,'snippet':snippet[:MAX_SNIPPET]}

def parse_feed_xml(xml,feed,today=None):
    """Parses RSS 2.0 or Atom. Keeps items within max_age_days, newest first, at most max_items."""
    root=ElementTree.fromstring(xml)
    items=[]
    for it in root.iter('item'):
        link=text_of(it,'link');title=strip_html(text_of(it,'title'));published=iso_date(text_of(it,'pubDate'))
        source=strip_html(text_of(it,'source')) or feed['name']
        # Google News appends " - Publisher" to titles; the publisher is already in <source>.
        if title.endswith(f' - {source}'):title=title[:-(len(source)+3)]
        if title and link and published:
            items.append(item(feed,text_of(it,'guid') or link,title,link,source,published,strip_html(text_of(it,'description'))))
    for entry in root.iter(ATOM+'entry'):
        links=entry.findall(ATOM+'link')
        alt=next((l for l in links if l.get('rel') in (None,'alternate')),links[0] if links else None)
        link=alt.get('href','') if alt is not None else ''
        title=strip_html(text_of(entry,ATOM+'title'))
        published=iso_date(text_of(entry,ATOM+'published') or text_of(entry,ATOM+'updated'))
        if title and link and published:
            items.append(item(feed,text_of(entry,ATOM+'id') or link,title,link,feed['name'],published,strip_html(text_of(entry,ATOM+'summary'))))
    today=today or datetime.now(timezone.utc).date()
    oldest=(today-timedelta(days=feed['max_age_days'])).isoformat()
    items=[i for i in items if i['published_date']>=oldest]
    return sorted(items,key=lambda i:i['published_date'],reverse=True)[:feed['max_items']]

async def get(client,url):
    resp=await client.get(url,headers={'user-agent':USER_AGENT},timeout=TIMEOUT,follow_redirects=True)
    if resp.status_code>=400:raise RuntimeError(f'HTTP {resp.status_code} from {httpx.URL(url).host}')
    return resp.text

async def fetch_hf_releases(client,feed):
    tree=json.loads(await get(client,f"https://huggingface.co/api/datasets/{feed['dataset']}/tree/main"))
    items=[]
    for entry in tree:
        m=re.fullmatch(r'release_(\d{4})_(\d{2})_(\d{2})',entry.get('path','')) if entry.get('type')=='directory' else None
        if not m:continue
        date=f'{m[1]}-{m[2]}-{m[3]}'
        if date<=feed['covered_until']:continue
        snippet=''
        for doc in ('data_documentation.md','README.md'):  # release notes give the tagger something to read
            try:snippet=await get(client,f"https://huggingface.co/datasets/{feed['dataset']}/raw/main/{entry['path']}/{doc}");break
            except Exception:continue
        items.append({'external_id':f"{feed['key']}:{entry['path']}",'feed_key':feed['key'],
            'title':f'Anthropic Economic Index: new data release ({date})','url':f"https://huggingface.co/datasets/{feed['dataset']}/tree/main/{entry['path']}",
            'source_name':feed['name'],'source_type':feed['source_type'],'published_date':date,'snippet':snippet[:MAX_SNIPPET]})
    return items

async def fetch_feed(client,feed):
    if feed['kind']=='rss':return parse_feed_xml(await get(client,feed['url']),feed)
    return await fetch_hf_releases(client,feed)
=======
"""Download configured feeds and turn them into dated feed items (newest first)."""
import hashlib,html,json,re
from datetime import datetime,timedelta,timezone
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree
import httpx

USER_AGENT='FuturePath/0.1 (career navigator demo)'
TIMEOUT=15
MAX_SNIPPET=1500
ATOM='{http://www.w3.org/2005/Atom}'

def short_hash(value):return hashlib.sha1(value.encode()).hexdigest()[:16]

def strip_html(value):
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]*>',' ',value or ''))).strip()

def iso_date(value):
    if not value:return None
    try:dt=parsedate_to_datetime(value)  # RSS: "Tue, 21 Oct 2026 08:00:00 GMT"
    except (TypeError,ValueError):
        try:dt=datetime.fromisoformat(value.replace('Z','+00:00'))  # Atom: ISO 8601
        except ValueError:return None
    return dt.date().isoformat()

def text_of(node,tag):
    found=node.find(tag)
    return (found.text or '').strip() if found is not None else ''

def item(feed,external,title,url,source_name,published,snippet):
    return {'external_id':f"{feed['key']}:{short_hash(external)}",'feed_key':feed['key'],'title':title,'url':url,'source_name':source_name,
            'source_type':feed['source_type'],'published_date':published,'snippet':snippet[:MAX_SNIPPET]}

def parse_feed_xml(xml,feed,today=None):
    """Parses RSS 2.0 or Atom. Keeps items within max_age_days, newest first, at most max_items."""
    root=ElementTree.fromstring(xml)
    items=[]
    for it in root.iter('item'):
        link=text_of(it,'link');title=strip_html(text_of(it,'title'));published=iso_date(text_of(it,'pubDate'))
        source=strip_html(text_of(it,'source')) or feed['name']
        # Google News appends " - Publisher" to titles; the publisher is already in <source>.
        if title.endswith(f' - {source}'):title=title[:-(len(source)+3)]
        if title and link and published:
            items.append(item(feed,text_of(it,'guid') or link,title,link,source,published,strip_html(text_of(it,'description'))))
    for entry in root.iter(ATOM+'entry'):
        links=entry.findall(ATOM+'link')
        alt=next((l for l in links if l.get('rel') in (None,'alternate')),links[0] if links else None)
        link=alt.get('href','') if alt is not None else ''
        title=strip_html(text_of(entry,ATOM+'title'))
        published=iso_date(text_of(entry,ATOM+'published') or text_of(entry,ATOM+'updated'))
        if title and link and published:
            items.append(item(feed,text_of(entry,ATOM+'id') or link,title,link,feed['name'],published,strip_html(text_of(entry,ATOM+'summary'))))
    today=today or datetime.now(timezone.utc).date()
    oldest=(today-timedelta(days=feed['max_age_days'])).isoformat()
    items=[i for i in items if i['published_date']>=oldest]
    return sorted(items,key=lambda i:i['published_date'],reverse=True)[:feed['max_items']]

async def get(client,url):
    resp=await client.get(url,headers={'user-agent':USER_AGENT},timeout=TIMEOUT,follow_redirects=True)
    if resp.status_code>=400:raise RuntimeError(f'HTTP {resp.status_code} from {httpx.URL(url).host}')
    return resp.text

async def fetch_hf_releases(client,feed):
    tree=json.loads(await get(client,f"https://huggingface.co/api/datasets/{feed['dataset']}/tree/main"))
    items=[]
    for entry in tree:
        m=re.fullmatch(r'release_(\d{4})_(\d{2})_(\d{2})',entry.get('path','')) if entry.get('type')=='directory' else None
        if not m:continue
        date=f'{m[1]}-{m[2]}-{m[3]}'
        if date<=feed['covered_until']:continue
        snippet=''
        for doc in ('data_documentation.md','README.md'):  # release notes give the tagger something to read
            try:snippet=await get(client,f"https://huggingface.co/datasets/{feed['dataset']}/raw/main/{entry['path']}/{doc}");break
            except Exception:continue
        items.append({'external_id':f"{feed['key']}:{entry['path']}",'feed_key':feed['key'],
            'title':f'Anthropic Economic Index: new data release ({date})','url':f"https://huggingface.co/datasets/{feed['dataset']}/tree/main/{entry['path']}",
            'source_name':feed['name'],'source_type':feed['source_type'],'published_date':date,'snippet':snippet[:MAX_SNIPPET]})
    return items

async def fetch_feed(client,feed):
    if feed['kind']=='rss':return parse_feed_xml(await get(client,feed['url']),feed)
    return await fetch_hf_releases(client,feed)
>>>>>>> da0787dab49148d066631b796b12e2b882c85231
