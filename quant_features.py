import numpy as np

def add_quant_features(df):
    df["Return_5"] = df["XAU"].pct_change(5)
    df["Volatility"] = df["Return"].rolling(10).std()
    df["Momentum"] = df["XAU"] - df["XAU"].shift(10)
    df["Trend_EMA"] = df["EMA20"] - df["EMA50"]
    df["RSI_zone"] = np.where(df["RSI14"] > 70, 1,
                       np.where(df["RSI14"] < 30, -1, 0))
    return df.dropna()
