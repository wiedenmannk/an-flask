#!/bin/bash

echo "Starte Saxon"

# Pfade zu den Eingabedateien und zur Saxon JAR-Datei
SCHEMATRON_FILE="/home/dev/dev/python/an-flask/zugferd/Schema/EXTENDED/Schematron/FACTUR-X_EXTENDED.sch"
OUTPUT_XSLT="/home/dev/dev/python/an-flask/zugferd/Schema/EXTENDED/FACTUR-X_EXTENDED.xsl"
XML_FILE="/home/dev/dev/python/an-flask/tests/xml/zugferd/extended.xml"
SAXON_JAR="/home/dev/dev/java/SaxonEE12-5J/saxon-ee-12.5.jar"

# Wandelt die Schematron-Datei in eine XSLT-Datei um
echo "java -jar \"$SAXON_JAR\" -s:\"$SCHEMATRON_FILE\" -xsl:\"$OUTPUT_XSLT\""
java -jar "$SAXON_JAR" -s:"$SCHEMATRON_FILE" -xsl:"$OUTPUT_XSLT" 2>&1 | tee conversion.log

# Überprüft die Umwandlung
if [ $? -ne 0 ]; then
  echo "Fehler bei der Umwandlung der Schematron-Datei in XSLT."
  exit 1
fi

# Führt die XSLT-Transformation durch
echo "java -jar \"$SAXON_JAR\" -s:\"$XML_FILE\" -xsl:\"$OUTPUT_XSLT\""
java -jar "$SAXON_JAR" -s:"$XML_FILE" -xsl:"$OUTPUT_XSLT" 2>&1 | tee transformation.log

# Überprüft die Transformation
if [ $? -ne 0 ]; then
  echo "Fehler bei der XSLT-Transformation."
  exit 1
fi

echo "Die Schematron-Validierung war erfolgreich."
