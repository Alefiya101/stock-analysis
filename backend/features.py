import pandas as pd

def compute_features(df):
    """
    Adds calculated metrics:
    - RETURN
    - VOLATILITY
    - VOL_MA
    - MA_7
    - 52-week HIGH/LOW
    """

    df = df.copy()

    # Validate required columns
    required_cols = ['CLOSE', 'VOLUME']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # 1. RETURN (Daily Return = (CLOSE - OPEN) / OPEN)
    df['RETURN'] = (df['CLOSE'] - df['OPEN']) / df['OPEN']

    # 2. VOLATILITY (7-day rolling std)
    df['VOLATILITY'] = df['RETURN'].rolling(window=7).std()

    # 3. Volume Moving Average
    df['VOL_MA_7'] = df['VOLUME'].rolling(window=7).mean()

    # --- Assignment Metrics ---

    # 4. 7-day Moving Average of Close
    df['MA_7'] = df['CLOSE'].rolling(window=7).mean()

    # 5. 52-week High/Low (~252 trading days)
    df['HIGH_52W'] = df['CLOSE'].rolling(window=252, min_periods=1).max()
    df['LOW_52W'] = df['CLOSE'].rolling(window=252, min_periods=1).min()

    # --- Handle NaNs carefully ---

    # First RETURN will be NaN → set to 0
    df['RETURN'] = df['RETURN'].fillna(0)

    # Rolling features → backward fill
    rolling_cols = ['VOLATILITY', 'VOL_MA_7', 'MA_7']
    df[rolling_cols] = df[rolling_cols].bfill()

    return df


if __name__ == "__main__":
    print("Feature computation module ready.")
