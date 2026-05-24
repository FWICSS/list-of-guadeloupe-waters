import csv
import json
import os
from datetime import date
from pathlib import Path

_LOCATIONS: list[dict] = []

_DATA_PATH = os.getenv(
    "DATA_PATH",
    str(Path(__file__).parent.parent / "docs" / "data.json"),
)
_CSV_PATH = os.getenv(
    "CSV_PATH",
    str(Path(__file__).parent.parent / "All" / "all.csv"),
)

ISLAND_MAP = {
    "Anse-Bertrand": "Grande-Terre", "Baie-Mahault": "Grande-Terre",
    "Le Gosier": "Grande-Terre", "Le Moule": "Grande-Terre",
    "Les Abymes": "Grande-Terre", "Morne-à-l'Eau": "Grande-Terre",
    "Petit-Canal": "Grande-Terre", "Pointe-à-Pitre": "Grande-Terre",
    "Port-Louis": "Grande-Terre", "Sainte-Anne": "Grande-Terre",
    "Saint-François": "Grande-Terre", "Baillif": "Basse-Terre",
    "Basse-Terre": "Basse-Terre", "Bouillante": "Basse-Terre",
    "Capesterre-Belle-Eau": "Basse-Terre", "Deshaies": "Basse-Terre",
    "Gourbeyre": "Basse-Terre", "Goyave": "Basse-Terre",
    "Lamentin": "Basse-Terre", "Petit-Bourg": "Basse-Terre",
    "Pointe-Noire": "Basse-Terre", "Saint-Claude": "Basse-Terre",
    "Sainte-Rose": "Basse-Terre", "Trois-Rivières": "Basse-Terre",
    "Vieux-Fort": "Basse-Terre", "Vieux-Habitants": "Basse-Terre",
    "Capesterre-de-Marie-Galante": "Marie-Galante",
    "Grand-Bourg": "Marie-Galante", "Saint-Louis": "Marie-Galante",
    "La Désirade": "La Désirade",
    "Terre-de-Bas": "Les Saintes", "Terre-de-Haut": "Les Saintes",
}


def _load_from_json(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _load_from_csv(path: str) -> list[dict]:
    locations = []
    with open(path, newline="", encoding="utf-8") as f:
        for i, row in enumerate(csv.DictReader(f)):
            try:
                lat = float(row["Latitude"])
                lon = float(row["Longitude"])
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
    return locations


def load():
    global _LOCATIONS
    try:
        _LOCATIONS = _load_from_json(_DATA_PATH)
        print(f"[data] {len(_LOCATIONS)} entrées chargées depuis {_DATA_PATH}")
    except FileNotFoundError:
        _LOCATIONS = _load_from_csv(_CSV_PATH)
        print(f"[data] {len(_LOCATIONS)} entrées chargées depuis {_CSV_PATH} (fallback CSV)")


def get_locations(type_: str | None = None, ile: str | None = None, commune: str | None = None) -> list[dict]:
    result = _LOCATIONS
    if type_:
        result = [l for l in result if l.get("type") == type_]
    if ile:
        result = [l for l in result if l.get("ile") == ile]
    if commune:
        commune_lower = commune.lower()
        result = [l for l in result if commune_lower in l.get("commune", "").lower()]
    return result


def get_location_by_id(id_: int) -> dict | None:
    for loc in _LOCATIONS:
        if loc.get("id") == id_:
            return loc
    return None


def get_stats() -> dict:
    beaches = sum(1 for l in _LOCATIONS if l.get("type") == "beach")
    rivers = sum(1 for l in _LOCATIONS if l.get("type") == "river")
    waterfalls = sum(1 for l in _LOCATIONS if l.get("type") == "waterfall")
    by_island: dict[str, int] = {}
    for loc in _LOCATIONS:
        ile = loc.get("ile", "Autre")
        by_island[ile] = by_island.get(ile, 0) + 1
    return {
        "total": len(_LOCATIONS),
        "beaches": beaches,
        "rivers": rivers,
        "waterfalls": waterfalls,
        "by_island": by_island,
        "last_updated": date.today().isoformat(),
    }
