
# Data-Pipeline: Korrelation zwischen Bitcoin und Börsen

## Projektbeschreibung

Dieses Projekt analysiert die Korrelation zwischen der Kryptowährung Bitcoin und traditionellen Börsenindizes wie dem Dow Jones Industrial Average (DJIA). Die Daten stammen von der Plattform [Kaggle](https://www.kaggle.com/) und enthalten über 1 Million Datenpunkte, die täglich bzw. minütlich aktualisiert werden.

Ziel ist es, mithilfe moderner Big-Data-Technologien aussagekräftige Analysen über mögliche Zusammenhänge zwischen traditionellen und digitalen Finanzmärkten durchzuführen.

---

## Projektstruktur

```text
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
```

## Technologien

- Docker & Docker-Compose: Containerisierung und Orchestrierung der Microservices
- Apache Spark: Verarbeitung, Aggregation und Analyse großer Datenmengen
- MySQL: Persistente Speicherung der bereinigten und aggregierten Daten
- ELK Stack (Elasticsearch, Logstash, Kibana): Visualisierung und Überwachung von Logs und Status
- Kaggle API: Download der Rohdaten
- GitHub: Versionierung und Codeverwaltung
- Python dotenv: Verwaltung von Umgebungsvariablen (.env-Dateien)

## Datenpipeline-Ablauf

1. **Datenbeschaffung**  
   Die historischen Daten zu Bitcoin und DJIA werden automatisch per Kaggle-API heruntergeladen.

2. **Ingestion Service**  
   Die CSV-Dateien werden in ein temporäres Verzeichnis geschrieben.

3. **Verarbeitung mit Spark**  
   - Start über Docker Compose  
   - Bereinigung, Aggregation und Korrelation der Daten  
   - Speicherung in MySQL

4. **Überwachung**  
   ELK-Stack visualisiert Logs und den Zustand des Systems in Echtzeit.

## Architekturprinzipien

- Microservice-Architektur zur Trennung von Zuständigkeiten
- Skalierbarkeit durch Spark & Docker
- Sicherheit durch eingeschränkte Netzwerkbereiche und Zugang zu Services
- Einhaltung von Datenschutz und Data-Governance-Prinzipien

## Datenquellen

- Bitcoin Historical Data – minütlich
- DJIA Historical Data – täglich

## Visualisierungen

### Bitcoin Close Price Correlation

<img src="images/correlation_btc_close.png" alt="Correlation Bitcoin" width="600"/>

### DJIA Close Price Correlation

<img src="images/correlation_djia_close.png" alt="Correlation DJIA" width="600"/>

## Manuelle Ausführung beim ersten Start (Windows)

1. Stelle sicher, dass Docker Desktop gestartet ist.
2. Navigiere im Explorer zum Projektverzeichnis.
3. Führe die Datei `run_pipeline.bat` per Doppelklick aus.

   Alternativ im Terminal:

   ```bash
   cd "Pfad\zum\Projektordner"
   run_pipeline.bat
   ```

4. Installiere benötigte Python-Bibliotheken:

   ```bash
   pip install -r requirements.txt
   ```

5. Erstelle eine `.env` Datei mit folgendem Inhalt:

   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=geheim
   DB_NAME=finance
   ```

6. Lade deine `kaggle.json` von deinem Kaggle-Konto herunter und speichere sie unter:

   ```
   ingestion/kaggle/kaggle.json
   ```

7. Die Ausgabedateien findest du nach der Verarbeitung unter `data/processed/`.

## Automatisierte Ausführung mit dem Windows Task Scheduler

Die Pipeline kann einmal pro Quartal automatisch ausgeführt werden.

### Schritt-für-Schritt Anleitung:

1. Taskplaner öffnen  
   Suche im Startmenü nach "Aufgabenplanung" oder "Task Scheduler".

2. Neue Aufgabe erstellen  
   Klicke auf „Aufgabe erstellen…“ (nicht „Einfache Aufgabe“).

3. Registerkarte **Allgemein**  
   Name: `Data Pipeline Quarterly`  
   Haken bei „Mit höchsten Privilegien ausführen“ setzen

4. **Trigger**  
   Zeitplan: Monatlich  
   Wähle z. B. Januar, April, Juli, Oktober  
   Tag: z. B. 1., Uhrzeit: 10:00

5. **Aktionen**  
   Neue Aktion → „Programm starten“  
   Pfad zur `.bat`-Datei:
   ```
   C:\Pfad\zum\Projekt\run_pipeline.bat
   ```

6. **Bedingungen & Einstellungen (optional)**  
   - Nur bei Netzstrom ausführen  
   - Bei Bedarf auch bei Inaktivität

7. **Speichern und testen**  
   Rechtsklick auf den Task → „Ausführen“ testen
