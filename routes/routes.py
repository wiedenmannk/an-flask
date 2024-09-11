import base64
import io
import logging
from typing import Dict, Any
from flask import Blueprint, jsonify, request
import fitz  # PyMuPDF
import psutil
import sys
import os
from pathlib import Path


# Füge das Projekt-Root-Verzeichnis zu sys.path hinzu
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from service.pdf_maker import PDFMaker
from service.zugferd_xml_generator import ZugferdXmlGenerator

bp = Blueprint("zugferd", __name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Setze die Log-Ebene auf DEBUG


# TODO entferne das generieren des XML Contents und schaue erst mal ob das PDF generiert wird.
# TODO umbau dieser Routen /api/save-pdf-and-xml und /api/generate-zugferd. Fraglich ob beide Routen noch gebraucht werden
@bp.route("/api/generate-zugferd", methods=["POST"])
def generate_zugferd_pdf() -> Any:
    logger.info("Call api/zugferd")
    if request.content_type != "application/json":
        logger.error("Unsupported Media Type")
        return jsonify({"error": "Unsupported Media Type"}), 415
    try:
        logger.info("get Data")
        data: Dict[str, str] = request.json

        # Pfade definieren
        output_dir = "output"
        # pdf_path = root_dir / "files" / "test.pdf"
        xml_filepath = root_dir / output_dir / "zugferd_api.xml"
        output_pdf_path = root_dir / output_dir / "zugferd_api.pdf"
        pdf_file = root_dir / output_dir / "raw_invoice.pdf"

        print(f"XML Path: {xml_filepath}")
        print(f"Output PDF Path: {output_pdf_path}")
        print(f"Raw pdf file: {pdf_file}")

        # Stelle sicher, dass der "generated" Ordner existiert
        os.makedirs(root_dir / output_dir, exist_ok=True)

        pdf_base64 = data.get("pdf_content")
        invoice_json = data.get("invoice")

        logger.info("data received")
        if not pdf_base64 or not invoice_json:
            errMsg = "Missing pdf_content or invoice json data"
            logger.error(errMsg)
            return jsonify({"error": errMsg}), 400

        logger.info("received pdf document")
        logger.info("try to add XML content")

        try:
            # ZUGFeRD XML-Generator erstellen und XML generieren
            xml_generator = ZugferdXmlGenerator()

            # Generiere XML und zeige als String
            xml_string = xml_generator.generate_xml_from_json(
                invoice_json, xml_filepath
            )
            logger.info(f"Generated XML String:\n{xml_string}")

        except Exception as e:
            logger.error("Failed to create XML File: %s", str(e))
            return jsonify({"error": "Failed to create XML File"}), 500

        try:
            logger.info("save base64 to pdf")
            # PDFMaker erstellen und XML an PDF anhängen
            pdf_maker = PDFMaker()
            pdf = pdf_maker.process_base64_pdf(pdf_base64)
            pdf.save(pdf_file)
            if pdf is not None:
                pdf_maker.attach_xml(
                    str(xml_filepath), "zugferd.xml", str(output_pdf_path), pdf
                )
                logger.info(f"PDF with XML attached saved to: {output_pdf_path}")

        except Exception as e:
            errMsg = "Failed to save pdf"
            pdf.close()
            logger.error("{errMsg}: %s", str(e))
            return jsonify({"error": errMsg}), 500

        # Überprüfe den Speicherverbrauch
        process = psutil.Process()
        logger.info(
            "Memory usage after PDF generation: %f MB",
            process.memory_info().rss / (1024 * 1024),
        )

        logger.info("ZUGFeRD PDF created successfully: %s", output_pdf_path)
        return (
            jsonify(
                {"message": "ZUGFeRD PDF created successfully", "path": output_pdf_path}
            ),
            200,
        )

    except Exception as e:
        logger.error("Error processing request: %s", str(e))
        return jsonify({"error": str(e)}), 500


@bp.route("/api/save-pdf-and-xml", methods=["POST"])
def save_pdf_and_xml() -> Any:
    logger.info("Call api/save-pdf-and-xml")
    if request.content_type != "application/json":
        logger.error("Unsupported Media Type")
        return jsonify({"error": "Unsupported Media Type"}), 415

    try:
        data = request.json
        pdf_base64 = data.get("pdf_content")
        xml_content = data.get("xml_content")

        if not pdf_base64 or not xml_content:
            logger.error("Missing pdf_content or xml_content")
            return jsonify({"error": "Missing pdf_content or xml_content"}), 400

        # Decode and save PDF
        pdf_data = base64.b64decode(pdf_base64)
        pdf_output_path = "output_test.pdf"
        with open(pdf_output_path, "wb") as pdf_file:
            pdf_file.write(pdf_data)
        logger.info("PDF saved as %s", pdf_output_path)

        # Save XML
        xml_output_path = "output_test.xml"
        with open(xml_output_path, "w", encoding="utf-8") as xml_file:
            xml_file.write(xml_content)
        logger.info("XML saved as %s", xml_output_path)

        return jsonify({"message": "PDF and XML saved successfully"}), 200

    except Exception as e:
        logger.error("Error processing request: %s", str(e))
        return jsonify({"error": str(e)}), 500
