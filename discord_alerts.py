import requests
import streamlit as st

WEBHOOK_URL = st.secrets.get("https://discord.com/api/webhooks/1466040458961490143/Ys55zLGhmromUN0HIbxi_nz6i23iu2shRFijHVX6wQ-mbaxpi06nCZOFHsNm8_03fcgw")

def send_discord_alert(message):
    if not WEBHOOK_URL:
        print("Webhook URL not set")
        return
    data = {"content": message}
    try:
        requests.post(WEBHOOK_URL, json=data)
        print("Alert sent successfully!")
    except Exception as e:
        print("Error sending Discord alert:", e)
