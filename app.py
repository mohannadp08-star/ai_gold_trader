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

# جلب بيانات الذهب
df = fetch_gold_data()

# حساب المؤشرات الفنية
df = compute_indicators(df)

# إضافة خصائص Quant
df = add_quant_features(df)

# ميزات النموذج
features = ["XAU","EMA20","EMA50","RSI14","Return_5","Volatility","Momentum","Unusual"]

# تدريب نموذج Random Forest
if not df.empty:
    rf = train_rf(df, features)
    last = df.iloc[-1]
    rf_pred = rf.predict([last[features]])[0]

    # بيانات التوقعات
    pred_price = float(last["XAU"]) + 0.1
    current_price = float(last["XAU"])
    rsi = float(last["RSI14"])
    anomaly = last["Unusual"].any() if hasattr(last["Unusual"], "__iter__") else bool(last["Unusual"])

    # القرار النهائي
    decision = make_decision(rf_pred, pred_price, current_price, rsi, anomaly)

    # إشعار Discord
    send_discord_alert(decision, current_price, pred_price)

    # عرض المعلومات
    st.metric("Current Price", current_price)
    st.metric("Predicted Price (LSTM)", pred_price)
    st.metric("Decision", decision)

    # شارت تفاعلي
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["XAU"], mode="lines", name="XAU"))
    fig.update_layout(title="Gold Price Chart", xaxis_title="Time", yaxis_title="Price (USD)")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No data available to train the model.")
