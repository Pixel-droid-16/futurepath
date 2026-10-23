"""Configured trend-signal sources pulled by "Refresh signals". Add or remove feeds here."""
from urllib.parse import quote

def google_news(query):
    return 'https://news.google.com/rss/search?q='+quote(f'{query} when:30d')+'&hl=en-MY&gl=MY&ceid=MY:en'

FEEDS=[
    {'kind':'rss','key':'gnews-my-ai-jobs','name':'Google News: AI and jobs in Malaysia','source_type':'news','max_items':15,'max_age_days':45,
     'url':google_news('(AI OR "artificial intelligence") (jobs OR workers OR reskilling OR upskilling) Malaysia')},
    {'kind':'rss','key':'gnews-my-green-jobs','name':'Google News: green jobs in Malaysia','source_type':'news','max_items':10,'max_age_days':45,
     'url':google_news('Malaysia ("green jobs" OR "renewable energy" OR solar OR "energy transition") (jobs OR skills OR talent)')},
    {'kind':'rss','key':'gnews-my-digital-talent','name':'Google News: digital and data talent in Malaysia','source_type':'news','max_items':10,'max_age_days':45,
     'url':google_news('Malaysia (cybersecurity OR "data analytics" OR "digital talent" OR fintech) (jobs OR skills OR shortage)')},
    {'kind':'rss','key':'gnews-my-talent-policy','name':'Google News: Malaysian talent and skills policy','source_type':'news','max_items':8,'max_age_days':45,
     'url':google_news('Malaysia (TalentCorp OR MyMahir OR "HRD Corp" OR TVET) (skills OR reskilling OR "critical occupations")')},
    {'kind':'rss','key':'arxiv-genai-labour','name':'arXiv: generative AI and labour markets','source_type':'research','max_items':6,'max_age_days':120,
     'url':'https://export.arxiv.org/api/query?search_query=abs:%22labor+market%22+AND+abs:%22generative+AI%22&sortBy=submittedDate&sortOrder=descending&max_results=10'},
    # New release_YYYY_MM_DD folders become candidate signals; earlier releases are covered by curated signals.
    {'kind':'hf-releases','key':'hf-anthropic-economic-index','name':'Anthropic Economic Index (Hugging Face dataset)','source_type':'dataset',
     'dataset':'Anthropic/EconomicIndex','covered_until':'2025-09-15'},
]
