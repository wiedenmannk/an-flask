# backend/backend.py
import logging
from flask import Blueprint, jsonify, request
from model.database import db
from sqlalchemy import text
from model.user import User

be = Blueprint("backend", __name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@be.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    confirm_password = data.get("confirmPassword")

    if not username or not password or password != confirm_password:
        return jsonify({"error": "Invalid data"}), 400

    existing_user = User.query.filter_by(
        UserLogin=username
    ).first()  # Behalte die Großschreibung bei
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@be.route("/api/test", methods=["GET"])
def test_query():
    try:
        # Öffne eine Verbindung zur Datenbank
        with db.engine.connect() as connection:
            # Verwende text() um den SQL-Befehl auszuführen
            result = connection.execute(text('SELECT * FROM "User" LIMIT 1'))

            # Verarbeite das Ergebnis mit mappings()
            rows = [
                dict(row) for row in result.mappings()
            ]  # Hier wird die mappings-Methode verwendet
            print(rows)  # Optional: für Debugging

        return jsonify({"status": "Query executed", "data": rows}), 200

    except Exception as e:
        # Fehlerbehandlung
        print(f"Error executing query: {e}")
        return jsonify({"error": str(e)}), 500
