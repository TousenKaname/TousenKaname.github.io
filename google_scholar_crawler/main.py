"""Fetch Google Scholar stats for the homepage.

Runs daily (and on pushes to main) via
.github/workflows/google_scholar_crawler.yaml and force-pushes two JSON
files to the `google-scholar-stats` branch:

- gs_data.json           full author profile; `publications` is keyed by
                         author_pub_id and consumed by the homepage JS
                         (per-paper citation counts + auto-generated
                         "Full Publication List" section)
- gs_data_shieldsio.json shields.io endpoint payload for the total-citations
                         badge shown next to the intro paragraph

Citation counts come from the Google Scholar profile page (the only
Scholar request made). Author lists and venues come from Crossref/arXiv
via enrich.py, because Scholar blocks per-publication requests from CI.
The workflow wraps this script in `timeout`, so a blocked Scholar session
fails the run (keeping the previously published data) instead of hanging.
"""
import json
import os
import signal
import time
from contextlib import contextmanager
from datetime import datetime

from scholarly import scholarly

from enrich import enrich_publication

scholarly.set_timeout(15)
scholarly.set_retries(2)

AUTHOR_FETCH_TIMEOUT = 600  # seconds for the profile + publication list


@contextmanager
def time_limit(seconds):
    def _raise(signum, frame):
        raise TimeoutError(f"timed out after {seconds}s")

    previous = signal.signal(signal.SIGALRM, _raise)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)


print("Fetching Google Scholar profile...", flush=True)
with time_limit(AUTHOR_FETCH_TIMEOUT):
    author: dict = scholarly.search_author_id(os.environ['GOOGLE_SCHOLAR_ID'])
    scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
print(f"Profile fetched: {author.get('name')}, {author.get('citedby')} citations,"
      f" {len(author['publications'])} publications", flush=True)

# Look up complete author lists and venues so the homepage can render the
# full publication list. A miss keeps the basic entry (title/year/citations)
# and the site degrades gracefully.
for pub in author['publications']:
    title = pub['bib'].get('title', '')
    result = enrich_publication(title) if title else None
    if result:
        authors, venue = result
        pub['bib']['author'] = ' and '.join(authors)
        pub['venue'] = venue
        print(f"enriched: {title[:60]} | {venue[:40]}", flush=True)
    else:
        print(f"no match: {title[:60]}", flush=True)
    time.sleep(1)  # be polite to the open APIs

author['updated'] = str(datetime.now())
author['publications'] = {v['author_pub_id']: v for v in author['publications']}

os.makedirs('results', exist_ok=True)
with open('results/gs_data.json', 'w') as outfile:
    json.dump(author, outfile, ensure_ascii=False)

shieldio_data = {
    "schemaVersion": 1,
    "label": "citations",
    "message": f"{author['citedby']}",
}
with open('results/gs_data_shieldsio.json', 'w') as outfile:
    json.dump(shieldio_data, outfile, ensure_ascii=False)
print("Done.", flush=True)
