import base64
import io
import logging
from typing import Dict, Any
from flask import Blueprint, jsonify, request
import fitz  # PyMuPDF
import psutil

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

        pdf_base64 = data.get("pdf_content")
        xml_content = data.get("xml_content")

        logger.info("data received")
        if not pdf_base64 or not xml_content:
            logger.error("Missing pdf_content or xml_content")
            return jsonify({"error": "Missing pdf_content or xml_content"}), 400

        logger.info("try to create data")
        pdf_data = base64.b64decode(pdf_base64)
        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")

        logger.info("received pdf document")
        logger.info("try to add XML content to PDF")

        try:
            xref = pdf_document._embfile_add(
                name="ZUGFeRD-invoice.xml",
                buffer_=io.BytesIO(xml_content.encode()),
                filename="ZUGFeRD-invoice.xml",
            )
            logger.info("XML added to PDF, xref: %d", xref)
        except Exception as e:
            logger.error("Failed to add XML content to PDF: %s", str(e))
            pdf_document.close()
            return jsonify({"error": "Failed to add XML content"}), 500

        output_path = "output_zugferd.pdf"
        logger.info("Saving PDF to %s", output_path)
        pdf_document.save(output_path, garbage=4, deflate=True)
        pdf_document.close()

        # Überprüfe den Speicherverbrauch
        process = psutil.Process()
        logger.info(
            "Memory usage after PDF generation: %f MB",
            process.memory_info().rss / (1024 * 1024),
        )

        logger.info("ZUGFeRD PDF created successfully: %s", output_path)
        return (
            jsonify(
                {"message": "ZUGFeRD PDF created successfully", "path": output_path}
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
