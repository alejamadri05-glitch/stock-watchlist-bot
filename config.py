import os
from dotenv import load_dotenv

load_dotenv()  # Loads credentials from .env file — never hardcode secrets!

URL = "https://tradefinder.in/market-pulse"
SCRAPE_INTERVAL = 60  # seconds

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
