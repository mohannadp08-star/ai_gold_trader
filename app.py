import streamlit as st
import plotly.graph_objects as go
from data_fetch import fetch_gold_data
from analysis import compute_indicators
from quant_features import add_quant_features
from ml_model import train_rf
from lstm_model import prepare_lstm, build_lstm
from confidence import confidence_score
from risk_management import calculate_atr, atr_sl_tp
from discord_alerts import send_discord_alert
from decision_engine import make_decision

st.set_page_config(page_title="🤖 Auto AI Gold Trader", layout="wide")

st.title("🤖 Auto AI Gold Trader")

# ────────────── جلب البيانات ──────────────
df = fetch_gold_data()

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

last = df.iloc[-1]

# ────────────── توقعات LSTM حقيقية ──────────────
lstm_predictions = build_lstm(prepare_lstm(df))
pred_price = float(lstm_predictions.iloc[-1])

current_price = float(last["XAU"].iloc[0])
rsi = float(last["RSI14"].iloc[0])
anomaly = bool(last["Unusual"].iloc[0])

# ────────────── اتخاذ القرار النهائي ──────────────
rf_pred = int(rf.predict([last[features]])[0])
decision = make_decision(rf_pred, pred_price, current_price, rsi, anomaly)

# حساب الثقة
conf = confidence_score(rf_pred, pred_price, current_price, rsi, anomaly)

# ────────────── Stop Loss / Take Profit باستخدام ATR ──────────────
atr = last["ATR"].iloc[0]
sl, tp = atr_sl_tp(current_price, atr)

# ────────────── عرض المعلومات ──────────────
st.markdown(f"**Current Price:** {current_price:.2f}")
st.markdown(f"**Predicted Price (LSTM):** {pred_price:.2f}")
st.markdown(f"**Confidence:** {conf}%")

# تحديد لون التوصية
if decision == "BUY":
    color = "green"
elif decision == "SELL":
    color = "red"
else:
    color = "orange"

st.markdown(f"**Decision:** <span style='color:{color}; font-weight:bold'>{decision}</span>", unsafe_allow_html=True)
st.markdown(f"**Stop Loss:** {sl:.2f} | **Take Profit:** {tp:.2f}")

# ────────────── عرض الشارت ──────────────
fig = go.Figure()

fig.add_trace(go.Scatter(x=df.index, y=df["XAU"], mode="lines", name="Gold Price",
                         line=dict(color="blue", width=2)))
fig.add_trace(go.Scatter(x=df.index, y=df["EMA20"], mode="lines", name="EMA20",
                         line=dict(color="purple", width=1)))
fig.add_trace(go.Scatter(x=df.index, y=df["EMA50"], mode="lines", name="EMA50",
                         line=dict(color="pink", width=1)))

# إبراز الشراء / البيع / الانتظار بلون خلفية
fig.update_layout(
    title="Gold Price Chart",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    plot_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)

# ────────────── إرسال إشعار Discord إذا كانت الثقة عالية ──────────────
if conf > 75:
    send_discord_alert(
        f"🚀 Strong signal detected!\nPrice: {current_price:.2f}\nPredicted: {pred_price:.2f}\nConfidence: {conf}%\nDecision: {decision}"
    )
