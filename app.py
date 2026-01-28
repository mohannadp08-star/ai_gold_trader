# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from data_fetch import fetch_gold_data
from analysis import compute_indicators
from quant_features import add_quant_features
from ml_model import train_rf
from decision_engine import make_decision
from alerts import send_discord_alert
from sklearn.preprocessing import MinMaxScaler

st.set_page_config(page_title="🤖 Auto AI Gold Trader", layout="wide")

st.title("🤖 Auto AI Gold Trader")

# -------------------------------
# Fetch & Prepare Data
# -------------------------------
df = fetch_gold_data()               # جلب بيانات الذهب
df = compute_indicators(df)          # المؤشرات مثل RSI, EMA
df = add_quant_features(df)          # ميزات Quant إضافية

features = ["XAU","EMA20","EMA50","RSI14","Return_5","Volatility","Momentum","Unusual"]

# -------------------------------
# Train Random Forest
# -------------------------------
rf = train_rf(df, features)
last = df.iloc[-1]

rf_pred = rf.predict([last[features]])[0]

# -------------------------------
# LSTM Prediction Placeholder
# -------------------------------
# لاحقًا يمكن وضع LSTM الحقيقي هنا
scaler = MinMaxScaler()
scaled_prices = scaler.fit_transform(df[["XAU"]])
lstm_pred_scaled = scaled_prices[-1] + 0.01  # مثال على توقع صغير
pred_price = scaler.inverse_transform([[lstm_pred_scaled]])[0,0]

current_price = float(last["XAU"])
rsi = float(last["RSI14"])
anomaly = bool(last["Unusual"].any()) if hasattr(last["Unusual"], 'any') else bool(last["Unusual"])

# -------------------------------
# Make Decision
# -------------------------------
decision = make_decision(rf_pred, pred_price, current_price, rsi, anomaly)

# Stop Loss / Take Profit (مثال باستخدام ATR)
stop_loss = current_price - 45
take_profit = current_price + 90

# -------------------------------
# Display Info
# -------------------------------
st.metric("Current Price", f"${current_price:.2f}")
st.metric("Predicted Price (LSTM)", f"${pred_price:.2f}")
st.metric("Confidence", "50%")  # Placeholder
st.metric("Decision", decision)
st.text(f"SL: {stop_loss:.2f} | TP: {take_profit:.2f}")

# -------------------------------
# Plotly Chart with Color for Decision
# -------------------------------
fig = go.Figure()

color_map = {"BUY": "green", "SELL": "red", "HOLD": "blue"}
line_color = color_map.get(decision, "blue")

fig.add_trace(go.Scatter(
    x=df.index,
    y=df["XAU"],
    mode='lines',
    line=dict(color=line_color, width=2),
    name="Gold Price"
))

fig.update_layout(
    title="Gold Price Chart",
    xaxis_title="Date",
    yaxis_title="Price USD",
    template="plotly_dark",
    height=500
)

st.plotly_chart(fig, width="stretch")

# -------------------------------
# Send Discord Alert
# -------------------------------
send_discord_alert(decision, current_price, pred_price)
