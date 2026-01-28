import pandas as pd

def compute_indicators(df):
    """
    حساب المؤشرات الفنية: EMA20/50, RSI14, Volatility, Momentum
    """
    # --- تأكد أن العمود Close رقمي ---
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    # إزالة الصفوف التي فيها NaN بعد التحويل
    df = df.dropna(subset=["Close"])

    # EMA
    df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()
    df["EMA50"] = df["Close"].ewm(span=50, adjust=False).mean()

    # RSI14
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df["RSI14"] = 100 - (100 / (1 + rs))

    # Volatility
    df["Volatility"] = df["Close"].pct_change().rolling(20).std()

    # Momentum
    df["Momentum"] = df["Close"] - df["Close"].shift(5)

    return df
