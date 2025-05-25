# Basierend auf offiziellem Bitnami Spark-Image
FROM bitnami/spark:3.5.0

# Wechsle auf Root-Rechte für Paketinstallation
USER root

# Installiere pip + pyspark + pandas
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install pyspark pandas

# Arbeitsverzeichnis
WORKDIR /app

# Kopiere deine Skripte
COPY process.py .

# Zurück zum Standardbenutzer
USER 1001

# Container soll aktiv bleiben
CMD ["sleep", "3600"]

RUN pip install scipy pandas

