import logging
from flask import Blueprint, jsonify, request
from pathlib import Path
import sys

# Füge das Projekt-Root-Verzeichnis zu sys.path hinzu
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from service.xml_validator import XMLValidator

# Erstelle den Blueprint
vbp = Blueprint("validator", __name__)


# Route für die XML-Validierung
@vbp.route("/validate", methods=["POST"])
def validate_xml():
    try:
        # XML-Datei aus dem POST-Request erhalten
        if "xml_file" not in request.files:
            return jsonify({"error": "No XML file provided."}), 400

        xml_file = request.files["xml_file"]

        # Speichere die Datei temporär, um sie mit dem Validator zu verarbeiten
        temp_file_path = root_dir / "tmp" / xml_file.filename
        xml_file.save(temp_file_path)

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


# Diese Funktion registrierst du später in der Hauptapp:
# app.register_blueprint(vbp, url_prefix="/validator")
