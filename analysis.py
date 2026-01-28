import pandas as pd
import numpy as np

def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    # EMA
    df['EMA20'] = df['XAU'].ewm(span=20, adjust=False).mean()
    df['EMA50'] = df['XAU'].ewm(span=50, adjust=False).mean()

    # RSI 14
    delta = df['XAU'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    df['RSI14'] = 100 - (100 / (1 + rs))

    # Returns & Volatility
    df['Return_5'] = df['XAU'].pct_change(5)
    df['Volatility'] = df['XAU'].pct_change().rolling(20).std()

    # Momentum
    df['Momentum'] = df['XAU'] - df['XAU'].shift(10)

    # Simple anomaly detection
    df['Unusual'] = np.abs(df['Return_5']) > 3 * df['Volatility']

    return df.dropna()
