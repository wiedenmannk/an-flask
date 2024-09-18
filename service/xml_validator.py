import subprocess
import json
import logging
from pathlib import Path


class XMLValidator:
    def __init__(self, jar_path, logger=None):
        self.jar_path = jar_path
        self.logger = logger or logging.getLogger(__name__)
        self.setup_logger()

    def setup_logger(self):
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def validate_xml(self, xml_file):
        command = [
            "java",
            "-jar",
            str(self.jar_path),
            "--action",
            "validate",
            "--source",
            str(xml_file),
        ]

        try:
            # Subprocess run without 'check=True', so we handle errors without raising an exception
            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0:
                self.logger.info("Validierung erfolgreich.")
                return self.parse_output(result.stdout)
            else:
                self.logger.error("Validierung fehlgeschlagen.")
                self.logger.error(f"Fehlerausgabe: {result.stderr}")
                return {
                    "status": "error",
                    "message": result.stderr,
                    "output": result.stdout,  # Include the output in case it's relevant
                }
        except Exception as e:
            self.logger.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
            return {"status": "error", "message": str(e)}

    def parse_output(self, output):
        try:
            # Parst den XML-Teil des Outputs (vereinfachtes Beispiel)
            validation_result = {"status": "success", "details": output}
            return validation_result
        except Exception as e:
            self.logger.error(f"Fehler beim Parsen der Ausgabe: {e}")
            return {"status": "error", "message": str(e)}

    def validate_to_json(self, xml_file):
        result = self.validate_xml(xml_file)
        return json.dumps(result, indent=4)
