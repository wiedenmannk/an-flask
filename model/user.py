# model/user.py
from model.database import db


class User(db.Model):
    __tablename__ = (
        '"User"'  # Tabelle im Schema "public" mit exakter Groß- und Kleinschreibung
    )
    # __table_args__ = {"schema": "public"}  # Schema angeben, falls benötigt

    id = db.Column(
        '"User_ID"', db.Integer, primary_key=True
    )  # Exakte Spaltenbezeichnung mit Anführungszeichen
    username = db.Column('"UserLogin"', db.String(255), unique=True, nullable=False)
    password = db.Column('"UserPassword"', db.String(255), nullable=False)

    def __init__(self, username, password):
        self.username = username.lower()  # Speichere als Kleinbuchstaben
        self.password = password

    def get_username(self):
        return self.username.lower()  # Gibt immer Kleinbuchstaben zurück
