import yfinance as yf
import pandas as pd

def fetch_gold_data():
    """
    تحميل بيانات الذهب (XAU/USD) من Yahoo Finance.
    """
    try:
        df = yf.download("GC=F", period="60d", interval="1h")
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        df.rename(columns={'Close':'XAU'}, inplace=True)
        df.index = pd.to_datetime(df.index)
        return df
    except Exception as e:
        print("Error fetching data:", e)
        return pd.DataFrame()
