import pandas as pd

def compute_indicators(df):
    """
    حساب EMA و RSI ومؤشرات أخرى.
    """
    df["EMA20"] = df["XAU"].ewm(span=20, adjust=False).mean()
    df["EMA50"] = df["XAU"].ewm(span=50, adjust=False).mean()
    delta = df["XAU"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df["RSI14"] = 100 - (100 / (1 + rs))
    df["Return_5"] = df["XAU"].pct_change(5)
    df["Volatility"] = df["XAU"].rolling(10).std()
    df["Momentum"] = df["XAU"] - df["XAU"].shift(10)
    df["Trend_EMA"] = df["EMA20"] - df["EMA50"]
    df["Unusual"] = False  # سيتم تحديثه لاحقًا
    return df
