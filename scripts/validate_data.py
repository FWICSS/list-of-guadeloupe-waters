#!/usr/bin/env python3
"""Validate all.csv — detect duplicates, empty names, out-of-bounds coords."""

import csv
from pathlib import Path

ROOT = Path(__file__).parent.parent
SOURCE = ROOT / "All" / "all.csv"

# Bounding box approximative de l'archipel guadeloupéen
LAT_MIN, LAT_MAX = 15.8, 16.55
LON_MIN, LON_MAX = -61.85, -60.95

errors = []
warnings = []


def check(rows):
    seen_coords = {}
    seen_names = {}

    for i, row in enumerate(rows):
        line = i + 2  # header = line 1
        nom = row.get("Nom", "").strip()
        type_ = row.get("Type", "").strip()
        commune = row.get("Commune", "").strip()

        # Nom vide ou générique
        if not nom or nom.lower() in ("plage", "rivière", "cascade"):
            errors.append(f"Ligne {line} : nom vide ou trop générique → '{nom}' ({commune})")

        # Coords valides
        try:
            lat = float(row["Latitude"])
            lon = float(row["Longitude"])
        except (ValueError, KeyError):
            errors.append(f"Ligne {line} : coordonnées invalides → {row.get('Latitude')} / {row.get('Longitude')}")
            continue

        if not (LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX):
            errors.append(f"Ligne {line} : coords hors Guadeloupe → {lat}, {lon} ({nom})")

        # Doublons de coordonnées exactes
        coord_key = (round(lat, 5), round(lon, 5))
        if coord_key in seen_coords:
            prev_line, prev_nom, prev_commune = seen_coords[coord_key]
            if nom == prev_nom and commune != prev_commune:
                warnings.append(
                    f"Ligne {line} : même lieu sous 2 communes → '{nom}' "
                    f"({prev_commune} ligne {prev_line} / {commune})"
                )
            elif nom != prev_nom:
                warnings.append(
                    f"Ligne {line} : coords identiques pour 2 noms différents → "
                    f"'{prev_nom}' (ligne {prev_line}) et '{nom}'"
                )
        else:
            seen_coords[coord_key] = (line, nom, commune)

        # Quasi-doublons de nom dans la même commune
        name_key = (nom.lower().strip(), commune)
        if name_key in seen_names:
            warnings.append(
                f"Ligne {line} : nom quasi-identique dans la même commune → "
                f"'{nom}' déjà vu ligne {seen_names[name_key]}"
            )
        else:
            seen_names[name_key] = line


def main():
    with open(SOURCE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    check(rows)

    print(f"\n=== Rapport de validation — {SOURCE.name} ===")
    print(f"Total entrées : {len(rows)}\n")

    if errors:
        print(f"ERREURS ({len(errors)}) :")
        for e in errors:
            print(f"  ✗ {e}")
    else:
        print("  Aucune erreur.")

    print()

    if warnings:
        print(f"AVERTISSEMENTS ({len(warnings)}) :")
        for w in warnings:
            print(f"  ⚠ {w}")
    else:
        print("  Aucun avertissement.")

    print()
    if not errors:
        print("Données valides.")
    else:
        print("Corriger les erreurs avant de publier.")


if __name__ == "__main__":
    main()
