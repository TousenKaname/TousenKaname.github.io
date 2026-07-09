"""Build the Google Scholar stats JSON for the homepage.

Runs daily (and on pushes to main) via
.github/workflows/google_scholar_crawler.yaml and force-pushes two JSON
files to the `google-scholar-stats` branch:

- gs_data.json           author profile; `publications` is keyed by
                         author_pub_id and consumed by the homepage JS
                         (per-paper citation counts + auto-generated
                         "Full Publication List" section)
- gs_data_shieldsio.json shields.io endpoint payload for the total-citations
                         badge shown next to the intro paragraph

Citation counts come from the Google Scholar profile page, fetched in a
subprocess (fetch_scholar.py) under a hard timeout because Scholar
sometimes blocks CI runners and scholarly then hangs. When that happens,
the previously published data is reused as the base — the `updated`
timestamp is kept so the page shows the last successful Scholar sync —
and only the Crossref/arXiv enrichment (authors, venues) is refreshed.
"""
import json
import os
import subprocess
import sys
import time
from datetime import datetime

import requests

from enrich import enrich_publication

SCHOLAR_FETCH_TIMEOUT = 300  # seconds before the Scholar subprocess is killed


def fetch_from_scholar():
    subprocess.run([sys.executable, '-u', 'fetch_scholar.py'],
                   timeout=SCHOLAR_FETCH_TIMEOUT, check=True)
    with open('results/scholar_raw.json') as infile:
        author = json.load(infile)
    os.remove('results/scholar_raw.json')
    author['updated'] = str(datetime.now())
    return author


def fetch_previous_data():
    repo = os.environ.get('GITHUB_REPOSITORY',
                          'TousenKaname/TousenKaname.github.io')
    url = f'https://raw.githubusercontent.com/{repo}/google-scholar-stats/gs_data.json'
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    author = resp.json()
    # stored keyed by author_pub_id; the enrichment loop wants a list
    author['publications'] = list(author['publications'].values())
    return author


print("Fetching Google Scholar profile...", flush=True)
try:
    author = fetch_from_scholar()
except Exception as exc:  # noqa: BLE001 - blocked Scholar must not kill the run
    print(f"WARN: Scholar fetch failed ({exc}); "
          f"re-enriching previously published data instead", flush=True)
    author = fetch_previous_data()

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
