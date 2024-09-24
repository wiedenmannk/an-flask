from peewee import Model
from playhouse.postgres_ext import PostgresqlExtDatabase
from typing import Callable, Any


# ok ich habe die Klasse geschrieben nur um festzustellen das sie overpowered ist un keinen Mehrwert bringt
class DbRunner:
    def __init__(self, database):
        """Initialisiert DbRunner mit einer Datenbankinstanz."""
        self.database: PostgresqlExtDatabase = database

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
