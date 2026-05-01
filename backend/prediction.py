import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import shap
import warnings

# Suppress SHAP warnings for a cleaner API output
warnings.filterwarnings("ignore")

def predict_7_days(df):
    """
    Predicts next 7 days using Random Forest Regressor.
    Includes SHAP explanations to translate technical variables for laymen.
    """
    # Features used for the model
    feature_cols = ['CLOSE', 'VOLUME', 'RETURN', 'VOLATILITY', 'MA_7']
    
    # Data preparation
    data = df[feature_cols].dropna()
    
    if len(data) < 40:
        return {
            "predictions": [],
            "trend": "NEUTRAL",
            "explanation": {},
            "confidence": "LOW",
            "r2_score": 0
        }

    # Prepare training set: Use past data to predict the NEXT 7 days simultaneously
    # This is a Multi-Output Regression approach for more realistic paths
    X_list = []
    y_list = []
    
    # Create windows of data
    for i in range(len(data) - 14): # 7 days input, 7 days output
        X_list.append(data.iloc[i : i+7].values.flatten()) # Flatten 7 days of features
        y_list.append(data.iloc[i+7 : i+14]['CLOSE'].values) # Next 7 days of prices
        
    X = np.array(X_list)
    y = np.array(y_list)
    
    # Train Multi-Output Random Forest
    model = RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42)
    model.fit(X, y)
    
    # --- 1. Predictions ---
    # Use the most recent 7 days of data to predict the next 7
    current_window = data.tail(7).values.flatten().reshape(1, -1)
    predictions = model.predict(current_window)[0]
    
    # --- 2. SHAP Interpretation ---
    # For SHAP in multi-output, we'll explain the FIRST day of the prediction
    # to show what is driving the immediate trend.
    explainer = shap.TreeExplainer(model)
    # Explaining the first output (day 1)
    shap_values = explainer.shap_values(current_window)
    # Handle multi-output SHAP (it returns a list of arrays)
    if isinstance(shap_values, list):
        shap_values_day1 = shap_values[0]
    else:
        # Some versions return a 3D array [samples, features, outputs]
        shap_values_day1 = shap_values[:, :, 0] if len(shap_values.shape) == 3 else shap_values

    # Sum the impact across the 7 days of input features for each metric
    explanation = {}
    layman_map = {
        'CLOSE': 'Price Momentum',
        'VOLUME': 'Trading Activity',
        'RETURN': 'Recent Gains',
        'VOLATILITY': 'Market Risk',
        'MA_7': 'Trend Strength'
    }
    
    for i, col in enumerate(feature_cols):
        # Since we flattened 7 days of 5 features (35 features total), 
        # we sum the impact of all 7 days for each specific feature.
        indices = [i + (j * 5) for j in range(7)]
        impact = float(np.sum(shap_values_day1[0, indices]))
        explanation[layman_map[col]] = round(impact, 2)

    # --- 3. Metrics ---
    r2 = model.score(X, y)
    
    return {
        "predictions": [round(float(p), 2) for p in predictions],
        "trend": "UP" if predictions[-1] > data['CLOSE'].iloc[-1] else "DOWN",
        "explanation": explanation,
        "confidence": "HIGH" if r2 > 0.7 else ("MEDIUM" if r2 > 0.4 else "LOW"),
        "r2_score": round(float(r2), 2)
    }

if __name__ == "__main__":
    print("Random Forest + SHAP Prediction module ready.")
