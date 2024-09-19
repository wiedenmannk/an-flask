import logging
from flask import Blueprint, jsonify, request
from pathlib import Path
import os
import sys

# Füge das Projekt-Root-Verzeichnis zu sys.path hinzu
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from service.xml_validator import XMLValidator

# Erstelle den Blueprint
vbp = Blueprint("validator", __name__)

# Verzeichnis für temporäre Dateien erstellen, falls nicht vorhanden
temp_dir = root_dir / "tmp"
if not temp_dir.exists():
    os.makedirs(temp_dir)


# Route für die XML-Validierung
@vbp.route("/api/validate", methods=["POST"])
def validate_xml():
    try:
        data = request.get_json()

        if not data or "xmlContent" not in data:
            return jsonify({"error": "No XML content provided"}), 400

        # XML-Inhalt aus dem POST-Request erhalten
        xml_content = data["xmlContent"]

        # Temporäre Datei speichern
        temp_file_path = temp_dir / "temp_xml_file.xml"
        with open(temp_file_path, "w", encoding="utf-8") as temp_file:
            temp_file.write(xml_content)

        # Mustang-CLI JAR-Pfad festlegen
        jar_path = root_dir / "cli/Mustang-CLI-2.14.0-SNAPSHOT.jar"

        # XMLValidator instanziieren
        validator = XMLValidator(jar_path)

        # Validierung durchführen und Ergebnis als JSON zurückgeben
        json_output = validator.validate_to_json(temp_file_path)
        return jsonify(json_output), 200

    except Exception as e:
        logging.error(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 500
