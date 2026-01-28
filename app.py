# app.py
import streamlit as st
from data_fetch import fetch_gold_data
from analysis import compute_indicators
from quant_features import add_quant_features
from ml_model import train_lstm, predict_lstm, train_rf
from decision_engine import make_decision
from alerts import send_discord_alert
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="🤖 Auto AI Gold Trader", layout="wide")
st.title("🤖 Auto AI Gold Trader – تداول ذهب آلي بالذكاء الاصطناعي")

# جلب البيانات
df = fetch_gold_data()
if df.empty:
    st.error("لا توجد بيانات متاحة! تحقق من الاتصال بالإنترنت.")
    st.stop()

# حساب المؤشرات والميزات
df = compute_indicators(df)
df = add_quant_features(df)

# ميزات Random Forest
features = ["EMA20", "EMA50", "RSI14", "Return_5", "Volatility", "Momentum", "Unusual"]

# تدريب النماذج
rf = train_rf(df, features)
lstm_model = train_lstm(df)  # يحمل أو يدرب LSTM تلقائيًا

# آخر صف
last = df.iloc[-1]
current_price = float(last["XAU"])
rsi = float(last["RSI14"])
anomaly = bool(last["Unusual"])

# توقع Random Forest
rf_pred = rf.predict([last[features]])[0]  # 1 = صعود، 0 = هبوط

# توقع LSTM (السعر المتوقع للخطوة التالية)
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler().fit(df['XAU'].values.reshape(-1, 1))  # scaler مؤقت للتنبؤ
pred_price = predict_lstm(lstm_model, df, scaler)

# اتخاذ القرار النهائي
decision = make_decision(rf_pred, pred_price, current_price, rsi, anomaly)

# إرسال تنبيه Discord
send_discord_alert(decision, current_price, pred_price)

# عرض النتائج في أعمدة جميلة
col1, col2, col3, col4 = st.columns(4)
col1.metric("السعر الحالي", f"${current_price:,.2f}")
col2.metric("السعر المتوقع (LSTM)", f"${pred_price:,.2f}", delta=f"{pred_price - current_price:.2f}")
col3.metric("ثقة القرار", "عالية" if abs(pred_price - current_price) > 10 else "متوسطة")
col4.metric("القرار", decision, delta_color="normal" if decision == "HOLD" else "positive" if decision == "BUY" else "negative")

# حساب SL و TP بسيط (يمكن تحسينه)
sl = current_price * 0.99 if decision == "BUY" else current_price * 1.01
tp = current_price * 1.02 if decision == "BUY" else current_price * 0.98

st.markdown(f"**Stop Loss**: ${sl:,.2f} | **Take Profit**: ${tp:,.2f}")

# شارت تفاعلي مع إشارة القرار
fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index, open=df['XAU'], high=df['XAU'], low=df['XAU'], close=df['XAU'], name="XAU"))
fig.add_trace(go.Scatter(x=df.index[-10:], y=[pred_price]*10, mode="lines", name="LSTM Prediction", line=dict(color='orange', dash='dash')))
fig.add_hline(y=sl, line_dash="dot", annotation_text="SL", annotation_position="bottom right", line_color="red")
fig.add_hline(y=tp, line_dash="dot", annotation_text="TP", annotation_position="top right", line_color="green")
fig.update_layout(title="Gold Price Chart مع توقع LSTM", xaxis_title="التاريخ", yaxis_title="السعر (USD)", height=600)
st.plotly_chart(fig, use_container_width=True)
