import json
import xml.etree.ElementTree as ET
from pathlib import Path

class ZugferdXmlGenerator:
    def __init__(self):
        pass

    def generate_xml_from_json(self, json_data: dict, xml_filepath: str) -> None:
        """
        Generiert ein ZUGFeRD-taugliches XML aus JSON-Daten und speichert es auf der Festplatte.
        """
        try:
            # Erstelle das XML-Dokument basierend auf den JSON-Daten
            root = ET.Element("Invoice")

            # Beispielhafte Umwandlung von JSON zu XML, dies kann an die ZUGFeRD-Spezifikationen angepasst werden
            for key, value in json_data.items():
                child = ET.SubElement(root, key)
                child.text = str(value)
            
            # Speichere das XML als Datei
            tree = ET.ElementTree(root)
            tree.write(xml_filepath, encoding='utf-8', xml_declaration=True)
            print(f"ZUGFeRD XML-Datei erfolgreich gespeichert: {xml_filepath}")

        except Exception as e:
            print(f"Fehler beim Generieren des ZUGFeRD-XML: {e}")

    def read_xml(self, xml_filepath: str) -> ET.Element:
        """
        Liest eine XML-Datei von der Festplatte und gibt das Wurzelelement zurück.
        """
        try:
            tree = ET.parse(xml_filepath)
            root = tree.getroot()
            return root

        except Exception as e:
            print(f"Fehler beim Lesen der XML-Datei: {e}")
            return None

    def write_xml(self, xml_element: ET.Element, xml_filepath: str) -> None:
        """
        Schreibt ein XML-Element auf die Festplatte.
        """
        try:
            tree = ET.ElementTree(xml_element)
            tree.write(xml_filepath, encoding='utf-8', xml_declaration=True)
            print(f"XML-Datei erfolgreich geschrieben: {xml_filepath}")

        except Exception as e:
            print(f"Fehler beim Schreiben der XML-Datei: {e}")

# Beispielnutzung der Klasse
if __name__ == "__main__":
    generator = ZugferdXmlGenerator()

    # Beispielhafte JSON-Daten für ZUGFeRD
    json_data = {
        "InvoiceNumber": "12345",
        "InvoiceDate": "2024-09-06",
        "Amount": "100.00"
    }
    xml_filepath = "zugferd.xml"

    # ZUGFeRD XML aus JSON generieren
    generator.generate_xml_from_json(json_data, xml_filepath)

    # XML-Datei lesen und erneut speichern (Beispiel)
    root = generator.read_xml(xml_filepath)
    if root is not None:
        generator.write_xml(root, "copy_of_zugferd.xml")
