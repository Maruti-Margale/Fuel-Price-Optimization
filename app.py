import streamlit as st
import pandas as pd
import numpy as np
import json

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(page_title="Fuel Price Optimization", layout="centered")
st.title("⛽ Fuel Price Optimization")
st.write("Random Forest based daily price recommendation")

# -----------------------------
# Load historical data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("oil_retail_history.csv")
    df["date"] = pd.to_datetime(df["date"])
    df = df[df["volume"] >= 0]
    df = df[df["price"] >= df["cost"]]
    df = df.dropna()
    df = df.sort_values("date")
    return df

df = load_data()

# -----------------------------
# Feature engineering (same as your file)
# -----------------------------
df["comp_avg"] = (df["comp1_price"] + df["comp2_price"] + df["comp3_price"]) / 3
df["price_vs_comp"] = df["price"] - df["comp_avg"]

df["price_lag_1"] = df["price"].shift(1)
df["volume_lag_1"] = df["volume"].shift(1)
df["volume_lag_7"] = df["volume"].shift(7)

df["rolling_vol_7"] = df["volume"].rolling(7).mean()
df["rolling_price_7"] = df["price"].rolling(7).mean()

df["day_of_week"] = df["date"].dt.weekday
df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
df["month"] = df["date"].dt.month

df = df.dropna()

# -----------------------------
# Features & target
# -----------------------------
features = [
    "price", "cost",
    "comp1_price", "comp2_price", "comp3_price",
    "price_vs_comp",
    "price_lag_1",
    "volume_lag_1", "volume_lag_7",
    "rolling_vol_7", "rolling_price_7",
    "is_weekend", "month"
]

X = df[features]
y = df["volume"]

# -----------------------------
# Train-test split (no shuffle)
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# -----------------------------
# Train Random Forest
# -----------------------------
rf = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

rf.fit(X_train, y_train)

# -----------------------------
# Show model accuracy
# -----------------------------
pred = rf.predict(X_test)
mape = mean_absolute_percentage_error(y_test, pred)

st.info(f"Model Validation MAPE: {round(mape * 100, 2)}%")

# -----------------------------
# Sidebar inputs (today's prices)
# -----------------------------
st.sidebar.header("Today's Market Prices")

price = st.sidebar.number_input("Your last price", value=94.45)
cost = st.sidebar.number_input("Today's cost", value=85.77)
comp1 = st.sidebar.number_input("Competitor 1 price", value=95.01)
comp2 = st.sidebar.number_input("Competitor 2 price", value=95.70)
comp3 = st.sidebar.number_input("Competitor 3 price", value=95.21)

# -----------------------------
# Prepare today's features
# -----------------------------
last_row = df.iloc[-1]

comp_avg = (comp1 + comp2 + comp3) / 3

today_row = {
    "price": price,
    "cost": cost,
    "comp1_price": comp1,
    "comp2_price": comp2,
    "comp3_price": comp3,
    "price_vs_comp": price - comp_avg,
    "price_lag_1": last_row["price"],
    "volume_lag_1": last_row["volume"],
    "volume_lag_7": last_row["volume_lag_7"],
    "rolling_vol_7": last_row["rolling_vol_7"],
    "rolling_price_7": last_row["rolling_price_7"],
    "is_weekend": 0,
    "month": last_row["month"]
}

# -----------------------------
# Price optimization
# -----------------------------
if st.button("📈 Recommend Optimal Price"):

    min_price = max(cost * 1.02, price * 0.97)
    max_price = price * 1.03

    best_price = price
    best_profit = -1
    best_volume = 0

    for p in np.linspace(min_price, max_price, 20):
        today_row["price"] = p
        X_today = pd.DataFrame([today_row])[features]
        volume = rf.predict(X_today)[0]
        profit = (p - cost) * volume

        if profit > best_profit:
            best_profit = profit
            best_price = p
            best_volume = volume

    st.success("✅ Price Recommendation")
    st.metric("Recommended Price", f"{best_price:.2f}")
    st.metric("Expected Volume", int(best_volume))
    st.metric("Expected Profit", f"{int(best_profit):,}")
