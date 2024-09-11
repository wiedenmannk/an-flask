import os
import sys
from pathlib import Path

# Füge das Projekt-Root-Verzeichnis zu sys.path hinzu
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from service.pdf_maker import PDFMaker
from service.zugferd_xml_generator import ZugferdXmlGenerator


# Globale Variable für das Root-Verzeichnis
def test_pdf_processing():
    print(f"Root directory: {root_dir}")

    # Pfade definieren
    output_path = "output"
    pdf_path = root_dir / "files" / "test.pdf"
    base64_pdf_path = root_dir / "files" / "pdf_base64.txt"
    xml_filepath = root_dir / output_path / "zugferd.xml"
    output_pdf_path = root_dir / output_path / "output_with_xml.pdf"

    print(f"PDF Path: {pdf_path}")
    print(f"Base64 PDF Path: {base64_pdf_path}")
    print(f"XML Path: {xml_filepath}")
    print(f"Output PDF Path: {output_pdf_path}")

    # Stelle sicher, dass der "generated" Ordner existiert
    os.makedirs(root_dir / "generated", exist_ok=True)

    # Beispielhafte JSON-Daten für ZUGFeRD
    json_data = {
        "name": "Klaus",
        "lastName": "Wiedenmann",
        "summary": "10000",
        "bill": {"no": "1", "date": "2024-09-01"},
    }

    # ZUGFeRD XML-Generator erstellen und XML generieren
    xml_generator = ZugferdXmlGenerator()

    # Generiere XML und zeige als String
    xml_string = xml_generator.generate_xml_from_json(json_data)
    print(f"Generated XML String:\n{xml_string}")

    # Schreibe XML in eine Datei
    xml_generator.write_xml(xml_string, xml_filepath)
    print(f"XML written to: {xml_filepath}")

    # Base64-kodiertes PDF aus der Datei lesen
    with open(base64_pdf_path, "r") as file:
        base64_pdf = file.read()

    # PDFMaker erstellen und XML an PDF anhängen
    pdf_maker = PDFMaker()
    pdf = pdf_maker.process_base64_pdf(base64_pdf)
    if pdf is not None:
        pdf_maker.attach_xml(
            str(xml_filepath), "zugferd.xml", str(output_pdf_path), pdf
        )
        print(f"PDF with XML attached saved to: {output_pdf_path}")


# Test ausführen
if __name__ == "__main__":
    test_pdf_processing()
