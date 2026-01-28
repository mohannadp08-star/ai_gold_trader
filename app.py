import streamlit as st
from data_fetch import fetch_gold_data
from analysis import compute_indicators
from quant_features import add_quant_features
from ml_model import train_rf
from lstm_model import prepare_lstm, build_lstm
from confidence import confidence_score
from risk_management import calculate_atr, atr_sl_tp
from discord_alerts import send_discord_alert
from decision_engine import make_decision
import numpy as np

st.title("🤖 Auto AI Gold Trader")

# جلب البيانات
df = fetch_gold_data()

# التحقق من وجود البيانات
if df.empty:
    st.error("لا توجد بيانات متاحة الآن. حاول مرة أخرى لاحقًا.")
    st.stop()

# التحليلات والمؤشرات
df = compute_indicators(df)
df = add_quant_features(df)
df = calculate_atr(df)

features = ["XAU","EMA20","EMA50","RSI14","Return_5","Volatility","Momentum","Trend_EMA"]

# تدريب Random Forest
rf = train_rf(df, features)

last = df.iloc[-1]

rf_pred = rf.predict([last[features]])[0]

# إعداد LSTM
X, y, scaler = prepare_lstm(df, features)
model = build_lstm((X.shape[1], X.shape[2]))
model.fit(X, y, epochs=3, verbose=0)

pred = model.predict(X[-1].reshape(1, X.shape[1], X.shape[2]))
pred_price = scaler.inverse_transform([[pred[0][0]] + [0]*(len(features)-1)])[0][0]

# حساب الثقة واتخاذ القرار
conf = confidence_score(rf_pred, pred_price, last["XAU"], last["RSI14"], last["Unusual"])
decision = make_decision(rf_pred, pred_price, last["XAU"], last["RSI14"], last["Unusual"])

# عرض النتائج
st.metric("Current Price", last["XAU"])
st.metric("Predicted Price", pred_price)
st.metric("Confidence", f"{conf}%")
st.metric("Decision", decision)

atr = last["ATR"]
sl, tp = atr_sl_tp(last["XAU"], atr)
st.write(f"SL: {sl} | TP: {tp}")

# إرسال إشعار Discord إذا كانت الثقة > 75%
if conf > 75:
    send_discord_alert(f"🚀 Strong signal detected!\nPrice: {last['XAU']}\nPredicted: {pred_price:.2f}\nConfidence: {conf}%\nDecision: {decision}")
