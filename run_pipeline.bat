@echo off
cd "C:\Users\kirst\Desktop\IT\IU\Projekt Data Engineering\data-pipeline"
docker-compose run --rm ingestion
docker-compose run --rm spark
