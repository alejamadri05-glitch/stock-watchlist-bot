import pandas as pd
import os
import time
import random

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
os.makedirs(data_dir, exist_ok=True)
FILE_PATH = os.path.join(data_dir, "stocks.csv")

def save_stocks(stock_list):
    df = pd.DataFrame(stock_list, columns=["Stock"])
    df.to_csv(FILE_PATH, index=False)

def load_previous():
    if not os.path.exists(FILE_PATH):
        return []

    df = pd.read_csv(FILE_PATH)
    return df["Stock"].tolist()

def detect_changes(old, new):
    added = list(set(new) - set(old))
    removed = list(set(old) - set(new))
    return added, removed

def safe_update(driver, stocks, update_function, retries=3):
    for attempt in range(retries):
        try:
            update_function(driver, stocks)
            return True
        except Exception as e:
            print(f"Retry {attempt+1} failed:", e)
            time.sleep(random.uniform(2, 5))
    return False
