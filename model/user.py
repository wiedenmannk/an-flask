# backend/model.py
# model/user.py
from model.database import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column("user_id", db.Integer, primary_key=True)
    username = db.Column("userlogin", db.String(255), unique=True, nullable=False)
    password = db.Column("userpassword", db.String(255), nullable=False)

    def __init__(self, username, password):
        self.username = username.lower()  # Speichere als Kleinbuchstaben
        self.password = password

    def get_username(self):
        return self.username.lower()  # Gibt immer Kleinbuchstaben zurück
