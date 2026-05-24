# Contributing to Guadeloupe Waters

Contributions are welcome — corrections, new locations, additional data fields.

## Data source of truth

**`All/all.csv` is the only file to edit directly.** All other files (category CSVs, Markdown tables, KML, GeoJSON, JSON) are generated automatically from it.

## Column format

| Column | Type | Description |
|---|---|---|
| `Nom` | string | Full official name of the location |
| `Code_Postal` | string | 5-digit postal code (97xxx) |
| `Commune` | string | Municipality name |
| `Latitude` | decimal | WGS84 latitude (positive = north) |
| `Longitude` | decimal | WGS84 longitude (negative = west) |
| `Type` | string | `beach`, `river`, or `waterfall` |

## Policy on shared commune boundaries

Some geographic features sit on the boundary between two communes. **One entry per physical location** — use the commune that administers the site (the one managing beach access or signage). If genuinely ambiguous, use the commune with the lower postal code.

## Steps to add or correct an entry

1. Fork the repository
2. Edit `All/all.csv` only
3. Run validation: `python3 scripts/validate_data.py`
4. Regenerate all files: `python3 scripts/generate_all.py`
5. Commit the generated files alongside `all.csv`
6. Open a pull request with a brief description of the change and its source

## Coordinate accuracy

Use coordinates accurate to at least 5 decimal places. Source from OpenStreetMap, IGN Géoportail, or GPS measurement. Avoid rounding coordinates to fewer than 4 decimal places.

## Naming conventions

- Use the official French name as listed on IGN maps or the commune's official website
- Capitalize consistently: `Plage de l'Anse Laborde`, not `plage de l'anse laborde`
- For disambiguating identical names: append the commune in parentheses, e.g. `Rivière Moustique (Petit-Bourg)`

## Running scripts

```bash
# Validate data quality
python3 scripts/validate_data.py

# Regenerate all output formats
python3 scripts/generate_all.py
```
