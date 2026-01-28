import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1466040458961490143/Ys55zLGhmromUN0HIbxi_nz6i23iu2shRFijHVX6wQ-mbaxpi06nCZOFHsNm8_03fcgw"

def send_discord_alert(decision, current_price, predicted_price):
    try:
        data = {
            "content": f"Decision: {decision}\nCurrent: {current_price}\nPredicted: {predicted_price}"
        }
        requests.post(WEBHOOK_URL, json=data)
    except Exception as e:
        print(f"Failed to send alert: {e}")
