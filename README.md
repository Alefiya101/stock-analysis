# 📈 Stock Intelligence Dashboard: Professional ML Analytics Platform

An end-to-end financial intelligence engine that transforms a decade of raw NSE market data into actionable, interpretable forecasting insights.

---

## 🏗️ The Engineering Pipeline: A Logical Flow

### **1. Data Sourcing (The Foundation)**
The project utilizes 10 years of historical stock data (2010–2020) from the **National Stock Exchange (NSE)**, originally sourced from **Kaggle**. 
- **Scale**: Over 20,000 unique price records across 9 blue-chip companies.
- **Format**: Raw multi-sheet Excel workbooks requiring high-fidelity parsing.

### **2. Preprocessing & Data Integrity (The ETL Layer)**
Raw financial data is inherently messy. A custom ETL engine (`ingest.py`) was engineered to solve several critical data challenges:
- **Normalization**: Resolved inconsistent column naming (e.g., merging `TIMESTAMP` and `DATE` fields) and standardized numerical formats across different company exports.
- **Duplicate Resolution**: Implemented a "Last-State Wins" strategy to identify and remove duplicate intra-day records, ensuring the time series remains mathematically valid.
- **Constraint-Driven Ingestion**: Utilized **Supabase PostgreSQL** with unique constraint handling to allow for idempotent batch uploads, ensuring the database remains the "single source of truth."

### **3. Feature Selection & Engineering (The Math)**
To go beyond raw price data, the backend dynamically calculates a suite of technical indicators:
- **7-Day Moving Average (MA_7)**: Engineered to smooth short-term noise and identify underlying momentum.
- **Daily Returns**: Logarithmic calculation to standardize profit/loss ratios across different price scales.
- **Volatility (Risk Factor)**: Rolling standard deviation of returns to quantify market fear and uncertainty.
- **Smart Score**: A proprietary mathematical composite (0.0 - 1.0) that weights historical performance, current momentum, and model confidence into a single rankable metric.

### **4. Predictive Modeling: Why Random Forest?**
For the intelligence layer, a **Random Forest Regressor** was selected over simpler models.
- **Non-Linear Relationships**: Market data rarely follows a straight line; Random Forest excels at capturing complex, non-linear interactions between volume, volatility, and price.
- **Ensemble Stability**: By averaging multiple decision trees, the model reduces "overfitting" (detecting patterns that don't exist) and provides more reliable 7-day forecasts.
- **Robustness**: It naturally handles outliers and variations in trading volume that occur during market shocks.

### **5. Explainable AI (SHAP Integration)**
To ensure the model is not a "black box," the system integrates **SHAP (SHapley Additive exPlanations)**.
- **Layman Mapping**: Technical variables are translated into "Key Drivers" (e.g., mapping `VOLUME` to "Market Trading Activity").
- **Transparency**: SHAP decomposes the final prediction, showing the user exactly how much each factor pushed the price up or down. This builds trust by showing the "Why" behind the "What."

---

## 🛠️ System Orchestration

### **Backend: High-Density FastAPI**
- **Architecture**: Modular Python services designed for on-demand computation.
- **Cloud Backbone**: Deep integration with **Supabase** for persistent, cloud-scalable data storage.
- **Performance**: High-speed endpoints serving pre-calculated technicals and real-time ML inferences.

### **Frontend: Professional Finance Dashboard**
- **Design Philosophy**: A "Standard Finance" UI built for high-density data viewing. No distractions—just crisp borders, solid backgrounds, and clear information hierarchy.
- **Visualization (Recharts)**: Interactive Area charts that seamlessly blend historical reality with the 7-day ML forecast.
- **Predictive Panel**: A dedicated intelligence center showing trend directions, growth slopes, and model accuracy (R²).

---

## 📂 Project Architecture
```text
/stock-dashboard
  ├── /backend             # Intelligence & Data Layer
---

## 🚀 Deployment Status

**Live on Render**

---
