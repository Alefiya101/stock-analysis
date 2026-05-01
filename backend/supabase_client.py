import os
from supabase import create_client, Client
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# --- Load from environment variables ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# We use placeholders if not set, to avoid immediate crashes during development
if not SUPABASE_URL:
    SUPABASE_URL = "https://your-project-id.supabase.co"
if not SUPABASE_KEY:
    SUPABASE_KEY = "your-service-role-key"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def register_company(symbol, name, sector="Finance"):
    """
    Ensures the company exists in the 'companies' table.
    """
    try:
        data = {
            "symbol": symbol.upper(),
            "name": name,
            "sector": sector
        }
        supabase.table("companies").upsert(data).execute()
        print(f"Registered company: {symbol}")
        return True
    except Exception as e:
        print(f"Error registering company {symbol}: {e}")
        return False


def insert_stock_data(symbol, df):
    """
    Inserts processed stock data into Supabase in batches.
    """
    # ... (Keep existing code from here down)

    required_cols = ['DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    # Convert DataFrame → records (FASTER than iterrows)
    records_df = df[required_cols].copy()

    records_df['symbol'] = symbol
    records_df['date'] = records_df['DATE'].dt.strftime('%Y-%m-%d')

    # Rename columns to match DB schema (snake_case)
    records_df = records_df.rename(columns={
        'OPEN': 'open',
        'HIGH': 'high',
        'LOW': 'low',
        'CLOSE': 'close',
        'VOLUME': 'volume'
    })

    # Keep only required columns for the database
    records_df = records_df[['symbol', 'date', 'open', 'high', 'low', 'close', 'volume']]

    # Convert to list of dictionaries
    records = records_df.to_dict(orient="records")

    try:
        # Batch insert for safety and performance
        batch_size = 500
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            # Use on_conflict to ensure we update existing rows instead of failing
            supabase.table("stock_data").upsert(batch, on_conflict="symbol,date").execute()

        print(f"Uploaded {len(records)} rows for {symbol}")
        return True

    except Exception as e:
        print(f"Error uploading {symbol}: {e}")
        return False


def get_all_symbols():
    """
    Fetches all unique symbols from the 'companies' table.
    """
    try:
        response = supabase.table("companies").select("symbol").execute()
        return [item['symbol'] for item in response.data]
    except Exception as e:
        print(f"❌ Error fetching symbols: {e}")
        return []


def get_stock_data_from_db(symbol):
    """
    Fetches historical stock data for a symbol and returns it as a DataFrame.
    """
    try:
        response = supabase.table("stock_data") \
            .select("*") \
            .eq("symbol", symbol.upper()) \
            .order("date", desc=False) \
            .execute()
            
        if not response.data:
            return None
            
        df = pd.DataFrame(response.data)
        
        # Convert snake_case back to UPPERCASE for internal consistency (features/scoring expect this)
        df = df.rename(columns={
            'date': 'DATE',
            'open': 'OPEN',
            'high': 'HIGH',
            'low': 'LOW',
            'close': 'CLOSE',
            'volume': 'VOLUME'
        })
        
        # Ensure correct data types
        df['DATE'] = pd.to_datetime(df['DATE'])
        numeric_cols = ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
        
        return df
    except Exception as e:
        print(f"❌ Error fetching data for {symbol}: {e}")
        return None


if __name__ == "__main__":
    print("✅ Supabase client ready")
    symbols = get_all_symbols()
    print(f"Found symbols: {symbols}")
