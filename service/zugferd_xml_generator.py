import xml.etree.ElementTree as ET
from typing import Dict


class ZugferdXmlGenerator:
    def generate_xml_from_json(
        self, json_data: Dict, root_element: str = "Invoice"
    ) -> str:
        root = ET.Element(root_element)
        self._build_xml_recursive(root, json_data)
        return ET.tostring(root, encoding="utf-8", method="xml").decode("utf-8")

    def _build_xml_recursive(self, parent: ET.Element, data: Dict):
        """
        Diese Funktion geht rekursiv durch das JSON-Objekt und fügt verschachtelte Elemente als XML hinzu.
        """
        for key, value in data.items():
            child = ET.SubElement(parent, key)
            if isinstance(value, dict):
                # Rekursion, wenn der Wert ein verschachteltes Objekt ist
                self._build_xml_recursive(child, value)
            else:
                # Fügt den Wert als Textinhalt hinzu, wenn er kein verschachteltes Objekt ist
                child.text = str(value)

    def write_xml(self, xml_string: str, file_path: str) -> None:
        """
        Schreibt einen XML-String in die angegebene Datei.
        """
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(xml_string)
