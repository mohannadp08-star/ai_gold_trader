import pandas as pd
import numpy as np

def compute_indicators(df):
    """
    EMA, RSI, Return, Volatility, Momentum
    """
    if df.empty:
        return df

    df["EMA20"] = df["XAU"].ewm(span=20, adjust=False).mean()
    df["EMA50"] = df["XAU"].ewm(span=50, adjust=False).mean()

    delta = df["XAU"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["RSI14"] = 100 - (100 / (1 + rs))

    df["Return_5"] = df["XAU"].pct_change(5)
    df["Volatility"] = df["XAU"].rolling(window=20).std()
    df["Momentum"] = df["XAU"] - df["XAU"].shift(10)

    df["Unusual"] = np.where(abs(df["Return_5"]) > 0.02, True, False)
    df.fillna(0, inplace=True)
    return df
