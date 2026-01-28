import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1466040458961490143/Ys55zLGhmromUN0HIbxi_nz6i23iu2shRFijHVX6wQ-mbaxpi06nCZOFHsNm8_03fcgw"

def send_discord_alert(message):
    data = {"content": message}
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Alert sent successfully!")
    else:
        print("Failed to send alert", response.text)

# مثال استخدام:
send_discord_alert("🚀 Strong BUY signal for XAU/USD! Confidence: 85%")
