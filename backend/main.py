from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
import pandas as pd

# Import custom modules
from features import compute_features
from scoring import calculate_score
from prediction import predict_7_days
from supabase_client import get_all_symbols, get_stock_data_from_db

app = FastAPI(title="Stock Intelligence Dashboard API")

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Helper: Get Processed Data ---
def get_processed_df(symbol: str):
    """Fetches raw data from DB and computes features."""
    df = get_stock_data_from_db(symbol)
    if df is None or df.empty:
        return None
    
    try:
        df_featured = compute_features(df)
        return df_featured
    except Exception as e:
        print(f"Error processing features for {symbol}: {e}")
        return None

# --- Routes ---

@app.get("/api/health")
def read_root():
    return {
        "status": "online", 
        "message": "Stock Dashboard API is fetching directly from Supabase.",
    }


@app.get("/companies")
async def get_companies():
    """Returns a list of all available company symbols from Supabase."""
    symbols = get_all_symbols()
    return symbols


@app.get("/data/{symbol}")
async def get_stock_data(symbol: str):
    """Returns the last 100 days of historical data for the chart."""
    df = get_processed_df(symbol)

    if df is None:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found or has invalid data")

    # Get the last 100 days
    df_tail = df.tail(100).copy()

    # Convert DATE to string for JSON serialization
    df_tail['DATE'] = df_tail['DATE'].dt.strftime('%Y-%m-%d')

    return df_tail.to_dict(orient="records")


@app.get("/predict/{symbol}")
async def get_prediction(symbol: str):
    """Returns 7-day price forecast and trend analysis."""
    df = get_processed_df(symbol)

    if df is None:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")

    # Ensure we have enough data for a 30-day lookback
    if len(df) < 30:
        raise HTTPException(status_code=400, detail="Insufficient data for prediction (30 days required)")

    return predict_7_days(df)


@app.get("/top-picks")
async def get_top_picks():
    """Ranks stocks by Smart Score and returns the top 3."""
    symbols = get_all_symbols()
    rankings = []

    for symbol in symbols:
        try:
            df = get_processed_df(symbol)
            if df is not None:
                score = calculate_score(df)
                pred = predict_7_days(df)

                rankings.append({
                    "symbol": symbol,
                    "score": round(score, 4),
                    "trend": pred["trend"]
                })
        except Exception:
            continue

    # Sort by score descending and take top 3
    top_3 = sorted(rankings, key=lambda x: x['score'], reverse=True)[:3]
    return top_3


# --- Static File Serving (Monolith Mode) ---

# Define the path to the frontend build
# Adjusting for the 'backend' folder structure
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")

if os.path.exists(frontend_path):
    # Mount the static files (CSS, JS, etc.)
    # Note: Vite usually puts them in /assets
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_path, "assets")), name="static")

    # Catch-all route to serve the React index.html for any frontend route
    @app.get("/{rest_of_path:path}")
    async def serve_frontend(rest_of_path: str):
        return FileResponse(os.path.join(frontend_path, "index.html"))
else:
    print(f"Warning: Frontend build not found at {frontend_path}. API only mode.")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
