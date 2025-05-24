
import os
import time
import pandas as pd
import mysql.connector

# Verbindungseinstellungen für MySQL
DB_CONFIG = {
    'host': 'mysql',
    'user': 'root',
    'password': 'root',
    'database': 'gdp_data'
}

# Dateipfade zu den neuen Dateien
GDP_CSV = '/app/data/raw/pib_per_capita_countries_dataset.csv'
INFLATION_CSV = '/app/data/raw/global_inflation_countries.csv'
MERGED_CSV_PATH = '/app/data/processed/merged_data.csv'
CORRELATION_CSV = '/app/data/processed/correlation_by_country_year/reimport.csv'

def load_and_merge_data():
    gdp_df = pd.read_csv(GDP_CSV)
    inflation_df = pd.read_csv(INFLATION_CSV)

    # Debug-Ausgabe vor dem Umbau
    print("📌 Spalten in gdp_df:", gdp_df.columns.tolist())
    print("📌 Spalten in inflation_df:", inflation_df.columns.tolist())

    # Umbenennen auf identische Join-Spalten
    gdp_df = gdp_df[['country_name', 'year', 'gdp_per_capita']].rename(
        columns={'country_name': 'country', 'year': 'year', 'gdp_per_capita': 'gdp_per_capita'}
    )

    inflation_df = inflation_df[['country_name', 'year', 'inflation_rate']].rename(
        columns={'country_name': 'country', 'year': 'year', 'inflation_rate': 'inflation'}
    )

    print("📌 Nach Umbenennung gdp_df:", gdp_df.columns.tolist())
    print("📌 Nach Umbenennung inflation_df:", inflation_df.columns.tolist())

    # Jetzt klappt der Merge!
    merged_df = pd.merge(gdp_df, inflation_df, on=['country', 'year'])

    # Speichern
    os.makedirs('/app/data/processed', exist_ok=True)
    merged_df.to_csv(MERGED_CSV_PATH, index=False)
    print(f"✅ Datei gespeichert: {MERGED_CSV_PATH}")

    return merged_df

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
    print("✅ GDP- und Inflationsdaten erfolgreich in MySQL eingefügt")

def import_correlations():
    if not os.path.exists(CORRELATION_CSV):
        print(f"❌ Korrelationsergebnis nicht gefunden: {CORRELATION_CSV}")
        return

    df_corr = pd.read_csv(CORRELATION_CSV)

    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    for _, row in df_corr.iterrows():
        sql = """
        INSERT INTO correlation_by_country_year (country, year, num_records, correlation)
        VALUES (%s, %s, %s, %s)
        """

        # Sichere Umwandlung
        correlation_value = row['correlation']
        if pd.isna(correlation_value) or str(correlation_value).lower() in ['nan', 'null', 'none']:
            correlation_value = None
        else:
            correlation_value = float(correlation_value)

        values = (
            row['country'],
            int(row['year']),
            int(row['num_records']),
            correlation_value
        )
        cursor.execute(sql, values)

    connection.commit()
    cursor.close()
    connection.close()
    print("✅ Korrelationsergebnisse erfolgreich in MySQL importiert.")
