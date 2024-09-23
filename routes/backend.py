# backend/backend.py
import logging
from flask import Blueprint, jsonify, request
from model.database import db
from model.user import User

be = Blueprint("backend", __name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@be.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    confirm_password = data.get("confirmPassword")

    if not username or not password or password != confirm_password:
        return jsonify({"error": "Invalid data"}), 400

    existing_user = User.query.filter_by(UserLogin=username).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201
