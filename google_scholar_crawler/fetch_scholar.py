"""Fetch a Google Scholar author profile with one plain HTTP request.

This replaces the `scholarly` library. When Scholar refuses a request
(403 or a captcha page, common for CI runners), scholarly 1.x retries
forever with 60-120 s sleeps and ignores set_retries(), so the workflow
could only time out without saying why. A single request fails in
seconds and reports exactly what Scholar returned.

The returned dict mirrors the fields scholarly produced and the rest of
the pipeline (main.py, assets/js/scholar-stats.js) relies on.
"""
import re

import requests
from bs4 import BeautifulSoup

PROFILE_URL = 'https://scholar.google.com/citations'
PAGE_SIZE = 100
HEADERS = {
    'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/140.0 Safari/537.36'),
    'Accept-Language': 'en-US,en;q=0.9',
}


class ScholarBlocked(Exception):
    """Scholar answered, but not with the profile page."""


def _get_page(scholar_id, cstart):
    resp = requests.get(PROFILE_URL, headers=HEADERS, timeout=30, params={
        'user': scholar_id, 'hl': 'en', 'cstart': cstart, 'pagesize': PAGE_SIZE})
    if resp.status_code != 200:
        raise ScholarBlocked(f'HTTP {resp.status_code} from Google Scholar')
    page = BeautifulSoup(resp.text, 'html.parser')
    if page.select_one('#gs_captcha_f, #recaptcha'):
        raise ScholarBlocked('Google Scholar served a captcha page')
    if not page.select_one('#gsc_prf_in'):
        raise ScholarBlocked('response is not a Scholar profile page')
    return page


def _parse_publications(page, scholar_id):
    pubs = []
    for row in page.select('tr.gsc_a_tr'):
        link = row.select_one('a.gsc_a_at')
        if link is None:
            continue
        pub_id = re.search(r'citation_for_view=([^&]+)', link['href'])
        cites = row.select_one('.gsc_a_c a')
        year = row.select_one('.gsc_a_y span')
        pubs.append({
            'author_pub_id': pub_id.group(1) if pub_id else f'{scholar_id}:{len(pubs)}',
            'bib': {'title': link.get_text(strip=True),
                    'pub_year': year.get_text(strip=True) if year else ''},
            'num_citations': int(cites.get_text(strip=True) or 0) if cites else 0,
        })
    return pubs


def fetch_profile(scholar_id):
    page = _get_page(scholar_id, 0)
    # citations, h-index, i10-index: each as (all time, since 5 years ago)
    stats = [int(td.get_text(strip=True) or 0)
             for td in page.select('#gsc_rsb_st td.gsc_rsb_std')]
    stats += [0] * (6 - len(stats))
    years = [int(y.get_text()) for y in page.select('.gsc_g_t')]
    counts = [int(c.get_text() or 0) for c in page.select('.gsc_g_al')]

    publications = _parse_publications(page, scholar_id)
    while len(publications) and len(publications) % PAGE_SIZE == 0:
        more = _parse_publications(_get_page(scholar_id, len(publications)), scholar_id)
        if not more:
            break
        publications += more

    affiliation = page.select_one('#gsc_prf_i .gsc_prf_il')
    return {
        'scholar_id': scholar_id,
        'name': page.select_one('#gsc_prf_in').get_text(strip=True),
        'affiliation': affiliation.get_text(strip=True) if affiliation else '',
        'interests': [a.get_text(strip=True) for a in page.select('#gsc_prf_int a')],
        'citedby': stats[0], 'citedby5y': stats[1],
        'hindex': stats[2], 'hindex5y': stats[3],
        'i10index': stats[4], 'i10index5y': stats[5],
        'cites_per_year': dict(zip(years, counts)),
        'publications': publications,
    }
