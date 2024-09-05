import fitz  # PyMuPDF
from typing import Dict
from datetime import datetime

# Funktion, um das aktuelle Datum im PDF-Format zu erhalten
def get_pdf_date_format() -> str:
    return datetime.now().strftime("D:%Y%m%d%H%M%S")

# Funktion, um XML als Anhang zum PDF hinzuzufügen
def attach_xml_to_pdf(pdf_path: str, xml_content: bytes, xml_filename: str, output_pdf_path: str) -> None:
    try:
        # Öffne das PDF-Dokument
        pdf_document: fitz.Document = fitz.open(pdf_path)

        # Erstelle eine temporäre Datei für das XML, die wir anhängen werden
        with open(xml_filename, "wb") as f:
            f.write(xml_content)

        # Füge die XML-Datei als eingebettete Datei hinzu
        pdf_document._embfile_add(xml_filename, desc="ZUGFeRD XML")

        # Speichern des aktualisierten PDFs
        pdf_document.save(output_pdf_path)
        pdf_document.close()

        print(f"XML erfolgreich als Anhang hinzugefügt: {xml_filename}")

    except Exception as e:
        print(f"Fehler beim Hinzufügen des XML-Anhangs: {e}")

# Beispielnutzung der Funktion
xml_content = b"<xml>Test ZUGFeRD XML</xml>"
pdf_path = "output_test.pdf"
output_pdf_path = "pdfA3Xml.pdf"
xml_filename = "zugferd.xml"

attach_xml_to_pdf(pdf_path, xml_content, xml_filename, output_pdf_path)
