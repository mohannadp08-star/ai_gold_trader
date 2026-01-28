
import os
import pandas as pd
import yfinance as yf

CACHE_FILE = "gold_data_cache.csv"

def fetch_gold_data(period="60d", interval="1h"):
    if os.path.exists(CACHE_FILE):
        df = pd.read_csv(CACHE_FILE, parse_dates=["Datetime"])
        print("Loaded gold data from local cache.")
        return df.set_index("Datetime")

    try:
        df = yf.download("GC=F", period=period, interval=interval)
        df = df.reset_index()
        df.rename(columns={"Close": "XAU"}, inplace=True)
        df.to_csv(CACHE_FILE, index=False)
        print("Fetched gold data from Yahoo Finance and cached.")
        return df.set_index("Datetime")
    except Exception as e:
        print(f"Failed to fetch data: {e}")
        return pd.DataFrame()
