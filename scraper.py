from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os

def init_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Use a LOCAL profile folder to completely avoid Apple/Chrome OSX locking conflicts!
    profile_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bot_profile")
    options.add_argument(f"user-data-dir={profile_dir}")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver

def get_stock_list(driver, url):
    driver.get(url)

    wait = WebDriverWait(driver, 15)

    # Wait for the dynamic React table rows to load that contain the data-key attribute
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr[data-key]")))

    # Select all table rows containing stock keys
    elements = driver.find_elements(By.CSS_SELECTOR, "tr[data-key]")

    stocks = []

    for el in elements:
        # The data-key attribute is formatted as "SYMBOL_INDEX" (e.g. "RELIANCE_1")
        data_key = el.get_attribute("data-key")
        if data_key and "_" in data_key:
            name = data_key.split("_")[0].strip()
            if name:
                stocks.append(name)

    return list(dict.fromkeys(stocks))  # order-preserving deduplication


