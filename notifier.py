import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_message(message):
    # Failsafe if tokens aren't configured yet
    if TELEGRAM_TOKEN == "your_bot_token":
        print("Skipping Telegram Alert: Bot token and Chat ID not configured in config.py")
        return False
        
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, data=payload)
        return response.status_code == 200
    except Exception as e:
        print("Telegram error:", e)
        return False
