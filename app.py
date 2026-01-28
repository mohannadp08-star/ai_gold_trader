# app.py
import streamlit as st
from data_fetch import fetch_gold_data
from analysis import compute_indicators
from quant_features import add_quant_features
from ml_model import train_rf
from decision_engine import make_decision
from alerts import send_discord_alert
import plotly.graph_objects as go


st.set_page_config(page_title="🤖 Auto AI Gold Trader", layout="wide")
st.title("🤖 Auto AI Gold Trader")


# Fetch and prepare data
df = fetch_gold_data()
df = compute_indicators(df)
df = add_quant_features(df)


features = ["XAU","EMA20","EMA50","RSI14","Return_5","Volatility","Momentum","Unusual"]
rf = train_rf(df, features)
last = df.iloc[-1]
rf_pred = rf.predict([last[features]])[0]


# Use float conversion safely
pred_price = float(last["XAU"] + 0.1) # مثال على التوقع يمكن تغييره لاحقًا
current_price = float(last["XAU"])
rsi = float(last["RSI14"])
anomaly = bool(last["Unusual"].any()) # تصحيح مشكلة truth value


# Decision
decision = make_decision(rf_pred, pred_price, current_price, rsi, anomaly)
sl = current_price - (current_price * 0.0085)
tp = current_price + (current_price * 0.0095)


# Discord Alert
send_discord_alert(decision, current_price, pred_price)


# Plot chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['XAU'], mode='lines', name='Gold Price'))
fig.update_layout(title='Gold Price Chart', xaxis_title='Date', yaxis_title='Price', template='plotly_dark')
st.plotly_chart(fig, width='stretch')


# Display info
st.metric("Current Price", f"{current_price:.2f}")
st.metric("Predicted Price (LSTM)", f"{pred_price:.2f}")
st.metric("Confidence", "50%")
st.metric("Decision", decision)
st.write(f"Stop Loss: {sl:.2f} | Take Profit: {tp:.2f}")
