#!/usr/bin/env python3
"""Make a light copy of the community district boundaries for the web map.

The full NYC file is about 3.8 MB, so the districts drew last and the map looked broken
while it loaded. This keeps the shapes (to within about 5 metres) at a fraction of the size.

Reads  data/community_districts.geojson   (the full download, left untouched)
Writes data/community_districts_web.geojson

Run from the data-commons folder:  python3 tools/simplify_cds.py
"""
import json

SRC = 'data/community_districts.geojson'
OUT = 'data/community_districts_web.geojson'
TOLERANCE = 0.00005   # degrees, about 5 m: under a pixel at the map's closest zoom
KEEP = ('boro_cd',)   # the only property the map uses


def rdp(points, tol):
    """Ramer-Douglas-Peucker: drop points that barely change the line."""
    if len(points) < 3:
        return points
    (x1, y1), (x2, y2) = points[0], points[-1]
    dx, dy = x2 - x1, y2 - y1
    norm = (dx * dx + dy * dy) ** 0.5 or 1e-12
    far, idx = 0.0, 0
    for i in range(1, len(points) - 1):
        x, y = points[i]
        d = abs(dy * x - dx * y + x2 * y1 - y2 * x1) / norm
        if d > far:
            far, idx = d, i
    if far <= tol:
        return [points[0], points[-1]]
    return rdp(points[:idx + 1], tol)[:-1] + rdp(points[idx:], tol)


def ring(r):
    # a ring starts and ends on the same point, so split it at the point farthest from the start
    x0, y0 = r[0]
    far = max(range(len(r)), key=lambda i: (r[i][0] - x0) ** 2 + (r[i][1] - y0) ** 2)
    pts = rdp(r[:far + 1], TOLERANCE)[:-1] + rdp(r[far:], TOLERANCE)
    if len(pts) < 4:          # a ring needs at least 4 points (first = last); keep tiny islands as they were
        pts = r
    return [[round(x, 5), round(y, 5)] for x, y in pts]


def main():
    d = json.load(open(SRC))
    for f in d['features']:
        g = f['geometry']
        if g['type'] == 'Polygon':
            g['coordinates'] = [ring(r) for r in g['coordinates']]
        else:
            g['coordinates'] = [[ring(r) for r in poly] for poly in g['coordinates']]
        f['properties'] = {k: f['properties'][k] for k in KEEP if k in f['properties']}
    json.dump(d, open(OUT, 'w'), separators=(',', ':'))
    print(f'wrote {OUT}')


if __name__ == '__main__':
    main()
