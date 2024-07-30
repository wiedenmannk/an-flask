import random
from flask import Flask, jsonify

app = Flask(__name__)

def generate_random_number():
    return random.randint(1, 1000)

@app.route('/api/data', methods=['GET'])
def get_data():
    random_number = generate_random_number()
    text = f'Hello from Flask {random_number}'
    data = {"message": text}
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
        return jsonify(product)
    else:
        return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
