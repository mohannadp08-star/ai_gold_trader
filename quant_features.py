def add_quant_features(df):
    """
    إضافة ميزات Quantية إضافية (لـ Random Forest).
    """
    df["Feature1"] = df["Return_5"] * df["Momentum"]
    df["Feature2"] = df["Volatility"] / (df["RSI14"] + 1)
    return df
