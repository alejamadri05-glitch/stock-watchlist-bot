from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random

# Track added stocks to prevent duplicates
already_added = set()

def _open_search(driver, wait):
    """Navigate to chart and open the symbol search box. Returns the search input element."""
    driver.get("https://www.tradingview.com/chart/")
    time.sleep(8)  # Let the interactive chart load

    try:
        add_icon = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@data-name='add-symbol-button' or contains(@aria-label, 'Add symbol')]")
        ))
        add_icon.click()
    except Exception:
        print("Trying keyboard shortcut...")
        webdriver.ActionChains(driver).send_keys(Keys.INSERT).perform()

    time.sleep(1)
    return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-role='search']")))


def add_stocks(driver, stocks):
    global already_added

    if not stocks:
        return True

    wait = WebDriverWait(driver, 20)

    try:
        print(f"Navigating to TradingView to add: {stocks}")
        _open_search(driver, wait)  # open search once to get the panel visible

        for stock in stocks:
            if stock in already_added:
                continue

            try:
                # Re-fetch inside loop to avoid StaleElementReferenceException
                search_box = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input[data-role='search']")
                ))
                search_box.clear()
                search_box.send_keys(stock)
                time.sleep(random.uniform(1.5, 2.5))  # Anti-ban behavior
                search_box.send_keys(Keys.ENTER)

                print(f"Injected {stock} into TV Watchlist")
                already_added.add(stock)
                time.sleep(random.uniform(0.5, 1.0))
            except Exception as e:
                print(f"Error adding {stock}: {e}")

        return True

    except Exception as e:
        print(f"TradingView Integration Error: {e}")
        return False


def remove_stocks(driver, stocks):
    """
    Remove stocks from TradingView watchlist.
    Navigates to each symbol, right-clicks it in the watchlist, and selects Remove.
    """
    global already_added

    if not stocks:
        return True

    wait = WebDriverWait(driver, 20)

    try:
        print(f"Navigating to TradingView to remove: {stocks}")
        driver.get("https://www.tradingview.com/chart/")
        time.sleep(8)

        for stock in stocks:
            try:
                # Find symbol in the watchlist sidebar
                symbol_el = wait.until(EC.presence_of_element_located(
                    (By.XPATH, f"//span[contains(@class,'symbolName') and text()='{stock}']")
                ))

                # Right-click to bring up context menu
                webdriver.ActionChains(driver).context_click(symbol_el).perform()
                time.sleep(0.8)

                # Click "Remove" in context menu
                remove_btn = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//span[contains(text(),'Remove')]")
                ))
                remove_btn.click()

                print(f"Removed {stock} from TV Watchlist")
                already_added.discard(stock)
                time.sleep(random.uniform(0.5, 1.2))

            except Exception as e:
                print(f"Error removing {stock}: {e}")

        return True

    except Exception as e:
        print(f"TradingView Remove Error: {e}")
        return False

