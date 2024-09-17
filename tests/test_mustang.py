import subprocess
from pathlib import Path
import sys

# Füge das Projekt-Root-Verzeichnis zu sys.path hinzu
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))


def validate_xml_with_mustang(xml_file):
    # Pfad zum Mustang-CLI JAR-File
    mustang_cli_jar = root_dir / "cli/Mustang-CLI-2.14.0.jar"

    # Mustang-CLI-Kommando erstellen
    command = [
        "java",
        "-jar",
        mustang_cli_jar,
        "--action",
        "validate",
        "--source",
        xml_file,
    ]

    try:
        # Ausführung des Kommandos
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Validierung erfolgreich!")
        print("Ergebnis:")
        print(result.stdout)  # Ausgabe des Mustang-CLI anzeigen
    except subprocess.CalledProcessError as e:
        print(f"Fehler bei der Validierung: {e}")
        print(f"Fehlerausgabe: {e.stderr}")


# Beispiel-XML-Datei
# xml_file = root_dir / "tests/xml/zugferd/extended.xml"
xml_file = root_dir / "tests/xml/comfort_zugferd.xml"

# Validierung starten
validate_xml_with_mustang(xml_file)
