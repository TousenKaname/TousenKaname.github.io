"""Build the visitor-globe JSON for the homepage.

Runs on a schedule via .github/workflows/visitor_stats.yaml and force-pushes
visitors.json to the `visitor-stats` branch, which
assets/js/visitor-globe.js reads to draw the visitor globe in the footer.

The numbers come from the site's Flag Counter (the counter image in the
footer is what records each visit). Flag Counter has no API, so the
per-country totals are parsed from its public "countries" stats page, and
each country is placed on the globe via countries.csv:

- lat/lon: country centroids from Google's canonical countries table
  (https://developers.google.com/public-data/docs/canonical/countries_csv)
- iso_n3:  ISO 3166-1 numeric code, the feature id used by world-atlas,
           so visited countries can be shaded on the map

Standard library only, so the workflow needs no pip install. Any error
fails the run and leaves the previously published data in place.
"""
import csv
import html
import json
import os
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

COUNTER_ID = os.environ.get('FLAG_COUNTER_ID', 'gqFE')
COUNTRIES_URL = f'https://s01.flagcounter.com/countries/{COUNTER_ID}/'

# One table row per country: display name, visitor count, and the
# per-country chart link (/detail30/<code>/...), which carries the
# two-letter code. The name used to link to /factbook/<code>/ until
# Flag Counter switched those links to Wikipedia on 2026-10-17, so the
# code is taken from the chart link instead, and whitespace/attributes
# are matched loosely to survive small markup changes.
ROW_RE = re.compile(
    r'<u>([^<]+)</u></a>\s*</font>\s*</td>\s*'
    r'<td[^>]*>\s*<font[^>]*>\s*([\d,]+)\s*</font>\s*</td>\s*'
    r'<td[^>]*>\s*<a href="?/detail\d*/(\w\w)/')
TOTAL_RE = re.compile(r'Countries \d+ - \d+ of ([\d,]+)')


# Flag Counter answers 403 to any User-Agent that looks like a bot (the
# old 'visitor-globe-crawler/1.0' started failing on 2026-10-13), so
# present as an ordinary browser.
USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/129.0 Safari/537.36')


# When overloaded (or hit too often) Flag Counter returns HTTP 200 with a
# short "Server too busy. Please try again in 5 minutes." body instead of
# the stats page, so retry that, and transient HTTP errors, after a pause.
ATTEMPTS = 3
RETRY_DELAY = 150  # seconds; two waits ~ the 5 minutes it asks for, within timeout-minutes


def fetch_page(url):
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    for attempt in range(1, ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(request, timeout=30) as resp:
                page = resp.read().decode('utf-8', errors='replace')
            if 'Server too busy' not in page:
                return page
            problem = 'Flag Counter says the server is too busy'
        except urllib.error.HTTPError as err:
            if err.code not in (403, 429) and err.code < 500:
                raise
            problem = f'HTTP {err.code} from Flag Counter'
        if attempt == ATTEMPTS:
            raise SystemExit(f'{problem}; giving up after {ATTEMPTS} attempts')
        print(f'::warning::{problem}; retrying in {RETRY_DELAY}s '
              f'(attempt {attempt}/{ATTEMPTS})', flush=True)
        time.sleep(RETRY_DELAY)


def load_country_table():
    with open('countries.csv', newline='') as infile:
        return {row['code']: row for row in csv.DictReader(infile)}


def parse_countries(page, table):
    countries = []
    for name, visitors, code in ROW_RE.findall(page):
        entry = {'code': code.upper(),
                 'name': html.unescape(name).strip(),
                 'visitors': int(visitors.replace(',', ''))}
        # codes like A1/A2 (proxies, satellite) have no place on the map
        info = table.get(entry['code'])
        if info:
            entry.update(lat=float(info['lat']), lon=float(info['lon']),
                         iso_n3=info['iso_n3'])
        countries.append(entry)
    return countries


page = fetch_page(COUNTRIES_URL)
countries = parse_countries(page, load_country_table())
if not countries:
    snippet = ' '.join(page[:300].split())
    raise SystemExit('No country rows found; the Flag Counter page layout may have changed. '
                     f'Page starts with: {snippet}')

total_match = TOTAL_RE.search(page)
if total_match and int(total_match.group(1).replace(',', '')) != len(countries):
    print(f"::warning::Flag Counter lists {total_match.group(1)} countries "
          f"but {len(countries)} rows were parsed", flush=True)

data = {
    'updated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'stats_url': f'https://info.flagcounter.com/{COUNTER_ID}',
    'total_visitors': sum(c['visitors'] for c in countries),
    'countries': sorted(countries, key=lambda c: -c['visitors']),
}

os.makedirs('results', exist_ok=True)
with open('results/visitors.json', 'w') as outfile:
    json.dump(data, outfile, ensure_ascii=False)
print(f"{data['total_visitors']} visitors from {len(countries)} countries/regions; "
      f"top: {', '.join(c['name'] for c in data['countries'][:5])}", flush=True)
