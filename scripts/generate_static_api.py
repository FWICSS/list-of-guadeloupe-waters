#!/usr/bin/env python3
"""Generate static JSON API files for GitHub Pages.

Output structure under docs/api/v1/:
  locations.json  — all entries  {count, data}
  beaches.json    — type=beach   {count, data}
  rivers.json     — type=river   {count, data}
  waterfalls.json — type=waterfall {count, data}
  stats.json      — aggregate stats
"""

import json
from datetime import date
from pathlib import Path

from common import ROOT

DATA_FILE = ROOT / "docs" / "data.json"
OUT_DIR = ROOT / "docs" / "api" / "v1"


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    locations = json.loads(DATA_FILE.read_text(encoding="utf-8"))

    beaches = [l for l in locations if l.get("type") == "beach"]
    rivers = [l for l in locations if l.get("type") == "river"]
    waterfalls = [l for l in locations if l.get("type") == "waterfall"]

    def write(name, data):
        payload = {"count": len(data), "data": data}
        (OUT_DIR / name).write_text(
            json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
        print(f"  {OUT_DIR / name}  ({len(data)} entrées)")

    write("locations.json", locations)
    write("beaches.json", beaches)
    write("rivers.json", rivers)
    write("waterfalls.json", waterfalls)

    by_island = {}
    for loc in locations:
        ile = loc.get("ile", "Autre")
        by_island[ile] = by_island.get(ile, 0) + 1

    stats = {
        "total": len(locations),
        "beaches": len(beaches),
        "rivers": len(rivers),
        "waterfalls": len(waterfalls),
        "by_island": by_island,
        "last_updated": date.today().isoformat(),
    }
    (OUT_DIR / "stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"  {OUT_DIR / 'stats.json'}  (stats)")
    print(f"\nAPI statique générée : {OUT_DIR}")


if __name__ == "__main__":
    print("=== Génération API statique ===")
    main()
