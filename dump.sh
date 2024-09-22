#!/bin/bash

set -x  # Aktiviert das Debugging

# Variablen für die Verbindung
DB_NAME="spielwiese"
DB_USER="root"
DUMP_FILE="spielwiese_dump.sql"

# Dump der Tabellenstruktur ohne Inhalte erstellen und Passwortaufforderung aktivieren
PGPASSWORD="dev" pg_dump -h localhost -U $DB_USER -s -d $DB_NAME > $DUMP_FILE

# Überprüfen, ob der Dump erfolgreich war
if [ $? -eq 0 ]; then
    echo "Dump der Tabellenstruktur wurde erfolgreich erstellt: $DUMP_FILE"
else
    echo "Fehler beim Erstellen des Dumps. Überprüfe Benutzername, Passwort und Datenbankname."
fi
