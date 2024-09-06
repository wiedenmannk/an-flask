import base64
from io import BytesIO
from pikepdf import Pdf, AttachedFileSpec
from pathlib import Path
import xml.etree.ElementTree as ET

class PDFMaker:
    def __init__(self):
        pass

    def attach_xml(self, xml_filepath: str, xml_filename: str, output_pdf_path: str, pdf: Pdf) -> None:
        """
        Nimmt den Pfad einer XML-Datei und hängt diese als Anhang an das PDF an.
        """
        try:
            # Erstelle AttachedFileSpec für das XML von der Festplatte
            filespec = AttachedFileSpec.from_filepath(pdf, Path(xml_filepath))
            
            # Füge die XML-Datei als Anhang hinzu
            pdf.attachments[xml_filename] = filespec

            # Speichere das neue PDF mit dem Anhang
            pdf.save(output_pdf_path)
            print(f"XML erfolgreich als Anhang hinzugefügt: {xml_filename}")

        except Exception as e:
            print(f"Fehler beim Hinzufügen des XML-Anhangs: {e}")
        
        finally:
            pdf.close()

    def process_base64_pdf(self, base64_pdf: str) -> Pdf:
        """
        Decodiert ein PDF im Base64-Format und öffnet es als PikePDF-Objekt.
        """
        try:
            # Base64-Daten decodieren
            pdf_data = base64.b64decode(base64_pdf)
            pdf = Pdf.open(BytesIO(pdf_data))
            return pdf

        except Exception as e:
            print(f"Fehler beim Verarbeiten des Base64-PDF: {e}")
            return None

    @staticmethod
    def generate_xml(xml_filepath: str) -> None:
        """
        Generiert ein einfaches XML-Dokument und speichert es auf der Festplatte.
        """
        root = ET.Element("Invoice")
        child = ET.SubElement(root, "Item")
        child.text = "Test ZUGFeRD XML"
        
        # Speichere das XML als Datei
        tree = ET.ElementTree(root)
        tree.write(xml_filepath, encoding='utf-8', xml_declaration=True)
        print(f"XML-Datei erfolgreich gespeichert: {xml_filepath}")

# Beispielnutzung der Klasse
if __name__ == "__main__":
    pdf_maker = PDFMaker()

    # Beispiel: XML-Datei generieren und speichern
    xml_filepath = "zugferd.xml"
    pdf_maker.generate_xml(xml_filepath)

    # Beispiel Base64-String eines PDFs (dieser muss ersetzt werden durch echte Base64-Daten)
    base64_pdf = "JVBERi0xLjcKJc..."

    # Base64-PDF verarbeiten
    pdf = pdf_maker.process_base64_pdf(base64_pdf)

    if pdf is not None:
        # XML an das PDF anhängen
        output_pdf_path = "output_with_xml.pdf"
        pdf_maker.attach_xml(xml_filepath, "zugferd.xml", output_pdf_path, pdf)
