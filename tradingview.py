from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random

# Track added stocks to prevent duplicates
already_added = set()

def add_stocks(driver, stocks):
    global already_added
    
    if not stocks:
        return

    wait = WebDriverWait(driver, 20)

    try:
        print(f"Navigating to TradingView to add: {stocks}")
        driver.get("https://www.tradingview.com/chart/")
        time.sleep(8)  # Let the interactive chart load

        try:
            add_icon = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[@data-name='add-symbol-button' or contains(@aria-label, 'Add symbol')]")
            ))
            add_icon.click()
        except:
            print("Trying keyboard shortcut...")
            webdriver.ActionChains(driver).send_keys(Keys.INSERT).perform()

        time.sleep(1)
        search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-role='search']")))

        for stock in stocks:
            if stock in already_added:
                continue
                
            try:
                search_box.clear()
                search_box.send_keys(stock)
                time.sleep(random.uniform(1.5, 2.5))  # Anti-ban behavior 
                search_box.send_keys(Keys.ENTER)
                
                print(f"Injected {stock} into TV Watchlist")
                already_added.add(stock)
                time.sleep(random.uniform(0.5, 1.0))
            except Exception as e:
                print(f"Error adding {stock}: {e}")

    except Exception as e:
        print(f"TradingView Integration Error: {e}")
