from flask import Flask, request, jsonify
import pikepdf
from lxml import etree

app = Flask(__name__)

@app.route('/api/generate-zugferd', methods=['POST'])
def generate_zugferd_pdf():
    pdf_path = request.json.get('pdf_path')
    xml_content = request.json.get('xml_content')
    
    try:
        pdf = pikepdf.Pdf.open(pdf_path)
        pdf.attachments['ZUGFeRD-invoice.xml'] = pikepdf.EmbeddedFile(xml_content.encode(), name='ZUGFeRD-invoice.xml')
        output_path = pdf_path.replace(".pdf", "_zugferd.pdf")
        pdf.save(output_path, pdf_a_mode=pikepdf.PdfAFormat.PDF_A_3B)
        return jsonify({"message": "ZUGFeRD PDF created successfully", "path": output_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
