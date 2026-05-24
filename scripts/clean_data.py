#!/usr/bin/env python3
"""Clean and normalise all.csv.

Writes a cleaned copy to All/all_cleaned.csv and prints a report.
Does NOT overwrite all.csv — human review required before replacing.
"""

import csv
import math
import re
from pathlib import Path

from common import ISLAND_MAP, ROOT, load_csv

SOURCE = ROOT / "All" / "all.csv"
OUTPUT = ROOT / "All" / "all_cleaned.csv"

ARTICLES = {"de", "du", "des", "la", "le", "les", "d'", "l'", "à", "au", "aux", "en", "et"}
VALID_TYPES = {"beach", "river", "waterfall"}


def title_fr(text):
    """Capitalize French place names, keeping articles lowercase."""
    if not text:
        return text
    words = re.split(r"(\s+|-)", text)
    result = []
    for i, word in enumerate(words):
        if re.match(r"\s+|-", word):
            result.append(word)
            continue
        low = word.lower()
        # Always capitalize the very first real word
        if i == 0 or (i == 2 and re.match(r"\s+|-", words[1])):
            result.append(word.capitalize())
        elif low in ARTICLES:
            result.append(low)
        else:
            result.append(word.capitalize())
    return "".join(result)


def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    a = (math.sin((phi2 - phi1) / 2) ** 2
         + math.cos(phi1) * math.cos(phi2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def main():
    rows = load_csv(SOURCE)
    errors = []
    warnings = []
    cleaned = []

    coords_seen = {}

    for i, row in enumerate(rows):
        line = i + 2
        r = {k: v.strip() for k, v in row.items()}

        # Normalize name
        original_nom = r.get("Nom", "")
        r["Nom"] = title_fr(original_nom)
        if r["Nom"] != original_nom:
            warnings.append(f"Ligne {line} : nom normalisé '{original_nom}' → '{r['Nom']}'")

        # Validate type
        type_ = r.get("Type", "").lower()
        if type_ not in VALID_TYPES:
            errors.append(f"Ligne {line} : type invalide '{type_}' pour '{r['Nom']}'")
        r["Type"] = type_

        # Validate commune in ISLAND_MAP
        commune = r.get("Commune", "")
        if commune and commune not in ISLAND_MAP:
            warnings.append(f"Ligne {line} : commune inconnue '{commune}' pour '{r['Nom']}'")

        # Validate coordinates
        try:
            lat = float(r["Latitude"])
            lon = float(r["Longitude"])
        except (ValueError, KeyError):
            errors.append(f"Ligne {line} : coordonnées invalides pour '{r['Nom']}'")
            cleaned.append(r)
            continue

        # Near-duplicate detection (< 100m)
        coord_key = (round(lat, 4), round(lon, 4))
        for prev_key, (prev_line, prev_nom) in coords_seen.items():
            plat, plon = prev_key
            dist = haversine(lat, lon, plat, plon)
            if dist < 100:
                warnings.append(
                    f"Ligne {line} : '{r['Nom']}' est à {dist:.0f}m de '{prev_nom}' (ligne {prev_line})"
                )
                break
        coords_seen[coord_key] = (line, r["Nom"])

        cleaned.append(r)

    # Write cleaned CSV
    if cleaned:
        fieldnames = list(cleaned[0].keys())
        with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(cleaned)

    print(f"\n=== Rapport de nettoyage — {SOURCE.name} ===")
    print(f"Total entrées : {len(rows)}\n")

    if errors:
        print(f"ERREURS ({len(errors)}) :")
        for e in errors:
            print(f"  ✗ {e}")
    else:
        print("  Aucune erreur.")

    print()

    if warnings:
        print(f"AVERTISSEMENTS / MODIFICATIONS ({len(warnings)}) :")
        for w in warnings:
            print(f"  ⚠ {w}")
    else:
        print("  Aucun avertissement.")

    print(f"\nFichier nettoyé écrit dans : {OUTPUT}")
    print("Comparer avec all.csv avant de remplacer.")


if __name__ == "__main__":
    main()
