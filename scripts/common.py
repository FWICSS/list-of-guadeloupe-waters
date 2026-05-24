#!/usr/bin/env python3
"""Shared utilities for all generation scripts."""

from pathlib import Path
import csv

ROOT = Path(__file__).parent.parent

ISLAND_MAP = {
    "Anse-Bertrand": "Grande-Terre",
    "Baie-Mahault": "Grande-Terre",
    "Le Gosier": "Grande-Terre",
    "Le Moule": "Grande-Terre",
    "Les Abymes": "Grande-Terre",
    "Morne-à-l'Eau": "Grande-Terre",
    "Petit-Canal": "Grande-Terre",
    "Pointe-à-Pitre": "Grande-Terre",
    "Port-Louis": "Grande-Terre",
    "Sainte-Anne": "Grande-Terre",
    "Saint-François": "Grande-Terre",
    "Baillif": "Basse-Terre",
    "Basse-Terre": "Basse-Terre",
    "Bouillante": "Basse-Terre",
    "Capesterre-Belle-Eau": "Basse-Terre",
    "Deshaies": "Basse-Terre",
    "Gourbeyre": "Basse-Terre",
    "Goyave": "Basse-Terre",
    "Lamentin": "Basse-Terre",
    "Petit-Bourg": "Basse-Terre",
    "Pointe-Noire": "Basse-Terre",
    "Saint-Claude": "Basse-Terre",
    "Sainte-Rose": "Basse-Terre",
    "Trois-Rivières": "Basse-Terre",
    "Vieux-Fort": "Basse-Terre",
    "Vieux-Habitants": "Basse-Terre",
    "Capesterre-de-Marie-Galante": "Marie-Galante",
    "Grand-Bourg": "Marie-Galante",
    "Saint-Louis": "Marie-Galante",
    "La Désirade": "La Désirade",
    "Terre-de-Bas": "Les Saintes",
    "Terre-de-Haut": "Les Saintes",
}


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
