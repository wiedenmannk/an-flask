import random
import logging
from flask import Flask, jsonify

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
    
    # Logge den API-Call
    app.logger.info('GET /api/data - Response: %s', data)
    
    return jsonify(data)

@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    products = {
        1: { 'id': 1, 'name': 'Product 1', 'description': 'Description of Product 1', 'serial': generate_random_number() },
        2: { 'id': 2, 'name': 'Product 2', 'description': 'Description of Product 2', 'serial': generate_random_number() },
        # Weitere Produkte können hier hinzugefügt werden
    }
    product = products.get(product_id)
    
    if product:
        # Logge den API-Call und die Produktdaten
        app.logger.info('GET /api/product/%d - Response: %s', product_id, product)
        return jsonify(product)
    else:
        error_message = {'error': 'Product not found'}
        # Logge den API-Call und den Fehler
        app.logger.info('GET /api/product/%d - Response: %s', product_id, error_message)
        return jsonify(error_message), 404

if __name__ == '__main__':
    app.run(debug=True)