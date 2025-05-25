# Python-Slim Image als Basis
FROM python:3.9-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere alle Dateien
COPY . /app

# Installiere benötigte Python-Pakete
RUN pip install pandas mysql-connector-python kaggle

# Standardkommando beim Containerstart
CMD ["python", "ingest.py"]
