FROM bitnami/spark:3.5.0

USER root

RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install --no-cache-dir \
        pandas \
        scipy \
        mysql-connector-python \
        python-dotenv \
        py4j

WORKDIR /app
COPY process.py .

USER 1001

CMD ["python3", "/app/process.py"]
