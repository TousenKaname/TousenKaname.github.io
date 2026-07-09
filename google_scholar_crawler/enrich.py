"""Look up complete author lists and venues for publications.

Google Scholar aggressively blocks per-publication detail requests from CI
runners, so enrichment uses CI-friendly open APIs instead:

- Crossref (published journal/conference papers with DOIs)
- arXiv (preprints; also yields a journal_ref when one exists)

Only confident title matches are accepted; anything else returns None and
the homepage falls back to title/year/citations for that entry.
"""
import html
import re
import xml.etree.ElementTree as ET

import requests

HTTP_TIMEOUT = 15
USER_AGENT = {'User-Agent': 'gs-homepage-crawler/1.0 (mailto:guoanwang971@gmail.com)'}

ARXIV_NS = {'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom'}


def _normalize(title):
    return re.sub(r'[^a-z0-9]+', ' ', html.unescape(title).lower()).strip()


def _titles_match(a, b):
    na, nb = _normalize(a), _normalize(b)
    if not na or not nb:
        return False
    if na == nb or na in nb or nb in na:
        return True
    # tolerate spacing drift like Scholar's "5.5 m" vs "5.5M"
    da, db = na.replace(' ', ''), nb.replace(' ', '')
    if da == db or da in db or db in da:
        return True
    ta, tb = set(na.split()), set(nb.split())
    return len(ta & tb) / max(len(ta | tb), 1) >= 0.9


def _from_crossref(title):
    resp = requests.get('https://api.crossref.org/works',
                        params={'query.bibliographic': title, 'rows': 3},
                        headers=USER_AGENT, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    for item in resp.json()['message']['items']:
        candidate = (item.get('title') or [''])[0]
        if not _titles_match(title, candidate):
            continue
        authors = [' '.join(filter(None, [a.get('given'), a.get('family')]))
                   for a in item.get('author', [])]
        authors = [a for a in authors if a]
        if not authors:
            continue
        container = item.get('container-title') or []
        venue = container[0] if container else item.get('publisher', '')
        return authors, venue
    return None


def _from_arxiv(title):
    # arXiv's query parser chokes on &, quotes, etc. — search on words only
    query = 'ti:"%s"' % re.sub(r'[^\w\s.-]+', ' ', title).strip()
    resp = requests.get('https://export.arxiv.org/api/query',
                        params={'search_query': query, 'max_results': 5},
                        headers=USER_AGENT, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    for entry in ET.fromstring(resp.text).findall('atom:entry', ARXIV_NS):
        candidate = ' '.join(entry.find('atom:title', ARXIV_NS).text.split())
        if not _titles_match(title, candidate):
            continue
        authors = [a.find('atom:name', ARXIV_NS).text
                   for a in entry.findall('atom:author', ARXIV_NS)]
        if not authors:
            continue
        journal_ref = entry.find('arxiv:journal_ref', ARXIV_NS)
        venue = journal_ref.text if journal_ref is not None else 'arXiv preprint'
        return authors, venue
    return None


def _try(source, title):
    try:
        return source(title)
    except Exception as exc:  # noqa: BLE001 - a miss must not kill the run
        print(f"WARN: {source.__name__} failed for '{title[:60]}': {exc}",
              flush=True)
        return None


def enrich_publication(title):
    """Return (authors, venue) for a publication title, or None.

    Crossref is preferred for published papers (it knows the real venue);
    when it only finds a preprint-server deposit (or no venue), arXiv's
    record is used instead so preprints read consistently.
    """
    crossref = _try(_from_crossref, title)
    if crossref and crossref[1] and not re.search(r'rxiv', crossref[1], re.I):
        return crossref
    return _try(_from_arxiv, title) or crossref
