import csv

def clean_djia_csv(input_file, output_file, ticker):
    prefixes = ['Close', 'High', 'Low', 'Open', 'Volume']
    columns_to_keep = ['Date'] + [f"{prefix}_{ticker}" for prefix in prefixes]

    with open(input_file, newline='') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        rows = list(reader)

        full_header = rows[0]
        ticker_row = rows[1]

        processed_header = []
        for i, col in enumerate(full_header):
            t = ticker_row[i].strip()
            col_name = f"{col}_{t}" if col != "Date" and t else col
            processed_header.append(col_name)

        keep_indices = [i for i, col in enumerate(processed_header) if col in columns_to_keep]

        writer.writerow([processed_header[i] for i in keep_indices])
        for row in rows[2:]:
            writer.writerow([row[i] for i in keep_indices])

    print(f"✔️ Bereinigte Datei geschrieben: {output_file}")
