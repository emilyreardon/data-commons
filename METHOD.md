# How the map is made

## Turnout

- **Source:** NYC Campaign Finance Board, "Historical Voter Turnout" (NYC Open Data, rixx-fc37). It covers every election since 2017 and is published once a year, so the newest election runs a year or more behind.
- **Turnout** = people who voted ÷ (people who voted + eligible people who didn't). "Eligible" means registered voters in the Board of Elections file, not every adult resident.
- **From election districts to community districts:** the city publishes turnout by election district (about 4,000 small areas), not by community district (59). Each election district is placed in the community district that contains a point inside it, and the votes are added up. An election district that straddles a boundary counts entirely toward one side, so totals near borders are approximate.
- Rows the CFB withholds for privacy ("NA", very small districts) are skipped. Parks and airports (Joint Interest Areas) have no turnout.
- The regrouping reproduces the citywide figure the CFB reports (for example 12.8% for the 2023 general election).

## Public art

- **Volunteers:** OpenStreetMap points tagged `tourism=artwork` in a box around New York City, loaded live from the Overpass API; points outside the community districts are left out. Volunteers tag what they notice, from funded sculptures to murals to religious statues, often without a title or artist.
- **The city:** Public Design Commission inventory, DOT Art installations and Percent for Art projects (NYC Open Data). Percent for Art lists addresses only; they're placed with NYC Planning Labs GeoSearch.
- Each artwork is assigned to the community district it falls in.
- The two counts measure different things, and the gap between them is part of the picture. Neither is complete.

## What the map can't show

Whether public art affects turnout. Turnout is shaped by many forces, among them oppression, racism, poverty, labor protections and whether people believe they have power. The map sets two public datasets side by side to ask the question, not to answer it.

## Live data and saved copies

The map loads the newest data from each source when it opens and falls back to saved copies in `data/` if a source is down. The code that does this is in `nyc_civic_art_map.html`; the regrouping is in `tools/build_turnout.py`.
