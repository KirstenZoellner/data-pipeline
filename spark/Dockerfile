FROM bitnami/spark:3.5.0

# Root-Rechte zum Installieren
USER root

# System & Python Pakete
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install --no-cache-dir \
        pandas \
        scipy \
        mysql-connector-python \
        py4j

# Arbeitsverzeichnis
WORKDIR /app

# Python-Skript reinkopieren
COPY process.py .

# Zurück zum Standardnutzer (1001)
USER 1001

# Starte Verarbeitung direkt
CMD ["python3", "/app/process.py"]
