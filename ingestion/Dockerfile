# Python-Slim Image als Basis
FROM python:3.9-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere das lokale Python-Skript ins Container-Verzeichnis
COPY ingest.py .

# Installiere benötigte Python-Pakete
RUN pip install pandas mysql-connector-python

# Standardkommando beim Containerstart
CMD ["python", "ingest.py"]
