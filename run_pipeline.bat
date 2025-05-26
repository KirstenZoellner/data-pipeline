@echo off
:: ----------------------------
:: Batch-Datei zum Starten der Data Pipeline
:: Diese Datei ruft zwei Docker-Container nacheinander auf:
:: 1. ingestion - lädt Daten von Kaggle
:: 2. spark     - verarbeitet und speichert die Daten
:: ----------------------------

:: Wechsle ins Projektverzeichnis
cd "C:\Users\kirst\Desktop\IT\IU\Projekt Data Engineering\data-pipeline"

:: Starte den Ingestion-Service (CSV-Download via Kaggle API)
docker-compose run --rm ingestion

:: Starte den Spark-Verarbeitungsprozess
docker-compose run --rm spark

:: Hinweis: Beide Container werden nach Ausführung automatisch wieder entfernt (--rm)
