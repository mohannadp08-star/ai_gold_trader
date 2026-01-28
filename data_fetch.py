# data_fetch.py
import yfinance as yf
import pandas as pd


def fetch_gold_data():
df = yf.download("GC=F", period="60d", interval="1h")
df = df[['Close']].rename(columns={'Close':'XAU'})
df.index = pd.to_datetime(df.index)
return df
