import random
import logging
from flask import Flask, jsonify, request
import pikepdf
from lxml import etree

app = Flask(__name__)

# Konfiguriere das Logging nur für die Konsole
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def generate_random_number():
    return random.randint(1, 1000)

@app.route('/api/data', methods=['GET'])
def get_data():
    random_number = generate_random_number()
    text = f'Hello from Flask {random_number}'
    data = {"message": text}
    
    app.logger.info('GET /api/data - Response: %s', data)
    
    return jsonify(data)

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    products = {
        1: { 'id': 1, 'name': 'Product 1', 'description': 'Description of Product 1', 'serial': generate_random_number() },
        2: { 'id': 2, 'name': 'Product 2', 'description': 'Description of Product 2', 'serial': generate_random_number() },
    }
    product = products.get(product_id)
    
    if product:
        app.logger.info('GET /api/product/%d - Response: %s', product_id, product)
        return jsonify(product)
    else:
        error_message = {'error': 'Product not found'}
        app.logger.info('GET /api/product/%d - Response: %s', product_id, error_message)
        return jsonify(error_message), 404

@app.route('/api/generate-zugferd', methods=['POST'])
def generate_zugferd_pdf():
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type"}), 415

    try:
        data = request.json
        app.logger.info('POST /api/generate-zugferd - Request Data: %s', data)

        pdf_path = data.get('pdf_path')
        xml_content = data.get('xml_content')

        if not pdf_path or not xml_content:
            return jsonify({"error": "Missing pdf_path or xml_content"}), 400
        
        pdf = pikepdf.Pdf.open(pdf_path)
        pdf.attachments['ZUGFeRD-invoice.xml'] = pikepdf.EmbeddedFile(xml_content.encode(), name='ZUGFeRD-invoice.xml')
        output_path = pdf_path.replace(".pdf", "_zugferd.pdf")
        pdf.save(output_path, pdf_a_mode=pikepdf.PdfAFormat.PDF_A_3B)
        
        app.logger.info('POST /api/generate-zugferd - Response: %s', {"message": "ZUGFeRD PDF created successfully", "path": output_path})
        return jsonify({"message": "ZUGFeRD PDF created successfully", "path": output_path}), 200

    except Exception as e:
        app.logger.error('POST /api/generate-zugferd - Error: %s', str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
