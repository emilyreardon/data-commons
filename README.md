# Not Inevitable: Public Art & Voter Turnout in NYC

A live map of voter turnout by community district beside public art as counted by volunteers (OpenStreetMap) and by the city (Public Design Commission, DOT Art, Percent for Art). It doesn't show that public art drives civic engagement; it uses both open datasets to propose art as one way forward.

Live: https://emilyreardon.org/public-art-and-voter-turnout.html

## What's here

| | |
|---|---|
| `nyc_civic_art_map.html` | The whole map: one page, Leaflet and Turf.js |
| `METHOD.md` | How turnout is calculated and how art is counted |
| `tools/build_turnout.py` | Regroups NYC turnout from election districts into community districts |
| `tools/geocode_percent_for_art.py` | Finds coordinates for Percent for Art addresses |
| `tools/simplify_cds.py` | Makes a light copy of the district boundaries for the web |
| `data/` | Saved copies of every dataset, so the map works if a live source is down |

## Updating the data

The map loads the newest data live. To refresh the saved copies:

```
python3 tools/build_turnout.py
python3 tools/geocode_percent_for_art.py
python3 tools/simplify_cds.py
```

`build_turnout.py` expects the election-district boundaries and turnout table in `source/` (download commands are at the top of the script).

## Credits

Began as my final project for Collecting and Using the Data Commons (Summer 2026), taught by Zhi Keng He. Data: NYC Campaign Finance Board, NYC City Planning, Public Design Commission, NYC DOT, NYC Department of Cultural Affairs (NYC Open Data); © OpenStreetMap contributors (ODbL). Code written with help from Claude (Anthropic).

Code: MIT License (see `LICENSE`).
