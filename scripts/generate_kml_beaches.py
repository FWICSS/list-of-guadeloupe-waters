#!/usr/bin/env python3
"""Generate a KML file for beaches only — for use in Google Earth / Google Maps."""

import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path

from common import ISLAND_MAP, ROOT

SOURCE = ROOT / "All" / "all.csv"
OUTPUT = ROOT / "Beaches" / "beaches.kml"

STYLE = {
    "icon": "http://maps.google.com/mapfiles/kml/shapes/sunny.png",
    "color": "ff00d7ff",
    "label": "Plages de Guadeloupe",
}


def indent_xml(elem):
    rough = ET.tostring(elem, encoding="unicode")
    reparsed = minidom.parseString(rough)
    return reparsed.toprettyxml(indent="  ")


def build_kml(rows):
    kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    doc = ET.SubElement(kml, "Document")

    ET.SubElement(doc, "name").text = "Plages de Guadeloupe"
    ET.SubElement(doc, "description").text = (
        "Liste des plages de Guadeloupe — github.com/dimitriaigle"
    )

    style = ET.SubElement(doc, "Style", id="style_beach")
    icon_style = ET.SubElement(style, "IconStyle")
    ET.SubElement(icon_style, "color").text = STYLE["color"]
    ET.SubElement(icon_style, "scale").text = "1.1"
    icon = ET.SubElement(icon_style, "Icon")
    ET.SubElement(icon, "href").text = STYLE["icon"]
    label_style = ET.SubElement(style, "LabelStyle")
    ET.SubElement(label_style, "scale").text = "0.8"

    folder = ET.SubElement(doc, "Folder")
    ET.SubElement(folder, "name").text = STYLE["label"]

    count = 0
    for row in rows:
        if row.get("Type", "").lower() != "beach":
            continue

        pm = ET.SubElement(folder, "Placemark")
        ET.SubElement(pm, "name").text = row["Nom"]
        ET.SubElement(pm, "styleUrl").text = "#style_beach"

        commune = row.get("Commune", "")
        island = ISLAND_MAP.get(commune, "")
        desc = (
            f"<b>{row['Nom']}</b><br/>"
            f"Commune : {commune}<br/>"
            f"Code postal : {row.get('Code_Postal', '')}<br/>"
            f"Île : {island}"
        )
        ET.SubElement(pm, "description").text = desc

        point = ET.SubElement(pm, "Point")
        ET.SubElement(point, "coordinates").text = (
            f"{row['Longitude']},{row['Latitude']},0"
        )
        count += 1

    return kml, count


def main():
    with open(SOURCE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    kml, count = build_kml(rows)
    xml_str = indent_xml(kml)

    lines = xml_str.split("\n")
    if lines[0].startswith("<?xml"):
        xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + "\n".join(lines[1:])

    OUTPUT.write_text(xml_str, encoding="utf-8")
    print(f"KML plages généré : {OUTPUT}")
    print(f"Plages exportées : {count}")


if __name__ == "__main__":
    main()
