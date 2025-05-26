import os
from kaggle.api.kaggle_api_extended import KaggleApi
from clean_djia_csv import clean_djia_csv

RAW_DIR = '/app/data/raw'

def download_from_kaggle():
    print("🌐 Starte Kaggle-Download...")
    os.makedirs(RAW_DIR, exist_ok=True)

    api = KaggleApi()
    api.authenticate()

    datasets = {
        "bitcoin": "mczielinski/bitcoin-historical-data",
        "djia": "joebeachcapital/djia-stocks-historical-ohlcv-daily-updated"
    }

    for name, dataset in datasets.items():
        print(f"📥 Lade {name}...")
        dataset_path = os.path.join(RAW_DIR, name)
        os.makedirs(dataset_path, exist_ok=True)
        api.dataset_download_files(dataset, path=dataset_path, unzip=True)
        print(f"✅ {name} fertig.")

    # 🧹 DJIA nach Download sofort bereinigen
    print("🧹 Bereinige DJIA-Datei...")
    clean_djia_csv(
        input_file='data/raw/djia/dow_jones_data.csv',
        output_file='data/raw/djia/djia_clean.csv',
        ticker='AAPL'  # ggf. dynamisch steuerbar
    )
    print("✅ DJIA-Bereinigung abgeschlossen.")

if __name__ == "__main__":
    download_from_kaggle()
