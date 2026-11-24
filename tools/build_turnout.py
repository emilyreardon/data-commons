#!/usr/bin/env python3
"""
build_turnout.py: regroup NYC voter turnout from Election Districts into Community Districts.

Why: the Campaign Finance Board publishes turnout for every election since 2017
(NYC Open Data, "Historical Voter Turnout", rixx-fc37), but only by Election District,
Assembly District and other political districts, not by Community District. This script
works out which Community District each Election District sits in, then adds up the
votes.

Run from the data-commons folder after downloading the three source files into source/:
    python3 tools/build_turnout.py

Reads
  source/election_districts.geojson   NYC Open Data wwxk-38u4 (Board of Elections)
  source/turnout_ed.csv               NYC Open Data rixx-fc37, Election District rows
  data/community_districts.geojson    NYC Open Data 5crt-au7u (City Planning)
Writes
  data/ed_to_cd.json        which Election Districts fall in each Community District
  data/turnout_by_cd.json   turnout by Community District for every election, newest first

Method: each Election District is placed in the Community District that contains a point
inside it. Turnout = people who voted / (people who voted + eligible people who did not).
Rows the CFB marks "NA" (very small districts, withheld for privacy) are skipped.
Parks and airports (Joint Interest Areas, district numbers above 18) get no turnout.
"""
import csv, json, os, sys
from datetime import date

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(HERE, *a)
BORO = {'1': 'MN', '2': 'BX', '3': 'BK', '4': 'QN', '5': 'SI'}


def polygons(geom):
    """List of polygons, each a list of rings, each ring a list of [x, y]."""
    if geom['type'] == 'Polygon':
        return [geom['coordinates']]
    if geom['type'] == 'MultiPolygon':
        return geom['coordinates']
    return []


def inside(x, y, polys):
    """Even-odd ray casting over every ring, so holes count as outside."""
    hit = False
    for poly in polys:
        for ring in poly:
            n = len(ring)
            for i in range(n):
                x1, y1 = ring[i][0], ring[i][1]
                x2, y2 = ring[(i + 1) % n][0], ring[(i + 1) % n][1]
                if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                    hit = not hit
    return hit


def point_inside(polys):
    """A point inside the shape: the centroid if it is inside, otherwise the middle of
    the first stretch inside along the horizontal line through the centroid."""
    biggest = max(polys, key=lambda p: len(p[0]))
    ring = biggest[0]
    cx = sum(p[0] for p in ring) / len(ring)
    cy = sum(p[1] for p in ring) / len(ring)
    if inside(cx, cy, polys):
        return cx, cy
    xs = []
    for poly in polys:
        for r in poly:
            for i in range(len(r)):
                x1, y1 = r[i][0], r[i][1]
                x2, y2 = r[(i + 1) % len(r)][0], r[(i + 1) % len(r)][1]
                if (y1 > cy) != (y2 > cy):
                    xs.append((x2 - x1) * (cy - y1) / (y2 - y1) + x1)
    xs.sort()
    if len(xs) >= 2:
        return (xs[0] + xs[1]) / 2, cy
    return ring[0][0], ring[0][1]


def bbox(polys):
    xs = [p[0] for poly in polys for r in poly for p in r]
    ys = [p[1] for poly in polys for r in poly for p in r]
    return min(xs), min(ys), max(xs), max(ys)


def num(s):
    s = (s or '').replace(',', '').strip()
    try:
        return float(s)
    except ValueError:
        return None


def main():
    # Community Districts (59 real ones; parks and airports are numbered above 18)
    cds = []
    for f in json.load(open(P('data', 'community_districts.geojson')))['features']:
        raw = str(f['properties'].get('boro_cd') or f['properties'].get('borocd'))
        key = BORO[raw[0]] + raw[1:].zfill(2)[-2:]
        if int(raw[1:]) > 18:
            continue
        polys = polygons(f['geometry'])
        cds.append((key, polys, bbox(polys)))

    # Election District → Community District
    ed2cd, missed = {}, []
    for f in json.load(open(P('source', 'election_districts.geojson')))['features']:
        ed = int(str(f['properties']['elect_dist']).replace(',', ''))
        polys = polygons(f['geometry'])
        if not polys:
            continue
        x, y = point_inside(polys)
        for key, cpolys, (x0, y0, x1, y1) in cds:
            if x0 <= x <= x1 and y0 <= y <= y1 and inside(x, y, cpolys):
                ed2cd[ed] = key
                break
        else:
            missed.append(ed)
    lookup = {}
    for ed, key in sorted(ed2cd.items()):
        lookup.setdefault(key, []).append(ed)
    json.dump(lookup, open(P('data', 'ed_to_cd.json'), 'w'), separators=(',', ':'))
    print(f'{len(ed2cd)} election districts placed in {len(lookup)} community districts; '
          f'{len(missed)} fall in parks, airports or water')

    # Turnout, every election
    sums, dates, city = {}, {}, {}
    skipped = 0
    for r in csv.DictReader(open(P('source', 'turnout_ed.csv'), newline='')):
        if r.get('geo_level') != 'Election District':
            continue
        v, d = num(r.get('voted')), num(r.get('did_not_vote'))
        if v is None or d is None:
            skipped += 1
            continue
        el = r['election']
        dates[el] = r['election_date'][:10]
        c = city.setdefault(el, [0, 0])          # citywide: every district, matched or not
        c[0] += v
        c[1] += d
        key = ed2cd.get(int(num(r['geo_unit'])))
        if not key:
            continue
        a = sums.setdefault(el, {}).setdefault(key, [0, 0])
        a[0] += v
        a[1] += d
    elections = []
    for el, by_cd in sums.items():
        t = {k: round(v / (v + d), 3) for k, (v, d) in by_cd.items() if v + d > 0}
        cv, cd_ = city[el]
        elections.append({'name': el, 'date': dates[el], 'citywide': round(cv / (cv + cd_), 3),
                          'turnout': dict(sorted(t.items()))})
    elections.sort(key=lambda e: e['date'], reverse=True)
    out = {
        'built': date.today().isoformat(),
        'source': 'NYC Campaign Finance Board, Historical Voter Turnout (NYC Open Data rixx-fc37), '
                  'regrouped from Election Districts to Community Districts',
        'elections': elections,
    }
    json.dump(out, open(P('data', 'turnout_by_cd.json'), 'w'), separators=(',', ':'))
    print(f'{len(elections)} elections written, newest: {elections[0]["name"]} ({elections[0]["date"]}); '
          f'{skipped} withheld rows skipped')
    for e in elections:
        print(f'  {e["date"]}  {e["name"]:<28} citywide {e["citywide"]:.1%}  {len(e["turnout"])} districts')


if __name__ == '__main__':
    sys.exit(main())
