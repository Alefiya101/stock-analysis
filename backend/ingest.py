from data_loader import load_stock_data
from supabase_client import register_company, insert_stock_data

def run_ingestion():
    print("Starting Data Ingestion to Supabase...")
    
    # 1. Load the raw data from Excel
    stocks = load_stock_data()
    
    if not stocks:
        print("No data found in 'input-dataset'. Check your folder path.")
        return

    print(f"Found {len(stocks)} companies. Starting upload...")

    for symbol, df in stocks.items():
        print(f"\nProcessing {symbol}...")
        
        # 2. Register the company in the 'companies' table
        # (We use the symbol as the name for now, you can edit this later)
        success_reg = register_company(symbol, name=f"{symbol} Corp")
        
        if success_reg:
            # 3. Upload the full historical price data
            insert_stock_data(symbol, df)
        else:
            print(f"Skipping price upload for {symbol} because registration failed.")

    print("\nIngestion process finished!")

if __name__ == "__main__":
    run_ingestion()
