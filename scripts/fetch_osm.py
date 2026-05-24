#!/usr/bin/env python3
"""Fetch candidate locations from OpenStreetMap Overpass API.

Results are written to scripts/osm_candidates.csv for human review.
Do NOT auto-import into all.csv — verify each entry before adding.
"""

import csv
import json
import math
import urllib.request
import urllib.parse
from pathlib import Path

from common import ISLAND_MAP, ROOT, load_csv

SOURCE = ROOT / "All" / "all.csv"
OUTPUT = Path(__file__).parent / "osm_candidates.csv"

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Bounding box: south, west, north, east
BBOX = "15.8,-61.85,16.55,-60.95"

QUERIES = [
    ("beach", f'node["natural"="beach"]({BBOX}); way["natural"="beach"]({BBOX});'),
    ("river", f'node["waterway"="river"]({BBOX}); way["waterway"="river"]({BBOX});'),
    ("waterfall", f'node["waterway"="waterfall"]({BBOX}); way["waterway"="waterfall"]({BBOX});'),
]

PROXIMITY_M = 200


def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def overpass_query(query_body):
    full_query = f"[out:json][timeout:30];({query_body});out center;"
    data = urllib.parse.urlencode({"data": full_query}).encode()
    req = urllib.request.Request(OVERPASS_URL, data=data)
    req.add_header("User-Agent", "GuadeloupeWaters/1.0 (github.com/dimitriaigle)")
    with urllib.request.urlopen(req, timeout=40) as resp:
        return json.loads(resp.read())


def extract_coords(element):
    if element["type"] == "node":
        return element["lat"], element["lon"]
    if element["type"] == "way" and "center" in element:
        return element["center"]["lat"], element["center"]["lon"]
    return None, None


def is_known(lat, lon, known):
    for klat, klon in known:
        if haversine(lat, lon, klat, klon) < PROXIMITY_M:
            return True
    return False


def main():
    existing = load_csv(SOURCE)
    known_coords = []
    for row in existing:
        try:
            known_coords.append((float(row["Latitude"]), float(row["Longitude"])))
        except ValueError:
            pass

    candidates = []

    for type_key, query_body in QUERIES:
        print(f"  Requête OSM : {type_key}...", end=" ", flush=True)
        try:
            result = overpass_query(query_body)
        except Exception as e:
            print(f"ERREUR ({e})")
            continue

        elements = result.get("elements", [])
        new_count = 0
        for el in elements:
            lat, lon = extract_coords(el)
            if lat is None:
                continue
            tags = el.get("tags", {})
            nom = tags.get("name", "").strip()
            if not nom:
                continue
            if is_known(lat, lon, known_coords):
                continue

            commune = tags.get("addr:city", tags.get("is_in:city", ""))
            cp = tags.get("addr:postcode", "")
            ile = ISLAND_MAP.get(commune, "")

            candidates.append({
                "Nom": nom,
                "Code_Postal": cp,
                "Commune": commune,
                "Latitude": round(lat, 6),
                "Longitude": round(lon, 6),
                "Type": type_key,
                "Ile_estimee": ile,
                "OSM_id": f"{el['type']}/{el['id']}",
            })
            new_count += 1

        print(f"{new_count} nouveaux candidats")

    if candidates:
        fieldnames = ["Nom", "Code_Postal", "Commune", "Latitude", "Longitude", "Type", "Ile_estimee", "OSM_id"]
        with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(candidates)
        print(f"\n{len(candidates)} candidats écrits dans {OUTPUT}")
        print("Vérifier chaque entrée avant d'ajouter dans All/all.csv")
    else:
        print("\nAucun nouveau candidat trouvé.")
        if OUTPUT.exists():
            OUTPUT.unlink()


if __name__ == "__main__":
    print("=== Recherche OSM — candidats Guadeloupe ===")
    main()
