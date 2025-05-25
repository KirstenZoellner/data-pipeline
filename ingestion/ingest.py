import os
import time
import pandas as pd
import mysql.connector
from kaggle.api.kaggle_api_extended import KaggleApi

# ----------------------
# KONSTANTEN & PFADSETUP
# ----------------------

RAW_DIR = '/app/data/raw'
PROCESSED_DIR = '/app/data/processed'
CORRELATION_CSV = os.path.join(PROCESSED_DIR, 'correlation_by_country_year.csv')
MERGED_CSV_PATH = os.path.join(PROCESSED_DIR, 'merged_data.csv')

DB_CONFIG = {
    'host': 'mysql',
    'user': 'root',
    'password': 'root',
    'database': 'gdp_data'
}

# ----------------------
# KAGGLE-DOWNLOAD
# ----------------------

def download_from_kaggle():
    print("🌐 Starte Kaggle-Download...")
    os.makedirs(RAW_DIR, exist_ok=True)

    api = KaggleApi()
    api.authenticate()

    datasets = {
        "gdp": "fredericksalazar/global-gdp-pib-per-capita-dataset-1960-present",
        "inflation": "fredericksalazar/global-inflation-rate-1960-present"
    }

    for name, dataset in datasets.items():
        print(f"📥 Lade {name}...")
        api.dataset_download_files(dataset, path=RAW_DIR, unzip=True)
        print(f"✅ {name} fertig.")

# ----------------------
# HILFSFUNKTIONEN
# ----------------------

def find_file(substring):
    for file in os.listdir(RAW_DIR):
        if substring.lower() in file.lower() and file.endswith('.csv'):
            return os.path.join(RAW_DIR, file)
    return None

# ----------------------
# VERARBEITUNG
# ----------------------

def load_and_merge_data():
    gdp_path = find_file('gdp') or find_file('pib')
    inflation_path = find_file('inflation')

    if not gdp_path or not inflation_path:
        raise FileNotFoundError("❌ GDP- oder Inflationsdaten fehlen im raw-Verzeichnis.")

    gdp_df = pd.read_csv(gdp_path)
    inflation_df = pd.read_csv(inflation_path)

    gdp_df = gdp_df[['country_name', 'year', 'gdp_per_capita']].rename(columns={
        'country_name': 'country',
        'year': 'year',
        'gdp_per_capita': 'gdp_per_capita'
    })

    inflation_df = inflation_df[['country_name', 'year', 'inflation_rate']].rename(columns={
        'country_name': 'country',
        'year': 'year',
        'inflation_rate': 'inflation'
    })

    merged_df = pd.merge(gdp_df, inflation_df, on=['country', 'year'])

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    merged_df.to_csv(MERGED_CSV_PATH, index=False)
    print(f"💾 Gespeichert: {MERGED_CSV_PATH}")

    return merged_df

# ----------------------
# DATENBANK
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
        INSERT INTO gdp_inflation (country, year, gdp_per_capita, inflation)
        VALUES (%s, %s, %s, %s)
        """
        values = (
            row['country'],
            int(row['year']),
            float(row['gdp_per_capita']),
            float(row['inflation'])
        )
        cursor.execute(sql, values)

    connection.commit()
    cursor.close()
    connection.close()
    print("✅ GDP/Inflation-Daten gespeichert.")

def import_correlations():
    if not os.path.exists(CORRELATION_CSV):
        print(f"⚠️ Keine Korrelationsergebnisse gefunden: {CORRELATION_CSV}")
        return

    df_corr = pd.read_csv(CORRELATION_CSV)

    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    for _, row in df_corr.iterrows():
        sql = """
        INSERT INTO correlation_by_country_year (country, year, pearson_correlation, lagged_pearson_correlation)
        VALUES (%s, %s, %s, %s)
        """

        values = (
            row['country_name'],
            int(row['year']),
            float(row['pearson_correlation']) if pd.notna(row['pearson_correlation']) else None,
            float(row['lagged_pearson_correlation']) if pd.notna(row['lagged_pearson_correlation']) else None
        )
        cursor.execute(sql, values)

    connection.commit()
    cursor.close()
    connection.close()
    print("✅ Korrelationen gespeichert.")

# ----------------------
# PIPELINE-AUFRUF
# ----------------------

if __name__ == "__main__":
    download_from_kaggle()
    df = load_and_merge_data()
    write_to_mysql(df)
    import_correlations()
