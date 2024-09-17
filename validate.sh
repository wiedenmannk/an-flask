#!/bin/bash

# Verzeichnis, in dem das JAR-File liegt
CLI_DIR="cli"

# Überprüfen, ob die richtige Anzahl an Argumenten übergeben wurde
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <xml-file>"
    exit 1
fi

# XML-Dateipfad
XML_FILE=$1

# Überprüfen, ob die XML-Datei existiert
if [ ! -f "$XML_FILE" ]; then
    echo "File not found: $XML_FILE"
    exit 1
fi

# Mustang-CLI-Command ausführen
java -jar "$CLI_DIR/Mustang-CLI-2.14.0.jar" --no-notices --action validate --source "$XML_FILE"
