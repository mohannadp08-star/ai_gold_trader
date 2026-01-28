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

# ────────────── جلب البيانات ──────────────
df = fetch_gold_data()

# التحقق من وجود البيانات
if df.empty:
    st.error("لا توجد بيانات متاحة الآن. حاول مرة أخرى لاحقًا.")
    st.stop()

# ────────────── التحليلات والمؤشرات ──────────────
df = compute_indicators(df)
df = add_quant_features(df)
df = calculate_atr(df)

features = ["XAU","EMA20","EMA50","RSI14","Return_5","Volatility","Momentum","Trend_EMA"]

# ────────────── تدريب Random Forest ──────────────
rf = train_rf(df, features)

# استخدام آخر صف فقط لكل القيم
last = df.iloc[-1]

# تحويل كل القيم إلى نوع بايثون مفرد
rf_pred = int(rf.predict([last[features]])[0])
pred_price = float(last["XAU"].iloc[0]) + 0.1  # مثال على التوقع، يمكن تعديل بناءً على LSTM
current_price = float(last["XAU"].iloc[0])
rsi = float(last["RSI14"].iloc[0])
anomaly = bool(last["Unusual"].iloc[0])         # تحويل Series صغيرة إلى bool

# ────────────── اتخاذ القرار النهائي ──────────────
decision = make_decision(rf_pred, pred_price, current_price, rsi, anomaly)

# حساب الثقة
conf = confidence_score(rf_pred, pred_price, current_price, rsi, anomaly)

# ────────────── عرض النتائج ──────────────
st.metric("Current Price", current_price)
st.metric("Predicted Price", pred_price)
st.metric("Confidence", f"{conf}%")
st.metric("Decision", decision)

# حساب SL / TP باستخدام ATR
atr = last["ATR"].iloc[0]
sl, tp = atr_sl_tp(current_price, atr)
st.write(f"SL: {sl} | TP: {tp}")

# إرسال إشعار Discord إذا كانت الثقة > 75%
if conf > 75:
    send_discord_alert(
        f"🚀 Strong signal detected!\nPrice: {current_price}\nPredicted: {pred_price:.2f}\nConfidence: {conf}%\nDecision: {decision}"
    )
