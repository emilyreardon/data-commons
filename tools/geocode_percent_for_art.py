#!/usr/bin/env python3
"""
geocode_percent_for_art.py: place Percent for Art projects on the map.

The Department of Cultural Affairs publishes completed Percent for Art projects
(NYC Open Data gzdv-qiga, updated yearly) with street addresses but no coordinates.
This script looks each address up with NYC GeoSearch (geosearch.planninglabs.nyc, the
City Planning address finder, free and keyless) and saves the results, so the map does
not have to look up hundreds of addresses on every visit.

The map still reads the live dataset each visit and looks up only addresses that are not
in this file yet, so new projects appear without running this again. Run it now and then
to refresh the saved copy:
    python3 tools/geocode_percent_for_art.py

Writes
  data/percent_for_art_geocodes.json   address → [lat, lon], or null if it could not be found
  data/percent_for_art.json            the dataset itself, a saved copy in case it is offline
"""
import json, os, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(HERE, *a)
DATASET = 'https://data.cityofnewyork.us/resource/gzdv-qiga.json?$limit=5000'
GEOSEARCH = 'https://geosearch.planninglabs.nyc/v2/search?size=1&text='


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'emilyreardon.org public art map'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def key(row):
    """The same key the map uses: address, borough and zip."""
    return ' | '.join((row.get(k) or '').strip() for k in ('address', 'borough2', 'zip_code'))


def main():
    rows = get(DATASET)
    json.dump(rows, open(P('data', 'percent_for_art.json'), 'w'), separators=(',', ':'))
    path = P('data', 'percent_for_art_geocodes.json')
    cache = json.load(open(path)) if os.path.exists(path) else {}
    todo = sorted({key(r) for r in rows if (r.get('address') or '').strip()} - set(cache))
    print(f'{len(rows)} projects, {len(todo)} addresses to look up')
    for i, k in enumerate(todo, 1):
        address, borough, zip_code = k.split(' | ')
        text = f'{address}, {borough} {zip_code}'.strip(', ')
        try:
            f = get(GEOSEARCH + urllib.parse.quote(text)).get('features', [])
            cache[k] = [round(f[0]['geometry']['coordinates'][1], 6), round(f[0]['geometry']['coordinates'][0], 6)] if f else None
        except Exception as e:
            print('  could not look up', text, e)
            continue
        if i % 25 == 0:
            print(f'  {i} of {len(todo)}')
        time.sleep(0.1)   # be gentle with the shared service
    json.dump(dict(sorted(cache.items())), open(path, 'w'), indent=0)
    found = sum(1 for v in cache.values() if v)
    print(f'{found} of {len(cache)} addresses placed; the rest (such as "various locations") stay off the map')


if __name__ == '__main__':
    main()
