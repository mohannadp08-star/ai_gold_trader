import pandas as pd
import yfinance as yf

def fetch_gold_data():
    df = yf.download("GC=F", period="60d", interval="1h")
    df = df.rename(columns={
        "Close": "XAU",
        "High": "High",
        "Low": "Low"
    })
    return df[["XAU", "High", "Low"]].dropna()
