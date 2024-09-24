# model/user.py
from model.database import db
from peewee import Model, PrimaryKeyField, CharField, BigIntegerField, fn


class User(Model):
    User_ID = PrimaryKeyField()  # Primary Key
    UserLogin = CharField(null=True)
    UserPassword = CharField(null=True)
    Company_ID = BigIntegerField(null=True)

    class Meta:
        database = db  # Verbindet das Modell mit der Datenbank
        db_table = "User"

    @classmethod
    def get_next_user_id(cls):
        # Rohe SQL-Abfrage, um die nächste verfügbare User_ID zu ermitteln
        query = cls.select(fn.MAX(cls.User_ID) + 1).scalar()
        return (
            query if query is not None else 1
        )  # Fängt den Fall ab, wenn keine Datensätze existieren

    @classmethod
    def check_user_exists(cls, username: str) -> bool:
        """Prüft, ob ein Benutzer mit dem gegebenen Benutzernamen existiert."""
        user_exists = cls.select().where(cls.UserLogin == username.lower()).exists()
        return user_exists
