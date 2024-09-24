# model/user.py
from model.database import db
from peewee import Model, PrimaryKeyField, CharField, BigIntegerField


class User(Model):
    User_ID = PrimaryKeyField()  # Primary Key
    UserLogin = CharField(null=True)
    UserPassword = CharField(null=True)
    Company_ID = BigIntegerField(null=True)

    class Meta:
        database = db  # Verbindet das Modell mit der Datenbank
        db_table = "User"  # Definiert den Tabellennamen mit Anführungszeichen

    @classmethod
    def check_user_exists(cls, username: str) -> bool:
        """Prüft, ob ein Benutzer mit dem gegebenen Benutzernamen existiert."""
        user_exists = cls.select().where(cls.UserLogin == username.lower()).exists()
        return user_exists
