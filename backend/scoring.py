import pandas as pd

def calculate_score(df):
    """
    Calculates a stock score based on:
    - 30-day return
    - volume growth
    - volatility

    Formula:
    score = (0.5 * return) + (0.3 * volume_growth) - (0.2 * volatility)
    """

    if df is None or len(df) < 30:
        return 0.0

    recent_df = df.tail(30).copy()

    # --- Validate required columns ---
    required_cols = ['CLOSE', 'VOLUME', 'VOLATILITY']
    for col in required_cols:
        if col not in recent_df.columns:
            raise ValueError(f"Missing column: {col}")

    # --- 1. 30-day Return ---
    start_price = recent_df['CLOSE'].iloc[0]
    end_price = recent_df['CLOSE'].iloc[-1]

    if start_price == 0:
        total_return_30d = 0
    else:
        total_return_30d = (end_price - start_price) / start_price

    # --- 2. Volume Growth ---
    avg_vol_30 = recent_df['VOLUME'].mean()
    avg_vol_7 = recent_df['VOLUME'].tail(7).mean()

    volume_growth = ((avg_vol_7 / avg_vol_30) - 1) if avg_vol_30 != 0 else 0

    # --- 3. Volatility ---
    avg_volatility = recent_df['VOLATILITY'].mean(skipna=True)

    if pd.isna(avg_volatility):
        avg_volatility = 0

    # --- Optional: normalize volume growth to avoid domination ---
    volume_growth = min(volume_growth, 2)  # cap extreme spikes

    # --- Final Score ---
    score = (
        (0.5 * total_return_30d) +
        (0.3 * volume_growth) -
        (0.2 * avg_volatility)
    )

    return float(score)


if __name__ == "__main__":
    print("Scoring module ready.")
