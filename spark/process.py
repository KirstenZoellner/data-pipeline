from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_unixtime, to_date
from scipy.stats import pearsonr
import pandas as pd
import os
import mysql.connector
import time

# Pfade
BTC_PATH = "data/raw/bitcoin/btcusd_1-min_data.csv"
DJIA_CLEAN_PATH = "data/raw/djia/djia_clean.csv"
CORRELATION_OUTPUT = "data/processed/daily_correlations.csv"
os.makedirs(os.path.dirname(CORRELATION_OUTPUT), exist_ok=True)

# MySQL Config
DB_CONFIG = {
    'host': 'mysql',
    'user': 'root',
    'password': 'root',
    'database': 'btc_djia_data'
}

# Spark starten
spark = SparkSession.builder.appName("Daily_BTC_DJIA_Correlation").getOrCreate()

# 🟡 BTC-Daten minutengenau laden
btc_df = (
    spark.read.option("header", True).option("inferSchema", True).csv(BTC_PATH)
    .withColumn("date", to_date(from_unixtime(col("Timestamp"))))
    .select("date", "Close")
)

# 🟢 DJIA-Daten laden
djia_df = (
    spark.read.option("header", True).option("inferSchema", True).csv(DJIA_CLEAN_PATH)
    .withColumnRenamed("Date", "date")
    .withColumnRenamed("Close_AAPL", "djia_close")
    .withColumn("date", to_date("date"))
    .select("date", "djia_close")
)

# 🔄 Join nach Datum (alle BTC-Minuten mit Tageswert von DJIA)
merged_df = btc_df.join(djia_df, on="date", how="inner")

# 🔁 In Pandas konvertieren
merged_pd = merged_df.toPandas().dropna().sort_values("date")
merged_pd["Close"] = pd.to_numeric(merged_pd["Close"], errors="coerce")
merged_pd["djia_close"] = pd.to_numeric(merged_pd["djia_close"], errors="coerce")
merged_pd = merged_pd.dropna()

# 📊 Tägliche Pearson-Korrelation
results = []
for day, group in merged_pd.groupby("date"):
    if group["Close"].nunique() > 1:
        corr, _ = pearsonr(group["Close"], group["djia_close"])
        results.append({"date": day, "correlation": corr, "count": len(group)})

# 📄 Speichern als CSV
result_df = pd.DataFrame(results)
result_df.to_csv(CORRELATION_OUTPUT, index=False)
print(f"✅ Tägliche Korrelationen gespeichert unter: {CORRELATION_OUTPUT}")

# 🛢 In MySQL schreiben
def write_to_mysql(df):
    for i in range(10):
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            print("✅ Verbindung zu MySQL hergestellt")
            break
        except mysql.connector.Error:
            print(f"⏳ Warte auf MySQL... Versuch {i+1}/10")
            time.sleep(5)
    else:
        raise ConnectionError("❌ Verbindung zu MySQL fehlgeschlagen.")

    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_btc_djia_correlation (
            date DATE PRIMARY KEY,
            correlation FLOAT,
            count INT
        )
    """)
    for _, row in df.iterrows():
        sql = """
        REPLACE INTO daily_btc_djia_correlation (date, correlation, count)
        VALUES (%s, %s, %s)
        """
        values = (row['date'], float(row['correlation']), int(row['count']))
        cursor.execute(sql, values)

    connection.commit()
    cursor.close()
    connection.close()
    print("✅ Tägliche Korrelationen in MySQL gespeichert.")

write_to_mysql(result_df)
