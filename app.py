import streamlit as st
from data_fetch import fetch_gold_data
from analysis import compute_indicators
from ml_model import load_models, predict
from decision_engine import decide_trade
from alerts import send_discord_alert
from utils.visualization import plot_signals

st.set_page_config(page_title="AI Gold Trader", layout="wide")
st.title("💰 AI Gold Trader - XAU/USD")

# --- جلب البيانات ---
df = fetch_gold_data()

# --- حساب المؤشرات ---
df = compute_indicators(df)

# --- تحميل النماذج ---
lstm_model, rf_model = load_models()

# --- التوقع ---
predicted_price, confidence = predict(df, lstm_model, rf_model)

# --- اتخاذ القرار ---
decision = decide_trade(predicted_price, confidence)

# --- إرسال التنبيه (اختياري) ---
if confidence > 0.8:
    send_discord_alert(decision, predicted_price, confidence)

# --- عرض الرسم ---
st.subheader("Gold Price Chart")
st.plotly_chart(plot_signals(df, predicted_price, decision))

# --- عرض القرار الحالي ---
st.write(f"**Current Decision:** {decision} | **Confidence:** {confidence:.2f}")
