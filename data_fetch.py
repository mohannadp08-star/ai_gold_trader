# data_fetch.py
import yfinance as yf
import pandas as pd

def fetch_gold_data():
    df = yf.download("GC=F", period="90d", interval="1h", auto_adjust=True)

    if df.empty:
        return df

    # 🧠 إصلاح مشكلة MultiIndex القادمة من yfinance
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()

    # توحيد أسماء الأعمدة
    df.rename(columns={
        "Datetime": "Date",
        "Close": "Close",
        "Open": "Open",
        "High": "High",
        "Low": "Low",
        "Volume": "Volume"
    }, inplace=True)

    return df
