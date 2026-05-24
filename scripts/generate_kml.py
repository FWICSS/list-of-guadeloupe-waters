#!/usr/bin/env python3
"""Generate a KML file from all.csv for use in Google Earth / Google Maps."""

import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path

from common import ISLAND_MAP, ROOT

SOURCE = ROOT / "All" / "all.csv"
OUTPUT = ROOT / "All" / "all.kml"

STYLES = {
    "beach": {
        "icon": "http://maps.google.com/mapfiles/kml/shapes/sunny.png",
        "color": "ff00d7ff",  # yellow (ABGR)
        "label": "Plages",
    },
    "river": {
        "icon": "http://maps.google.com/mapfiles/kml/shapes/water.png",
        "color": "ffff5500",  # blue (ABGR)
        "label": "Rivières",
    },
    "waterfall": {
        "icon": "http://maps.google.com/mapfiles/kml/shapes/water.png",
        "color": "ff0099ff",  # cyan (ABGR)
        "label": "Cascades",
    },
}

def indent_xml(elem):
    """Return a pretty-printed XML string."""
    rough = ET.tostring(elem, encoding="unicode")
    reparsed = minidom.parseString(rough)
    return reparsed.toprettyxml(indent="  ")


def make_style(doc, style_id, cfg):
    style = ET.SubElement(doc, "Style", id=style_id)
    icon_style = ET.SubElement(style, "IconStyle")
    color = ET.SubElement(icon_style, "color")
    color.text = cfg["color"]
    scale = ET.SubElement(icon_style, "scale")
    scale.text = "1.1"
    icon = ET.SubElement(icon_style, "Icon")
    href = ET.SubElement(icon, "href")
    href.text = cfg["icon"]
    label_style = ET.SubElement(style, "LabelStyle")
    label_scale = ET.SubElement(label_style, "scale")
    label_scale.text = "0.8"


def build_kml(rows):
    kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    doc = ET.SubElement(kml, "Document")

    name_el = ET.SubElement(doc, "name")
    name_el.text = "Guadeloupe Waters"
    desc_el = ET.SubElement(doc, "description")
    desc_el.text = "Plages, rivières et cascades de Guadeloupe — github.com/dimitriaigle"

    for type_key, cfg in STYLES.items():
        make_style(doc, f"style_{type_key}", cfg)

    folders = {t: ET.SubElement(doc, "Folder") for t in STYLES}
    for type_key, cfg in STYLES.items():
        ET.SubElement(folders[type_key], "name").text = cfg["label"]

    for row in rows:
        type_key = row.get("Type", "").lower()
        if type_key not in STYLES:
            continue

        folder = folders[type_key]
        pm = ET.SubElement(folder, "Placemark")

        ET.SubElement(pm, "name").text = row["Nom"]
        ET.SubElement(pm, "styleUrl").text = f"#style_{type_key}"

        commune = row.get("Commune", "")
        island = ISLAND_MAP.get(commune, "")
        desc = (
            f"<b>{row['Nom']}</b><br/>"
            f"Commune : {commune}<br/>"
            f"Code postal : {row.get('Code_Postal', '')}<br/>"
            f"Île : {island}<br/>"
            f"Type : {type_key.capitalize()}"
        )
        ET.SubElement(pm, "description").text = desc

        point = ET.SubElement(pm, "Point")
        coords = ET.SubElement(point, "coordinates")
        coords.text = f"{row['Longitude']},{row['Latitude']},0"

    return kml


def main():
    with open(SOURCE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    kml = build_kml(rows)
    xml_str = indent_xml(kml)

    # Remove the XML declaration added by minidom (kml files don't always need it)
    lines = xml_str.split("\n")
    if lines[0].startswith("<?xml"):
        xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + "\n".join(lines[1:])

    OUTPUT.write_text(xml_str, encoding="utf-8")

    counts = {}
    for row in rows:
        t = row.get("Type", "unknown")
        counts[t] = counts.get(t, 0) + 1

    print(f"KML généré : {OUTPUT}")
    print(f"Entrées exportées : {sum(counts.values())} ({counts})")


if __name__ == "__main__":
    main()
