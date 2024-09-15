from lxml import etree
import sys
from pathlib import Path

# Füge das Projekt-Root-Verzeichnis zu sys.path hinzu
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))


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
            schematron = etree.Schematron(schematron_doc)

        # Lade das XML-Dokument
        with open(xml_file, "rb") as xml_f:
            xml_doc = etree.parse(xml_f)

        # Führe die Schematron-Validierung durch
        if schematron.validate(xml_doc):
            print("Das XML-Dokument ist Schematron-gültig.")
            return True
        else:
            print("Schematron-Validierung fehlgeschlagen.")
            print(schematron.error_log)
            return False

    except Exception as e:
        print(f"Fehler bei der Schematron-Validierung: {e}")
        return False


xsd_path = root_dir / "zugferd/Schema"
xsd_path_extended = "EXTENDED"
xsd_schematron_dir = "Schematron"
zugferd_schema_extented = (
    xsd_path_extended
    / "FACTUR-X_EXTENDED_urn_un_unece_uncefact_data_standard_QualifiedDataType_100.xsd"
)
zugferd_schematron_extended = (
    xsd_path_extended / xsd_schematron_dir / "FACTUR-X_BASIC.sch"
)

# Beispielaufruf mit den Pfaden zu deinen Dateien
xml_file = "xml/comfort_zugferd.xml"
xsd_file = xsd_path / zugferd_schema_extented  # Haupt-XSD für Extended
sch_file = xsd_path / zugferd_schematron_extended  # Schematron-Datei für Extended

print(f"extended xsd schema {xsd_file}")
print(f"extended xsd schematron {sch_file}")

# Führe XSD-Validierung durch
validate_xml_with_xsd(xml_file, xsd_file)

# Führe Schematron-Validierung durch
validate_xml_with_schematron(xml_file, sch_file)
