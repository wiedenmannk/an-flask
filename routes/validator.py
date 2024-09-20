import logging
from flask import Blueprint, jsonify, request
from pathlib import Path
import os
import sys

# Set up logging
logging.basicConfig(level=logging.DEBUG)

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
        # Log request data for debugging
        logging.debug(f"Incoming request: {request.data}")

        data = request.get_json()
        logging.debug(f"Parsed JSON data: {data}")

        # Prüfen, ob das XML-Inhalt-Feld vorhanden ist
        if not data or "xml_content" not in data:
            logging.error("No XML content provided in request.")
            return jsonify({"error": "No XML content provided"}), 400

        # Daten aus dem Request erhalten
        xml_data = data["xml_content"]
        logging.debug(f"XML content data: {xml_data}")

        # Extrahiere den Buffer und den Dateinamen
        buffer_info = xml_data.get("buffer", {})
        buffer_data = buffer_info.get("data", [])
        original_name = xml_data.get("originalname", "temp_xml_file.xml")

        # Log Buffer Details
        logging.debug(f"Buffer type: {buffer_info.get('type')}")
        logging.debug(f"Buffer data length: {len(buffer_data)}")
        logging.debug(f"Original filename: {original_name}")

        # Wandelt die Daten aus dem Array in ein bytes-Objekt um
        buffer_bytes = bytes(buffer_data)

        # Temporäre Datei erstellen
        temp_file_path = temp_dir / original_name
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(buffer_bytes)
            logging.debug(f"Saved buffer to temporary file: {temp_file_path}")

        # Mustang-CLI JAR-Pfad festlegen
        jar_path = root_dir / "cli/Mustang-CLI-2.14.0-SNAPSHOT.jar"
        logging.debug(f"Using Mustang CLI JAR at: {jar_path}")

        # XMLValidator instanziieren
        validator = XMLValidator(jar_path)

        # Validierung durchführen und Ergebnis als JSON zurückgeben
        json_output = validator.validate_to_json(temp_file_path)
        logging.debug(f"Validation output: {json_output}")
        return jsonify(json_output), 200

    except Exception as e:
        logging.error(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 500
