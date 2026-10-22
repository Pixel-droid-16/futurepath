"""Trend signal layer, ported from LaluanKu: curated reports plus refreshable news, research and dataset feeds.

feeds.py      which sources a refresh pulls
fetch.py      download and parse RSS/Atom feeds and Hugging Face dataset releases
tagging.py    Claude tagger, with a deterministic keyword tagger as the fallback
guardrails.py "never invent" rules applied to every tagger proposal
refresh.py    the refresh pipeline and its audit trail
demand.py     signal-driven demand (the Trends score) for each career
"""
