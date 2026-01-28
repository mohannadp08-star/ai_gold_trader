# analysis.py
import pandas as pd


def compute_indicators(df):
df['EMA20'] = df['XAU'].ewm(span=20, adjust=False).mean()
df['EMA50'] = df['XAU'].ewm(span=50, adjust=False).mean()
delta = df['XAU'].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)
avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()
rs = avg_gain / avg_loss
df['RSI14'] = 100 - (100 / (1 + rs))
df['Return_5'] = df['XAU'].pct_change(5)
return df
