def add_quant_features(df):
    # Placeholder لإضافة ميزات كمية إضافية
    df["Momentum"] = df["Close"] - df["Close"].shift(5)
    return df
