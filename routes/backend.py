# backend/backend.py
import logging
from flask import Blueprint, jsonify, request
from model.database import db
from sqlalchemy import text
from model.user import User
from service.db_runner import DbRunner

be = Blueprint("backend", __name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# TODO: Sicherstellen das db als Instanz gebildet wird. Da jeweils pro Instanz ein db.connect und close gemacht werden muss
@be.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username: str = data.get("username")
    username: str = username.lower()
    password: str = data.get("password")
    confirm_password: str = data.get("confirmPassword")

    if not username or not password or password != confirm_password:
        return jsonify({"error": "Invalid data"}), 400

    try:
        db.connect()
        # prüfen, ob User bereits existiert
        user_exist = User.get(User.UserLogin == username)
        if user_exist:
            return jsonify({"error": "User already exist"}), 400

        db_runner = DbRunner(db)
        user_params = {"UserLogin": username, "UserPassword": password}
        new_user = db_runner.execute_transaction(
            lambda: db_runner.create_record(User, **user_params)
        )
        logger.info("Benutzer erfolgreich erstellt", new_user.UserLogin)

        db.close()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        # Fehler bei Anlage User
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
