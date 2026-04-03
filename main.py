from scraper import init_driver, get_stock_list
from utils import save_stocks, load_previous, detect_changes, safe_update
from tradingview import add_stocks, remove_stocks
from notifier import send_telegram_message
from config import URL, SCRAPE_INTERVAL

import time
import logging
import random
import os
from datetime import datetime

# Logging setup
base_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(base_dir, "logs")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, "app.log"),
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def run():
    driver = None
    previous = load_previous()

    logging.info("Bot started...")
    logging.info(f"Running with interval: {SCRAPE_INTERVAL}s | URL: {URL}")

    last_heartbeat = time.time()

    while True:
        try:
            if driver is None:
                logging.info("Initializing driver...")
                driver = init_driver()

            # 💓 Heartbeat mechanism
            if time.time() - last_heartbeat > 3600:
                if send_telegram_message("✅ Bot is alive and actively monitoring."):
                    last_heartbeat = time.time()
                else:
                    logging.warning("Heartbeat Telegram notification failed.")

            current = get_stock_list(driver, URL)

            # 🧪 Data Validation
            if not isinstance(current, list):
                logging.warning("Invalid scraper output - skipping iteration")
                time.sleep(5)
                continue

            added, removed = detect_changes(previous, current)

            if added or removed:
                update_success = True

                if added:
                    logging.info(f"New stocks detected: {added}")
                    
                    now = datetime.now().strftime("%H:%M:%S")
                    formatted_msg = f"⏱ {now}\n🚀 New Stocks:\n\n" + "\n".join(added)
                    if not send_telegram_message(formatted_msg):
                        logging.warning("Telegram notification failed for added stocks")

                    # 🔁 SAFE UPDATE
                    success = safe_update(driver, added, add_stocks)
                    update_success = success

                    if success:
                        logging.info("TradingView updated successfully")
                    else:
                        logging.error("Failed to update TradingView")

                if removed:
                    logging.info(f"Removed stocks: {removed}")
                    now = datetime.now().strftime("%H:%M:%S")
                    if not send_telegram_message(f"⏱ {now}\n❌ Removed:\n" + "\n".join(removed)):
                        logging.warning("Telegram notification failed for removed stocks")

                    # Wire removal into TradingView
                    remove_success = safe_update(driver, removed, remove_stocks)
                    if not remove_success:
                        logging.error("Failed to remove stocks from TradingView")
                        update_success = False

                # 🧠 State Safety Check
                if update_success:
                    save_stocks(current)
                    previous = current
                else:
                    logging.warning("State not saved due to TradingView update failure")

            else:
                logging.info("No changes detected")
                
            # 🧠 Anti-ban rate control with random jitter
            base = SCRAPE_INTERVAL
            jitter = random.uniform(-0.2 * base, 0.3 * base)
            delay_time = max(10, base + jitter)
            print(f"Sleeping for {delay_time:.2f} seconds...")
            time.sleep(delay_time)

        except Exception as e:
            logging.error(f"Critical error: {e}")
            
            if driver:
                try:
                    driver.quit()
                except Exception:
                    pass
            
            driver = None  # forces re-init on next loop iteration
            time.sleep(10)

if __name__ == "__main__":
    run()
