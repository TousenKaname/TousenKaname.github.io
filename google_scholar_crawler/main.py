"""Fetch Google Scholar stats for the homepage.

Runs daily via .github/workflows/google_scholar_crawler.yaml and force-pushes
two JSON files to the `google-scholar-stats` branch:

- gs_data.json           full author profile; `publications` is keyed by
                         author_pub_id and consumed by the homepage JS
                         (per-paper citation counts + auto-generated
                         "Full Publication List" section)
- gs_data_shieldsio.json shields.io endpoint payload for the total-citations
                         badge shown next to the intro paragraph
"""
import json
import os
import random
import time
from datetime import datetime

from scholarly import scholarly

author: dict = scholarly.search_author_id(os.environ['GOOGLE_SCHOLAR_ID'])
scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])

# Fill each publication with its detail page so the homepage can show the
# complete author list and venue. A failed fill keeps the basic entry
# (title/year/citations) so the site degrades gracefully.
for pub in author['publications']:
    try:
        scholarly.fill(pub)
        bib = pub['bib']
        bib.pop('abstract', None)  # keep gs_data.json small
        pub['venue'] = (bib.get('journal') or bib.get('conference')
                        or bib.get('book') or bib.get('source')
                        or bib.get('publisher') or '')
        # be gentle with Google Scholar to avoid getting rate-limited
        time.sleep(random.uniform(2, 5))
    except Exception as exc:  # noqa: BLE001 - one bad entry must not kill the run
        print(f"WARN: could not fill {pub.get('author_pub_id')}: {exc}")

author['updated'] = str(datetime.now())
author['publications'] = {v['author_pub_id']: v for v in author['publications']}
print(json.dumps(author, indent=2))

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
