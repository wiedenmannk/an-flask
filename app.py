import random
import logging
from flask import Flask, jsonify, request
import pikepdf
from lxml import etree
from routes.routes import bp as zugferd_route  # Korrekte Importstruktur
from routes.validator import vbp as validator_route
from routes.backend import be as backend_route
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from model.database import db  # Importiere db

app = Flask(__name__)

# Datenbank-Konfiguration
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://agentsmith:dev@localhost:5432/spielwiese"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True  # Zeigt SQL Statements direkt in der Konsole

# Initialisiere SQLAlchemy
db.init_app(app)  # Behalte dies für die DB-Initialisierung, aber entferne Migrate


# Konfiguriere das Logging nur für die Konsole
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logging.getLogger("sqlalchemy.engine").setLevel(
    logging.INFO
)  # Oder logging.DEBUG für mehr Details


def generate_random_number():
    return random.randint(1, 1000)


@app.route("/api/data", methods=["GET"])
def get_data():
    random_number = generate_random_number()
    text = f"Hello from Flask {random_number}"
    data = {"message": text}

    app.logger.info("GET /api/data - Response: %s", data)

    return jsonify(data)


@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    products = {
        1: {
            "id": 1,
            "name": "Product 1",
            "description": "Description of Product 1",
            "serial": generate_random_number(),
        },
        2: {
            "id": 2,
            "name": "Product 2",
            "description": "Description of Product 2",
            "serial": generate_random_number(),
        },
    }
    product = products.get(product_id)

    if product:
        app.logger.info("GET /api/product/%d - Response: %s", product_id, product)
        return jsonify(product)
    else:
        error_message = {"error": "Product not found"}
        app.logger.info("GET /api/product/%d - Response: %s", product_id, error_message)
        return jsonify(error_message), 404


# Registriere die Routen
app.register_blueprint(zugferd_route)  # Hier registrierst du den Blueprint direkt
app.register_blueprint(validator_route)  # Hier registrierst du den Blueprint direkt
app.register_blueprint(backend_route)

if __name__ == "__main__":
    app.run(debug=True)
