import os
import time
import pandas as pd
from scipy.stats import pearsonr
import mysql.connector
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date

# ----------------------
# CONFIG
# ----------------------

BTC_PATH = "data/raw/bitcoin/bitcoin.csv"   # ggf. Dateiname anpassen
DJIA_PATH = "data/raw/djia/djia.csv"         # ggf. Dateiname anpassen
OUTPUT_PATH = "data/processed/btc_djia_correlation.csv"
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

DB_CONFIG = {
    'host': 'mysql',
    'user': 'root',
    'password': 'root',
    'database': 'btc_djia_data'
}

# ----------------------
# SPARK
# ----------------------

spark = SparkSession.builder.appName("BTC_DJIA_Correlation").getOrCreate()

btc_df = spark.read.option("header", True).option("inferSchema", True).csv(BTC_PATH)
djia_df = spark.read.option("header", True).option("inferSchema", True).csv(DJIA_PATH)

btc_df = btc_df.withColumn("date", to_date(col("Date"), "yyyy-MM-dd")).select("date", col("Close").alias("btc_close"))
djia_df = djia_df.withColumn("date", to_date(col("Date"), "yyyy-MM-dd")).select("date", col("Close").alias("djia_close"))

merged_df = btc_df.join(djia_df, on="date", how="inner")

merged_pd = merged_df.toPandas().dropna().sort_values("date")

# ----------------------
# KORRELATION BERECHNEN
# ----------------------

corr, _ = pearsonr(merged_pd["btc_close"], merged_pd["djia_close"])

result_df = pd.DataFrame([{
    "correlation": corr,
    "n_days": len(merged_pd),
    "start_date": merged_pd["date"].min(),
    "end_date": merged_pd["date"].max()
}])

# ----------------------
# CSV SPEICHERN
# ----------------------

result_df.to_csv(OUTPUT_PATH, index=False)
print(f"✅ Korrelation gespeichert: {OUTPUT_PATH}")

# ----------------------
# IN MYSQL SCHREIBEN
# ----------------------

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
            float(row['correlation'])
        )
        cursor.execute(sql, values)

    connection.commit()
    cursor.close()
    connection.close()
    print("✅ Korrelation in MySQL gespeichert.")

write_to_mysql(result_df)
