def calculate_atr(df, period=14):
    df["H-L"] = df["High"] - df["Low"]
    df["H-PC"] = abs(df["High"] - df["XAU"].shift())
    df["L-PC"] = abs(df["Low"] - df["XAU"].shift())
    df["TR"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1)
    df["ATR"] = df["TR"].rolling(period).mean()
    return df

def atr_sl_tp(price, atr):
    sl = price - atr * 1.5
    tp = price + atr * 3
    return sl, tp
