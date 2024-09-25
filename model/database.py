"""
from playhouse.postgres_ext import PostgresqlExtDatabase

# Datenbankverbindung
db = PostgresqlExtDatabase(
    "spielwiese",
    user="agentsmith",
    password="dev",
    host="localhost",
    port=5432,
    max_connections=20,  # Anzahl der maximalen Verbindungen im Pool
    stale_timeout=300,  # Zeit, nach der eine inaktive Verbindung neu geöffnet wird
)
"""

from playhouse.pool import PooledPostgresqlExtDatabase

# Datenbankverbindung mit Connection-Pooling
db = PooledPostgresqlExtDatabase(
    "spielwiese",
    max_connections=20,  # Maximale Anzahl gleichzeitiger Verbindungen
    stale_timeout=300,  # Timeout für inaktive Verbindungen in Sekunden
    user="agentsmith",
    password="dev",
    host="localhost",
    port=5432,
)
