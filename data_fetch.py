import yfinance as yf
import pandas as pd

CACHE_FILE = "gold_data.csv"

def fetch_gold_data():
    """
    جلب بيانات الذهب التاريخية من Yahoo Finance
    أو تحميلها من الكاش المحلي إذا كان موجودًا
    """
    try:
        df = pd.read_csv(CACHE_FILE, index_col=0, parse_dates=True)
        print("Loaded cached data")
    except FileNotFoundError:
        print("Fetching data from Yahoo Finance...")
        df = yf.download("GC=F", start="2020-01-01", interval="1d")
        df.to_csv(CACHE_FILE)
    return df
