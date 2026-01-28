# quant_features.py
import pandas as pd


def add_quant_features(df):
df['Volatility'] = df['XAU'].rolling(window=10).std()
df['Momentum'] = df['XAU'] - df['XAU'].shift(10)
df['Unusual'] = (df['Return_5'].abs() > 0.02)
return df
