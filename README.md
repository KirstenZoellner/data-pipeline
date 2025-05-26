## Data-Pipeline: Korrelation zwischen Bitcoin und Börsen

## Projektbeschreibung

Dieses Projekt analysiert die Korrelation zwischen Kryptowährungen (insbesondere Bitcoin) und traditionellen Börsenindizes wie dem Dow Jones Industrial Average (DJIA). Die Daten stammen von der Plattform Kaggle und enthalten über 1 Million Datenpunkte, die täglich bzw. minütlich aktualisiert werden.

Ziel ist es, mithilfe moderner Big-Data-Technologien aussagekräftige Analysen über mögliche Zusammenhänge zwischen traditionellen und digitalen Finanzmärkten durchzuführen.

Projektstruktur

'''text

data-pipeline/
├── data/
│   ├── raw/
│   │   ├── bitcoin/
│   │   │   └── btcusd_1-min_data.csv
│   │   └── djia/
│   │       ├── dow_jones_data.csv
│   │       └── djia_clean.csv
│   └── processed/
│       └── combined_daily_and_summary.csv
├── images/
│   ├── correlation_btc_close.png
│   └── correlation_djia_close.png
├── ingestion/
│   └── kaggle/
│       ├── kaggle.json (nicht im Git enthalten)
│       └── Dockerfile
├── spark/
│   ├── process.py
│   └── Dockerfile
├── mysql/
│   └── init.sql
├── elk/
│   └── logstash.conf
├── docker-compose.yml
├── run_pipeline.bat
├── requirements.txt
├── .env (nicht im Git enthalten)
├── README.md
└── .gitignore

## Technologien

Docker & Docker-Compose: Containerisierung und Orchestrierung der Microservices

Apache Spark: Verarbeitung, Aggregation und Analyse großer Datenmengen

MySQL: Persistente Speicherung der bereinigten und aggregierten Daten

ELK Stack (Elasticsearch, Logstash, Kibana): Visualisierung und Überwachung von Logs und Status

Kaggle API: Download der Rohdaten

GitHub: Versionierung und Codeverwaltung

Python dotenv: Verwaltung von Umgebungsvariablen (.env-Dateien)

## Datenpipeline-Ablauf

Datenbeschaffung:

Die historischen Daten zu Bitcoin und DJIA werden automatisch per Kaggle-API heruntergeladen.

Ingestion Service:

Die CSV-Dateien werden in ein temporäres Verzeichnis geschrieben.

Verarbeitung mit Spark:

Start über Docker Compose

Bereinigung, Aggregation und Korrelation der Daten

Speicherung in MySQL

Überwachung:

ELK-Stack visualisiert Logs und den Zustand des Systems in Echtzeit.

## Architekturprinzipien

Microservice-Architektur zur Trennung von Zuständigkeiten

Skalierbarkeit durch Spark & Docker

Sicherheit durch eingeschränkte Netzwerkbereiche und Zugang zu Services

Einhaltung von Datenschutz und Data-Governance-Prinzipien

## Datenquellen

Bitcoin Historical Data – minütlich

DJIA Historical Data – täglich

## Visualisierungen

Bitcoin Close Price Correlation

![Correlation Bitcoin](images/correlation_btc_close.png)

DJIA Close Price Correlation

![Correlation DJIA](images/correlation_djia_close.png)

## Manuelle Ausführung beim ersten Start (Windows)

Stelle sicher, dass Docker Desktop gestartet ist.

Navigiere im Explorer zum Projektverzeichnis.

Führe die Datei run_pipeline.bat per Doppelklick aus.

Alternativ im Terminal:

cd "Pfad\zum\Projektordner"
run_pipeline.bat

Installiere benötigte Python-Bibliotheken:

pip install -r requirements.txt

Erstelle eine .env Datei mit folgenden Einträgen (Beispiel):

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=geheim
DB_NAME=finance

Lade deine kaggle.json von deinem Kaggle-Konto herunter und speichere sie unter:

ingestion/kaggle/kaggle.json

Nach erfolgreicher Ausführung findest du die Ausgabedateien unter data/processed/.

## Automatisierte Ausführung mit dem Windows Task Scheduler

Die Pipeline kann einmal pro Quartal automatisch ausgeführt werden. Dazu eignet sich die Windows-Aufgabenplanung.

## Schritt-für-Schritt Anleitung:

Taskplaner öffnen:

Suche im Startmenü nach "Aufgabenplanung" oder "Task Scheduler".

Neue Aufgabe erstellen:

Klicke auf "Aufgabe erstellen..." (nicht "Einfache Aufgabe").

Registerkarte Allgemein:

Name: Data Pipeline Quarterly

Haken bei "Mit höchsten Privilegien ausführen" setzen

Trigger:

Neu → Zeitplan: "Monatlich"

Wähle z. B. Januar, April, Juli, Oktober

Tag: z. B. 1., Uhrzeit: 10:00

Aktionen:

Neu → "Programm starten"

Programm/Skript: C:\Pfad\zum\Projekt\run_pipeline.bat

Bedingungen & Einstellungen:

Optional: Nur bei Netzstrom oder mit Internetverbindung ausführen

Speichern und schließen
