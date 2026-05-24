#!/usr/bin/env python3
"""Generate docs/data.json for the GitHub Pages web app."""

import csv
import json
from pathlib import Path

from common import ISLAND_MAP, ROOT

SOURCE = ROOT / "All" / "all.csv"
OUTPUT = ROOT / "docs" / "data.json"


def main():
    OUTPUT.parent.mkdir(exist_ok=True)

    locations = []
    with open(SOURCE, newline="", encoding="utf-8") as f:
        for i, row in enumerate(csv.DictReader(f)):
            try:
                lon = float(row["Longitude"])
                lat = float(row["Latitude"])
            except ValueError:
                continue

            commune = row.get("Commune", "")
            locations.append({
                "id": i + 1,
                "nom": row["Nom"],
                "type": row.get("Type", ""),
                "commune": commune,
                "code_postal": row.get("Code_Postal", ""),
                "ile": ISLAND_MAP.get(commune, "Autre"),
                "lat": lat,
                "lon": lon,
            })

    OUTPUT.write_text(json.dumps(locations, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    counts = {}
    for loc in locations:
        t = loc["type"]
        counts[t] = counts.get(t, 0) + 1

    print(f"JSON généré : {OUTPUT}")
    print(f"Entrées : {len(locations)} ({counts})")


if __name__ == "__main__":
    main()
