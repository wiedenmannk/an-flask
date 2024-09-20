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
        self.logger.setLevel(logging.DEBUG)  # Set to DEBUG to see all log messages

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
            result = subprocess.run(command, capture_output=True, text=True)

            output = result.stdout.strip() if result.stdout else "No output generated"
            message = (
                result.stderr.strip() if result.stderr else "No error message generated"
            )

            self.logger.debug(f"Validation output: {output}")  # Log stdout
            self.logger.debug(f"Validation message: {message}")  # Log stderr

            if result.returncode == 0:
                self.logger.info("Validierung erfolgreich.")
                return {
                    "status": "success",
                    "message": "",  # Keine Fehlermeldung bei Erfolg
                    "output": output,
                }
            else:
                self.logger.error("Validierung fehlgeschlagen.")
                return {"status": "error", "message": message, "output": output}
        except Exception as e:
            self.logger.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
            return {"status": "error", "message": str(e), "output": ""}

    def validate_to_json(self, xml_file):
        result = self.validate_xml(xml_file)
        self.logger.debug(
            f"API Response: {json.dumps(result, indent=4)}"
        )  # Additional log for API response
        return json.dumps(result, indent=4)
