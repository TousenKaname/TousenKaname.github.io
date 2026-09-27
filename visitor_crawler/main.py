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
import urllib.request
from datetime import datetime, timezone

COUNTER_ID = os.environ.get('FLAG_COUNTER_ID', 'gqFE')
COUNTRIES_URL = f'https://s01.flagcounter.com/countries/{COUNTER_ID}/'

# one table row per country: code, display name, visitor count
ROW_RE = re.compile(
    r'<a href=/factbook/(\w\w)/\w+ style="text-decoration:none;"><u>([^<]+)</u></a>'
    r'</font></td><td width=1%><font face=arial size=2>([\d,]+)</font>')
TOTAL_RE = re.compile(r'Countries \d+ - \d+ of ([\d,]+)')


def fetch_page(url):
    request = urllib.request.Request(
        url, headers={'User-Agent': 'visitor-globe-crawler/1.0 (+https://tousenkaname.github.io)'})
    with urllib.request.urlopen(request, timeout=30) as resp:
        return resp.read().decode('utf-8', errors='replace')


def load_country_table():
    with open('countries.csv', newline='') as infile:
        return {row['code']: row for row in csv.DictReader(infile)}


def parse_countries(page, table):
    countries = []
    for code, name, visitors in ROW_RE.findall(page):
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
    raise SystemExit('No country rows found; the Flag Counter page layout may have changed')

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
