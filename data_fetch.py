import yfinance as yf
import pandas as pd

def fetch_gold_data():
    """
    تحميل بيانات الذهب من Yahoo Finance
    """
    try:
        df = yf.download("GC=F", period="60d", interval="1h")
        df = df.reset_index()
        df.rename(columns={"Close": "XAU"}, inplace=True)
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()
