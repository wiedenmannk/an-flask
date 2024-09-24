from playhouse.postgres_ext import PostgresqlExtDatabase

# Datenbankverbindung
db = PostgresqlExtDatabase(
    "spielwiese",
    user="agentsmith",
    password="dev",
    host="localhost",
    port=5432,
)
