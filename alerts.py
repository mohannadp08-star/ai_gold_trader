import requests
import os

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL") or "https://discord.com/api/webhooks/1466040458961490143/Ys55zLGhmromUN0HIbxi_nz6i23iu2shRFijHVX6wQ-mbaxpi06nCZOFHsNm8_03fcgw"

def send_discord_alert(decision, current_price, pred_price, confidence):
    if "YOUR_DISCORD_WEBHOOK_HERE" in WEBHOOK_URL or not WEBHOOK_URL:
        print("Warning: Discord webhook not configured.")
        return

    color = 0x00ff00 if decision == "BUY" else 0xff0000 if decision == "SELL" else 0x808080
    embed = {
        "title": f"Auto AI Gold Trader Signal: **{decision}**",
        "description": f"Current: **${current_price:,.2f}**\nPredicted: **${pred_price:,.2f}**\nConfidence: **{confidence*100:.0f}%**",
        "color": color
    }

    payload = {"embeds": [embed]}
    try:
        requests.post(WEBHOOK_URL, json=payload)
        print("Discord alert sent.")
    except Exception as e:
        print(f"Failed to send Discord alert: {e}")
