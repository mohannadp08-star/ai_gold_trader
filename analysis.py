import numpy as np

def compute_indicators(df):
    df["EMA20"] = df["XAU"].ewm(span=20).mean()
    df["EMA50"] = df["XAU"].ewm(span=50).mean()

    delta = df["XAU"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    rs = gain.rolling(14).mean() / loss.rolling(14).mean()
    df["RSI14"] = 100 - (100 / (1 + rs))

    df["Return"] = df["XAU"].pct_change()
    df["Unusual"] = abs(df["Return"]) > df["Return"].std() * 2

    return df.dropna()
