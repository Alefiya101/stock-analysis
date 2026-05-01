import os
import pandas as pd

def load_stock_data(folder_path=None):
    if folder_path is None:
        # Go up one level from 'backend' folder to find 'input-dataset'
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        folder_path = os.path.join(base_dir, "input-dataset")
    """
    Reads all Excel files starting with 'Stock_' from the folder.
    Cleans and standardizes data.
    """
    data_store = {}

    if not os.path.exists(folder_path):
        print(f"❌ Error: Folder {folder_path} not found.")
        return data_store

    for filename in os.listdir(folder_path):
        if filename.startswith("Stock_") and filename.endswith(".xlsx"):

            # Extract symbol
            symbol = filename.replace("Stock_", "").replace(".xlsx", "").upper()
            file_path = os.path.join(folder_path, filename)

            try:
                df = pd.read_excel(file_path)

                # Normalize column names
                df.columns = df.columns.str.strip().str.upper()

                # Handle DATE / TIMESTAMP
                if 'DATE' in df.columns:
                    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
                elif 'TIMESTAMP' in df.columns:
                    df['DATE'] = pd.to_datetime(df['TIMESTAMP'], errors='coerce')
                else:
                    print(f"Skipping {symbol}: No DATE column")
                    continue

                # Drop invalid dates
                df = df.dropna(subset=['DATE'])

                # Sort by date
                df = df.sort_values(by='DATE')

                # Remove duplicate dates (keep the last one found)
                df = df.drop_duplicates(subset=['DATE'], keep='last')

                # Basic column validation
                required_cols = ['OPEN', 'CLOSE', 'VOLUME']
                missing = [col for col in required_cols if col not in df.columns]

                if missing:
                    print(f"Skipping {symbol}: Missing columns {missing}")
                    continue

                data_store[symbol] = df

                print(f"Loaded {symbol}: {len(df)} rows")

            except Exception as e:
                print(f"Failed to load {filename}: {e}")

    return data_store


if __name__ == "__main__":
    stocks = load_stock_data()
    print(f"\nTotal companies loaded: {len(stocks)}")

