from pathlib import Path
import sys
from lxml import etree

# Füge das Projekt-Root-Verzeichnis zu sys.path hinzu
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))


# ok diese Tests laufen leider nicht, da das schematron nicht von python gelesen werden kann
def validate_xml_with_xsd(xml_file, xsd_file):
    """Validiert das XML-Dokument gegen das XSD-Schema."""
    try:
        # Lade das XSD-Schema
        with open(xsd_file, "rb") as xsd_f:
            xsd_doc = etree.parse(xsd_f)
            xsd_schema = etree.XMLSchema(xsd_doc)

        # Lade das XML-Dokument
        with open(xml_file, "rb") as xml_f:
            xml_doc = etree.parse(xml_f)

        # Validierung des XML-Dokuments
        xsd_schema.assertValid(xml_doc)
        print("Das XML-Dokument ist XSD-gültig.")
        return True

    except etree.DocumentInvalid as e:
        print(f"XSD-Validierung fehlgeschlagen: {e}")
        return False


def validate_xml_with_schematron(xml_file, sch_file):
    """Validiert das XML-Dokument gegen die Schematron-Regeln."""
    try:
        # Lade die Schematron-Datei
        with open(sch_file, "rb") as sch_f:
            schematron_doc = etree.parse(sch_f)
            schematron = etree.Schematron(schematron_doc)  # Entferne 'store_report'

        # Lade das XML-Dokument
        with open(xml_file, "rb") as xml_f:
            xml_doc = etree.parse(xml_f)

        # Führe die Schematron-Validierung durch
        if schematron.validate(xml_doc):
            print("Das XML-Dokument ist Schematron-gültig.")
            return True
        else:
            print("Schematron-Validierung fehlgeschlagen.")
            print("Fehlerprotokoll:")
            for error in schematron.error_log:
                print(f"Zeile {error.line}, Spalte {error.column}: {error.message}")
            return False

    except Exception as e:
        print(f"Fehler bei der Schematron-Validierung: {e}")
        return False


# Verwende 'Path' für die Pfad-Konstruktion
validator_path = "validator"
extended = "EXTENDED"
schema_extended_file = "FACTUR-X_EXTENDED.xsd"
schematron_extended_file = "FACTUR-X_EXTENDED.sch"
version_path = "ZF_221"
validator_root = root_dir / validator_path

schema_path_extended = (
    validator_root / "schema" / version_path / extended
)  # Dies muss auch ein Path-Objekt sein
xsd_schematron_dir = (
    validator_root / "schematron" / version_path
)  # Pfade korrekt zusammensetzen

# Haupt-XSD und Schematron-Datei korrekt referenzieren
zugferd_schema_extended_file = schema_path_extended / schema_extended_file
zugferd_schematron_extended_file = xsd_schematron_dir / schematron_extended_file

# Beispielaufruf mit den Pfaden zu deinen Dateien
# xml_file = root_dir / "tests/xml" / "comfort_zugferd.xml"
xml_file = root_dir / "tests/xml/zugferd" / "extended.xml"
schema_file = zugferd_schema_extended_file  # XSD-Pfad
schematron_file = zugferd_schematron_extended_file  # Schematron-Pfad

# Ausgabe der Pfade zum Debuggen
print(f"Extended XSD schema: {schema_file}")
print(f"Extended Schematron: {schematron_file}")
print(f"xml file  {str(xml_file)}")

# Führe XSD-Validierung durch
validate_xml_with_xsd(xml_file, schema_file)

# Führe Schematron-Validierung durch
validate_xml_with_schematron(xml_file, schematron_file)
