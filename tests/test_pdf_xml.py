import os
from pathlib import os
from pathlib import Path
from service.pdf_maker import PDFMaker
from service.zugferd_xml_generator import ZugferdXmlGenerator

# Globale Variable für das Root-Verzeichnis
root_dir = Path(__file__).parent.parent

def test_pdf_processing():
    print(f"Root directory: {root_dir}")

    # Pfade definieren
    pdf_path = root_dir / "files" / "test.pdf"
    xml_filepath = root_dir / "generated" / "zugferd.xml"
    output_pdf_path = root_dir / "generated" / "output_with_xml.pdf"

    print(f"PDF Path: {pdf_path}")
    print(f"XML Path: {xml_filepath}")
    print(f"Output PDF Path: {output_pdf_path}")

    # Stelle sicher, dass der "generated" Ordner existiert
    os.makedirs(root_dir / "generated", exist_ok=True)

    # Beispielhafte JSON-Daten für ZUGFeRD
    json_data = {
        "InvoiceNumber": "12345",
        "InvoiceDate": "2024-09-06",
        "Amount": "100.00"
    }

    # ZUGFeRD XML-Generator erstellen und XML generieren
    xml_generator = ZugferdXmlGenerator()

    # Generiere XML und zeige als String
    xml_string = xml_generator.generate_xml_from_json(json_data, xml_filepath)
    print(f"Generated XML String:\n{xml_string}")

    # PDFMaker erstellen und XML an PDF anhängen
    pdf_maker = PDFMaker()
    pdf = pdf_maker.process_base64_pdf("JVBERi0xLjcKJc...")  # Ersetze dies durch echten Base64-Daten oder lade PDF direkt
    if pdf is not None:
        pdf_maker.attach_xml(str(xml_filepath), "zugferd.xml", str(output_pdf_path), pdf)
        print(f"PDF with XML attached saved to: {output_pdf_path}")

# Test ausführen
if __name__ == "__main__":
    test_pdf_processing()
