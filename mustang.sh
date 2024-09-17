#!/bin/bash

# Pfad zum Python-Testskript
TEST_SCRIPT_PATH="tests/test_mustang.py"

# Überprüfen, ob die Datei existiert
if [ -f "$TEST_SCRIPT_PATH" ]; then
    echo "Starte das Python-Testskript: $TEST_SCRIPT_PATH"
    
    # Python-Testskript ausführen
    python3 "$TEST_SCRIPT_PATH"
    
    # Überprüfen, ob das Skript erfolgreich ausgeführt wurde
    if [ $? -eq 0 ]; then
        echo "Das Testskript wurde erfolgreich ausgeführt."
    else
        echo "Fehler bei der Ausführung des Testskripts."
    fi
else
    echo "Das Python-Testskript wurde nicht gefunden: $TEST_SCRIPT_PATH"
fi
