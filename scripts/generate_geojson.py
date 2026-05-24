#!/usr/bin/env python3
"""Generate GeoJSON from all.csv — standard format for mapping libraries."""

import csv
import json
from pathlib import Path

from common import ISLAND_MAP, ROOT

SOURCE = ROOT / "All" / "all.csv"
OUTPUT = ROOT / "All" / "all.geojson"


def main():
    features = []
    with open(SOURCE, newline="", encoding="utf-8") as f:
        for i, row in enumerate(csv.DictReader(f)):
            try:
                lon = float(row["Longitude"])
                lat = float(row["Latitude"])
            except ValueError:
                print(f"  Ligne {i+2} ignorée (coords invalides) : {row['Nom']}")
                continue

            commune = row.get("Commune", "")
            features.append({
                "type": "Feature",
                "id": i + 1,
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat],
                },
                "properties": {
                    "nom": row["Nom"],
                    "type": row.get("Type", ""),
                    "commune": commune,
                    "code_postal": row.get("Code_Postal", ""),
                    "ile": ISLAND_MAP.get(commune, "Autre"),
                },
            })

    geojson = {
        "type": "FeatureCollection",
        "features": features,
    }

    OUTPUT.write_text(json.dumps(geojson, ensure_ascii=False, indent=2), encoding="utf-8")

    counts = {}
    for f in features:
        t = f["properties"]["type"]
        counts[t] = counts.get(t, 0) + 1

    print(f"GeoJSON généré : {OUTPUT}")
    print(f"Features : {len(features)} ({counts})")


if __name__ == "__main__":
    main()
