def calculate_atr(df, period=14):
    """
    حساب ATR (Average True Range) للـ Stop Loss / Take Profit.
    """
    df["H-L"] = df["High"] - df["Low"]
    df["H-PC"] = abs(df["High"] - df["XAU"].shift(1))
    df["L-PC"] = abs(df["Low"] - df["XAU"].shift(1))
    df["TR"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1)
    df["ATR"] = df["TR"].rolling(period).mean()
    return df

def atr_sl_tp(current_price, atr, multiplier=1.5):
    sl = current_price - atr * multiplier
    tp = current_price + atr * multiplier
    return sl, tp
