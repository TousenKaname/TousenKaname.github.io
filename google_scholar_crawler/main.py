"""Build the Google Scholar stats JSON for the homepage.

Runs every 8 hours (and on pushes to main) via
.github/workflows/google_scholar_crawler.yaml and force-pushes two JSON
files to the `google-scholar-stats` branch:

- gs_data.json           author profile; `publications` is keyed by
                         author_pub_id and consumed by the homepage JS
                         (per-paper citation counts + auto-generated
                         "Full Publication List" section)
- gs_data_shieldsio.json shields.io endpoint payload for the total-citations
                         badge shown next to the intro paragraph

Citation counts come from the Google Scholar profile page, fetched with
one plain request (fetch_scholar.py). Scholar sometimes refuses CI
runners (403 / captcha); the request then fails within seconds and logs
what Scholar returned. When that happens, the previously published data is reused as the base — the `updated`
timestamp is kept so the page shows the last successful Scholar sync —
and only the Crossref/arXiv enrichment (authors, venues) is refreshed.
Each such fallback is flagged with a warning in the Actions UI, and once
the data is STALE_AFTER_DAYS old the workflow fails so the breakage is
noticed instead of the page silently going stale.
"""
import json
import os
import time
from datetime import datetime

import requests

from enrich import enrich_publication
from fetch_scholar import fetch_profile

STALE_AFTER_DAYS = 3  # failed syncs tolerated before the workflow goes red


def fetch_from_scholar():
    author = fetch_profile(os.environ['GOOGLE_SCHOLAR_ID'])
    author['updated'] = str(datetime.now())
    print(f"Scholar profile fetched: {author['name']}, {author['citedby']} citations, "
          f"{len(author['publications'])} publications", flush=True)
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


def report_scholar_fallback(exc, updated):
    print(f"::warning::Google Scholar fetch failed ({exc}); "
          f"re-publishing data from the last successful sync ({updated})",
          flush=True)
    age = datetime.now() - datetime.fromisoformat(updated)
    github_output = os.environ.get('GITHUB_OUTPUT')
    if age.days >= STALE_AFTER_DAYS and github_output:
        # read by the "Check Scholar sync" step of the workflow
        with open(github_output, 'a') as outfile:
            outfile.write(f"scholar_stale_since={updated.split(' ')[0]}\n")


print("Fetching Google Scholar profile...", flush=True)
try:
    author = fetch_from_scholar()
except Exception as exc:  # noqa: BLE001 - blocked Scholar must not kill the run
    author = fetch_previous_data()
    report_scholar_fallback(exc, author['updated'])

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
