from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_unixtime, to_date, avg, when
from scipy.stats import pearsonr
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()  # Lädt Variablen aus .env-Datei

import mysql.connector
import time

# Pfade
BTC_PATH = "data/raw/bitcoin/btcusd_1-min_data.csv"
DJIA_CLEAN_PATH = "data/raw/djia/djia_clean.csv"
COMBINED_OUTPUT = "data/processed/combined_daily_and_summary.csv"
os.makedirs(os.path.dirname(COMBINED_OUTPUT), exist_ok=True)

# DB
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'btc_djia_data')
}


# Spark Session
spark = SparkSession.builder.appName("Rolling_Correlation").getOrCreate()

# BTC-Daten (Tagesschnitt)
btc_df = (
    spark.read.option("header", True).option("inferSchema", True).csv(BTC_PATH)
    .withColumn("date", to_date(from_unixtime(col("Timestamp"))))
    .groupBy("date").agg(avg("Close").alias("btc_close"))
    .filter(col("date") >= "2012-07-01")
)
btc_df = btc_df.withColumn("btc_close", when(col("btc_close") == 4.58, None).otherwise(col("btc_close"))).dropna()

# DJIA-Daten (bereits daily)
djia_df = (
    spark.read.option("header", True).option("inferSchema", True).csv(DJIA_CLEAN_PATH)
    .withColumnRenamed("Date", "date")
    .withColumnRenamed("Close_AAPL", "djia_close")
    .withColumn("date", to_date("date"))
)

# Join
merged_df = btc_df.join(djia_df, on="date", how="inner")
merged_pd = merged_df.toPandas().sort_values("date").dropna()

# Gleitendes Fenster
window_size = 7
results = []

for i in range(window_size, len(merged_pd)):
    window = merged_pd.iloc[i - window_size:i]
    btc = pd.to_numeric(window["btc_close"], errors="coerce")
    djia = pd.to_numeric(window["djia_close"], errors="coerce")

    if btc.nunique() > 1 and djia.nunique() > 1:
        corr, _ = pearsonr(btc, djia)
    else:
        corr = None

    row = merged_pd.iloc[i].to_dict()
    row["correlation"] = corr
    row["n_days"] = window_size
    row["start_date"] = window["date"].min()
    row["end_date"] = window["date"].max()
    results.append(row)

# Export
final_df = pd.DataFrame(results)
final_df.to_csv(COMBINED_OUTPUT, index=False)
print(f"📁 Datei gespeichert: {COMBINED_OUTPUT}")

# Optional: In MySQL schreiben
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
    for _, row in df.iterrows():
        sql = """
        INSERT INTO btc_djia_correlation (start_date, end_date, n_days, correlation)
        VALUES (%s, %s, %s, %s)
        """
        values = (
            row['start_date'],
            row['end_date'],
            int(row['n_days']),
            float(row['correlation']) if row['correlation'] is not None else None
        )
        cursor.execute(sql, values)

    connection.commit()
    cursor.close()
    connection.close()
    print("✅ Ergebnis in MySQL gespeichert.")

write_to_mysql(final_df)
