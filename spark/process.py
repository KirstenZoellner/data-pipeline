import pandas as pd
from scipy.stats import pearsonr
import os

# Dateipfade
inflation_path = "data/raw/global_inflation_countries.csv"
gdp_path = "data/raw/pib_per_capita_countries_dataset.csv"
output_path = "data/processed/correlation_by_country_year/correlation_by_country_year.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# CSVs laden
inflation = pd.read_csv(inflation_path)
gdp = pd.read_csv(gdp_path)

# Nur relevante Spalten
inflation = inflation[["country_code", "country_name", "year", "inflation_rate"]].copy()
gdp = gdp[["country_code", "year", "gdp_per_capita"]].copy()

# 0-Werte und fehlende Daten ausschließen
inflation = inflation[inflation["inflation_rate"].notnull()]
gdp = gdp[gdp["gdp_per_capita"].notnull()]

# Zusammenführen
merged = pd.merge(inflation, gdp, on=["country_code", "year"], how="inner")

# Berechnung pro Land und Jahr
results = []

for country in merged["country_name"].unique():
    df = merged[merged["country_name"] == country].dropna().sort_values("year")
    years = df["year"].unique()

    for year in years:
        sub = df[df["year"] <= year].copy()

        # einfache Pearson Korrelation (t vs. t)
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

# Speichern
pd.DataFrame(results).to_csv(output_path, index=False)
