from peewee import Model, PrimaryKeyField, CharField, BigIntegerField, DoesNotExist
from typing import Callable, Any
from playhouse.postgres_ext import PostgresqlExtDatabase

# Datenbankverbindung
db = PostgresqlExtDatabase(
    "spielwiese",
    user="agentsmith",
    password="dev",
    host="localhost",
    port=5432,
)


class User(Model):
    User_ID = PrimaryKeyField()  # Primary Key
    UserLogin = CharField(null=True)
    UserPassword = CharField(null=True)
    Company_ID = BigIntegerField(null=True)

    class Meta:
        database = db  # Verbindet das Modell mit der Datenbank
        db_table = "User"  # Definiert den Tabellennamen mit Anführungszeichen


class DbRunner:
    def __init__(self, database):
        """Initialisiert DbRunner mit einer Datenbankinstanz."""
        self.database = database

    def create_record(self, model_class: Model, **data):
        """Erstellt einen neuen Datensatz in einem angegebenen Modell."""
        return model_class.create(**data)

    def execute_transaction(self, action: Callable[[], Any]) -> Any:
        """Führt die gegebene Aktion innerhalb einer Transaktion aus."""
        try:
            with self.database.atomic():  # Peewee kümmert sich um commit/rollback
                return action()  # Führt die Aktion aus
        except Exception as e:
            print(f"Fehler während der Transaktion: {e}")
            raise  # Ausnahme weitergeben


# Beispiel für einfachen SELECT
def check_existing_users():
    try:
        users = User.select()  # Ruft alle User-Datensätze ab
        if users.exists():  # Überprüft, ob Datensätze vorhanden sind
            print("Vorhandene Benutzer:")
            for user in users:
                print(
                    f"ID: {user.User_ID}, Login: {user.UserLogin}, Company_ID: {user.Company_ID}"
                )
        else:
            print("Keine Benutzer gefunden.")
    except Exception as e:
        print(f"Fehler beim Abrufen der Benutzer: {e}")


# Beispiel einer Testfunktion
def test_db_runner():
    db_runner = DbRunner(db)
    user_id = 1020
    user_params = {
        "User_ID": user_id,
        "UserLogin": "testuser",
        "UserPassword": "testpass",
        "Company_ID": 802,
    }

    # Vor dem Erstellen prüfen, ob Benutzer existieren
    check_existing_users()

    try:
        new_user = db_runner.execute_transaction(
            lambda: db_runner.create_record(User, **user_params)
        )
        print("Benutzer erfolgreich erstellt:", new_user.User_ID)
    except Exception as e:
        print(f"Fehler beim Erstellen des Benutzers: {e}")

    try:
        user = User.get(User.User_ID == user_id)
        print(f"Benutzer gefunden: {user.UserLogin}")
    except DoesNotExist:
        print("Benutzer nicht gefunden.")

    # Nach dem Erstellen prüfen, ob Benutzer existieren
    check_existing_users()


# Verbindung zur Datenbank herstellen
try:
    db.connect()
    test_db_runner()  # Test durchführen
finally:
    db.close()
