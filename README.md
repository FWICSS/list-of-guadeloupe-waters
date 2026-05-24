# 🌊 Guadeloupe Waters

![Entries](https://img.shields.io/badge/entries-~250-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![GitHub Actions](https://img.shields.io/github/actions/workflow/status/dimitriaigle/List_of_beaches_and_rivers_of_Guadeloupe/validate.yml?label=CI)

[![GitHub Pages](https://img.shields.io/badge/map-GitHub%20Pages-orange)](https://dimitriaigle.github.io/List_of_beaches_and_rivers_of_Guadeloupe) [![Static API](https://img.shields.io/badge/API-static%20JSON-purple)](https://dimitriaigle.github.io/List_of_beaches_and_rivers_of_Guadeloupe/api/v1/)

> Open dataset of beaches, rivers, and waterfalls in Guadeloupe — ready to use in GeoJSON, KML, CSV, and JSON.
>
> Dataset ouvert des plages, rivières et cascades de Guadeloupe — disponible en GeoJSON, KML, CSV et JSON.

---

## 🗺️ Interactive Map

Explore all locations on an interactive Leaflet map:
**[dimitriaigle.github.io/List_of_beaches_and_rivers_of_Guadeloupe](https://dimitriaigle.github.io/List_of_beaches_and_rivers_of_Guadeloupe)**

<!-- Screenshot will be added once the map is deployed -->

---

## 📡 API

A REST API is available for programmatic access to the dataset.

**Base URL:** `https://your-coolify-domain.com` *(replace with your deployed instance)*
**Documentation:** `/docs` (Swagger UI)

### Endpoints

```bash
# List all locations
curl https://your-coolify-domain.com/v1/locations

# Beaches only
curl https://your-coolify-domain.com/v1/beaches

# Dataset statistics
curl https://your-coolify-domain.com/v1/stats
```

### Free API key

```bash
curl -X POST https://your-coolify-domain.com/v1/keys/register \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com"}'
```

### Pricing

| Plan | Requests/day | Price |
|---|---|---|
| Free | 100 | $0 |
| Premium | Unlimited | Contact us |

> The static API on GitHub Pages (`docs/api/v1/`) requires no key and has no rate limits.

---

## 📦 Data Formats

| Format | File | Description |
|---|---|---|
| CSV | `All/all.csv` | Source of truth — edit this file to contribute |
| GeoJSON | `All/all.geojson` | Compatible with Mapbox, QGIS, Leaflet |
| KML | `All/all.kml` | Google Earth, Google Maps import |
| JSON | `docs/data.json` | Enriched JSON for the web app |
| Static API | `docs/api/v1/` | Serverless endpoint, served via GitHub Pages |

---

## 🗂️ Data Schema

| Column | Type | Description |
|---|---|---|
| `Nom` | string | Official name of the location |
| `Code_Postal` | string | 5-digit postal code (`97xxx`) |
| `Commune` | string | Municipality |
| `Latitude` | decimal | WGS84 latitude |
| `Longitude` | decimal | WGS84 longitude |
| `Type` | string | `beach`, `river`, or `waterfall` |
| `Île` | string | Island (`Grande-Terre`, `Basse-Terre`, etc.) |

---

## 🚀 Quick Start

```bash
# Use the data directly (no setup needed)
curl https://dimitriaigle.github.io/List_of_beaches_and_rivers_of_Guadeloupe/api/v1/beaches.json

# Clone the repository
git clone https://github.com/dimitriaigle/List_of_beaches_and_rivers_of_Guadeloupe
cd List_of_beaches_and_rivers_of_Guadeloupe

# Regenerate all output formats from all.csv
python3 scripts/generate_all.py
```

---

## 🤝 Contributing

Contributions are welcome — corrections, new locations, or additional data fields.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide. The short version:

1. Fork the repo
2. Edit `All/all.csv` only (it is the single source of truth)
3. Run `python3 scripts/validate_data.py` then `python3 scripts/generate_all.py`
4. Open a pull request with a source reference for the added/corrected data

---

## 📄 License

[MIT](LICENSE) — free to use, share, and build upon.