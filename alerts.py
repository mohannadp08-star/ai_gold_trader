import requests
import streamlit as st


DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1466040458961490143/Ys55zLGhmromUN0HIbxi_nz6i23iu2shRFijHVX6wQ-mbaxpi06nCZOFHsNm8_03fcgw"


def send_discord_alert(decision, current_price, pred_price):
try:
content = f"Decision: {decision}\nCurrent Price: {current_price}\nPredicted Price: {pred_price}"
requests.post(DISCORD_WEBHOOK, json={"content": content})
st.info("Alert sent successfully!")
except Exception as e:
st.error(f"Failed to send Discord alert: {e}")
