# 📈 Automated Quantitative Stock Scanner & TradingView Injector

An enterprise-grade, highly resilient automation pipeline designed to continuously scrape high-momentum stock scanners, detect market shifts in real-time, and seamlessly inject alerts directly into mobile Telegram and TradingView Watchlists. 

This robust tool transforms manual day-trading operations into a completely headless, 24/7 background process.

## 🚀 Key Features

### 1. Zero-Touch TradingView UI Integration
- Automatically injects momentum tickers detected on your customized scanner directly into your pre-existing TradingView watchlists.
- Bypasses traditional API limits by natively interacting with the TradingView client UI.
- Implements state memory algorithms to prevent redundant stock overlap on subsequent runs.

### 2. Bulletproof React Scraper 
- Traditional DOM scrapers fail when website UI shifts. This engine utilizes **Headless Chrome WebDriver** mapped perfectly to static *React Element Data-Keys* (`tr[data-key]`) ensuring it never breaks, even if the target site experiences significant front-end updates and redesigns. 
- Integrated anti-bot flagging methodologies (Jitter timers, Shm-usage bypass, and Blink feature destruction).

### 3. Production-Grade Resiliency
- **Self-Healing WebDrivers:** The core loop detects Selenium crashes, memory leaks, and `ERR_CONNECTION_RESET` exceptions. It will safely terminate and entirely rebuild the WebDriver sandbox during execution to guarantee 100% sustained uptime.
- **Transactional State Operations:** UI integrations are treated strictly as database transactions via a Custom `safe_update` logic wrapper. If the UI injection fails due to network lag, local memory is reverted ensuring data integrity. 

### 4. Direct Telegram Telemetry
- Receives immediate Net-New and Net-Removed alerts sent straight to your pocket via the Telegram Bot API payload.
- Automated 60-Minute Heartbeat signals verify the background process hasn't stalled.

## 🛠️ Tech Stack & Architecture
- **Language:** Python 3.10+
- **Browser Automation:** Selenium, Chrome WebDriver (Service Manager)
- **Networking:** Requests, URL/URI parsing
- **Logging & Tracking:** Built-in explicit Python rotating file-handlers (`/logs/` trace directory).
- **Notification Backbone:** Telegram Bot API (HTTP endpoints).

## ⚙️ How to Deploy

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/stock-watchlist-bot.git
   cd stock-watchlist-bot
   ```

2. **Install Core Dependencies**
   Ensure you have downloaded Python 3 and install the required PIP modules:
   ```bash
   pip install selenium webdriver-manager requests
   ```

3. **Configure Environment Variables**
   Open `config.py` and input your Telegram Bot parameters alongside your preferred Scanner URL:
   ```python
   # config.py
   URL = "https://tradefinder.in/market-pulse" 
   SCRAPE_INTERVAL = 60  
   TELEGRAM_TOKEN = "YOUR_BOT_TOKEN_HERE"
   TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"
   ```

4. **Initialize The Application**
   ```bash
   python3 main.py
   ```
   *Note: On its first run, a sandboxed `bot_profile` dictionary is created. You will need to manually log into your respective TradingView account in that isolated browser window so the session cookies can be preserved for headless utilization!*

## 🧠 Future Roadmap Planning

- **Broker API Implementation:** Re-route the output signal logic to directly interact with Zerodha/Upstox API integrations for fully automated Market Orders.
- **Dockerization Container:** Wrap the dependency graph into a complete `docker-compose.yml` image for zero-friction EC2 or DigitalOcean Droplet deployment.
- **Quantitative ML Filtering:** Pipe the incoming stock detections through simple Moving Average or Exponential ML models to determine "buy grade" prior to alerting.

---
*Built as a scalable execution engine for automated day-trading. Not financial advice.*
