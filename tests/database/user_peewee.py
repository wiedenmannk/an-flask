from peewee import *
import psycopg2

# Verbinde dich mit deiner PostgreSQL-Datenbank
db = PostgresqlDatabase(
    "spielwiese",  # Name der Datenbank
    user="agentsmith",  # Benutzername
    password="dev",  # Passwort
    host="localhost",  # Hostname, wenn lokal
    port=5432,  # Standardport für PostgreSQL
)


# Definiere das Modell für die Tabelle "User", beachte die Groß- und Kleinschreibung
class User(Model):
    User_ID = BigIntegerField(primary_key=True)
    UserLogin = CharField()
    UserPassword = CharField()
    Company_ID = BigIntegerField()

    class Meta:
        database = db
        table_name = "User"  # Beachte die Großschreibung der Tabelle
        schema = "public"  # Schema 'public' in PostgreSQL


# Verbinde dich mit der Datenbank
db.connect()

# Einfügen eines neuen Datensatzes in die Tabelle "User"
new_user = User.create(
    User_ID=1001, UserLogin="testuser", UserPassword="password123", Company_ID=500
)

# Abrufen aller Datensätze aus der Tabelle "User"
users = User.select()
for user in users:
    print(
        f"User_ID: {user.User_ID}, UserLogin: {user.UserLogin}, UserPassword: {user.UserPassword}, Company_ID: {user.Company_ID}"
    )

# Verbindung trennen
db.close()
