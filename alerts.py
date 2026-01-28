from discord_webhook import DiscordWebhook

WEBHOOK_URL = "https://discord.com/api/webhooks/1466040458961490143/Ys55zLGhmromUN0HIbxi_nz6i23iu2shRFijHVX6wQ-mbaxpi06nCZOFHsNm8_03fcgw"

def send_discord_alert(decision, price, confidence):
    try:
        webhook = DiscordWebhook(url=WEBHOOK_URL, content=f"{decision} signal: {price:.2f} (Confidence: {confidence:.2f})")
        webhook.execute()
    except Exception as e:
        print(f"Discord alert failed: {e}")
