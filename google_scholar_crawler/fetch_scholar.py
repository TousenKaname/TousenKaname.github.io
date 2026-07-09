"""Fetch the Google Scholar author profile and dump it as JSON.

Run as a subprocess by main.py so a blocked/captcha'd Scholar session can
be killed reliably from outside (scholarly swallows in-process timers and
may sit in a selenium captcha wait for many minutes).
"""
import json
import os

from scholarly import scholarly

scholarly.set_timeout(15)
scholarly.set_retries(2)

author = scholarly.search_author_id(os.environ['GOOGLE_SCHOLAR_ID'])
scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])

os.makedirs('results', exist_ok=True)
with open('results/scholar_raw.json', 'w') as outfile:
    json.dump(author, outfile, ensure_ascii=False, default=str)
print(f"Scholar profile fetched: {author.get('name')}, "
      f"{author.get('citedby')} citations, "
      f"{len(author['publications'])} publications", flush=True)
