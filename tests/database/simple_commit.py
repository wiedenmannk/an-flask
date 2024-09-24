from peewee import Model, CharField, PrimaryKeyField
from playhouse.postgres_ext import PostgresqlExtDatabase

# Globale Datenbankverbindung erstellen
db = PostgresqlExtDatabase(
    "spielwiese",
    user="agentsmith",
    password="dev",
    host="localhost",
    port=5432,
)


class User(Model):
    User_ID = PrimaryKeyField()
    UserLogin = CharField(max_length=255)
    UserPassword = CharField(max_length=255)

    class Meta:
        database = db
        db_table = "User"


# Funktion zum Erstellen eines Benutzers
def create_user(user_login, user_password, user_id):
    try:
        with db.atomic():  # Beginne eine Transaktion
            user = User.create(
                UserLogin=user_login, UserPassword=user_password, User_ID=user_id
            )
            print("User erfolgreich erstellt:", user.UserLogin)
    except Exception as e:
        print(f"Fehler beim Erstellen des Benutzers: {e}")


# Verbindung zur Datenbank öffnen
db.connect()

# Benutzer erstellen
create_user("testuser", "testpassword", 5558)

# Überprüfen, ob der Benutzer in der Datenbank existiert
print("Aktuelle Benutzer in der Datenbank:")
for user in User.select():
    print(f"User_ID: {user.User_ID}, UserLogin: {user.UserLogin}")

# Verbindung schließen
db.close()
