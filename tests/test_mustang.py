import subprocess
from pathlib import Path
import sys

# Füge das Projekt-Root-Verzeichnis zu sys.path hinzu
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))


def validate_xml_with_mustang(xml_file):
    # Pfad zum Mustang-CLI JAR-File
    mustang_cli_jar = root_dir / "cli/Mustang-CLI-2.14.0-SNAPSHOT.jar"

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
        # Ausführung des Kommandos ohne 'check=True', um nicht in eine Exception zu laufen
        result = subprocess.run(command, capture_output=True, text=True)

        # Ausgabe des Mustang-CLI anzeigen
        if result.returncode == 0:
            print("Validierung erfolgreich!")
        else:
            print(
                "Validierung fehlgeschlagen. XML ist fehlerhaft, aber das ist erwartbar."
            )

        # Zeige die normale Ausgabe (stdout)
        print("Ergebnis:")
        print(result.stdout)

        # Falls Fehler in stderr sind, zeige sie ebenfalls an
        if result.stderr:
            print("Fehlerausgabe:")
            print(result.stderr)

    except Exception as e:
        print(f"Unerwarteter Fehler bei der Ausführung: {e}")


# Beispiel-XML-Datei
xml_file = root_dir / "tests/xml/comfort_zugferd.xml"

# Validierung starten
validate_xml_with_mustang(xml_file)
