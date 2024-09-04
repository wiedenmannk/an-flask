import base64
import io
import logging
from flask import Blueprint, jsonify, request
import pikepdf

bp = Blueprint('zugferd', __name__)

# Erstelle einen Logger für dieses Modul
logger = logging.getLogger(__name__)

@bp.route('/api/generate-zugferd', methods=['POST'])
def generate_zugferd_pdf():
    logger.info("call api/zugferd")
    if request.content_type != 'application/json':
        logger.error('Unsupported Media Type')
        return jsonify({"error": "Unsupported Media Type"}), 415

    try:
        data = request.json
        logger.info('Received data: %s', data)

        pdf_base64 = data.get('pdf_content')
        xml_content = data.get('xml_content')

        if not pdf_base64 or not xml_content:
            logger.error('Missing pdf_content or xml_content')
            return jsonify({"error": "Missing pdf_content or xml_content"}), 400

        pdf_data = base64.b64decode(pdf_base64)
        pdf = pikepdf.Pdf.open(io.BytesIO(pdf_data))
        pdf.attachments['ZUGFeRD-invoice.xml'] = pikepdf.EmbeddedFile(xml_content.encode(), name='ZUGFeRD-invoice.xml')
        output_path = "output_zugferd.pdf"
        pdf.save(output_path, pdf_a_mode=pikepdf.PdfAFormat.PDF_A_3B)

        logger.info('ZUGFeRD PDF created successfully: %s', output_path)
        return jsonify({"message": "ZUGFeRD PDF created successfully", "path": output_path}), 200

    except Exception as e:
        logger.error('Error processing request: %s', str(e))
        return jsonify({"error": str(e)}), 500
