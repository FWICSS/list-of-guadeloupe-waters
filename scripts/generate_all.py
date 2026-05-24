#!/usr/bin/env python3
"""Master script — generate all output formats from All/all.csv."""

import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent

steps = [
    ("Validation des données", SCRIPTS / "validate_data.py"),
    ("Génération KML (tous)", SCRIPTS / "generate_kml.py"),
    ("Génération KML plages", SCRIPTS / "generate_kml_beaches.py"),
    ("Génération GeoJSON", SCRIPTS / "generate_geojson.py"),
    ("Génération JSON (web)", SCRIPTS / "generate_json.py"),
    ("Génération API statique", SCRIPTS / "generate_static_api.py"),
]


def run(label, script):
    print(f"\n{'─'*50}")
    print(f"  {label}")
    print(f"{'─'*50}")
    result = subprocess.run([sys.executable, str(script)], capture_output=False)
    if result.returncode != 0:
        print(f"  ÉCHEC : {script.name}")
        sys.exit(1)


def main():
    print("=== Guadeloupe Waters — génération de tous les formats ===")
    for label, script in steps:
        run(label, script)
    print(f"\n{'═'*50}")
    print("  Tous les fichiers générés avec succès.")
    print(f"{'═'*50}\n")


if __name__ == "__main__":
    main()
