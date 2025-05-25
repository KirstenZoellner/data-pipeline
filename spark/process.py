
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from scipy.stats import pearsonr
import pandas as pd
import os

# Spark Session starten
spark = SparkSession.builder.appName("CorrelationByCountryYear").getOrCreate()

# Dateipfade
inflation_path = "data/raw/global_inflation_countries.csv"
gdp_path = "data/raw/pib_per_capita_countries_dataset.csv"
os.makedirs("data/processed", exist_ok=True)
output_path = "data/processed/correlation_by_country_year.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# CSVs laden
inflation_df = spark.read.option("header", True).option("inferSchema", True).csv(inflation_path)
gdp_df = spark.read.option("header", True).option("inferSchema", True).csv(gdp_path)

# Nur relevante Spalten auswählen
inflation_df = inflation_df.select("country_code", "country_name", "year", "inflation_rate")
gdp_df = gdp_df.select("country_code", "year", "gdp_per_capita")

# Nullwerte filtern
inflation_df = inflation_df.filter(col("inflation_rate").isNotNull())
gdp_df = gdp_df.filter(col("gdp_per_capita").isNotNull())

# Zusammenführen
merged_df = inflation_df.join(gdp_df, on=["country_code", "year"], how="inner")

# In Pandas umwandeln für komplexe Korrelationen
merged_pd = merged_df.toPandas()

# Berechnung wie im Original
results = []

for country in merged_pd["country_name"].unique():
    df = merged_pd[merged_pd["country_name"] == country].dropna().sort_values("year")
    years = df["year"].unique()

    for year in years:
        sub = df[df["year"] <= year].copy()

        # einfache Pearson Korrelation
        try:
            pearson_corr, _ = pearsonr(sub["inflation_rate"], sub["gdp_per_capita"])
        except:
            pearson_corr = pd.NA

        # Lagged Pearson: Inflation(t) vs. GDP(t+1)
        sub["gdp_lagged"] = sub["gdp_per_capita"].shift(-1)
        sub_lagged = sub.dropna()
        try:
            lag_corr, _ = pearsonr(sub_lagged["inflation_rate"], sub_lagged["gdp_lagged"])
        except:
            lag_corr = pd.NA

        results.append({
            "country_name": country,
            "year": int(year),
            "pearson_correlation": pearson_corr,
            "lagged_pearson_correlation": lag_corr
        })

# Ergebnisse speichern
pd.DataFrame(results).to_csv(output_path, index=False)
print(f"✅ Ergebnis gespeichert: {output_path}")
