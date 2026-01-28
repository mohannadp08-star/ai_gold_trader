def add_quant_features(df):
    """
    يمكن إضافة خصائص Quant إضافية هنا
    """
    if df.empty:
        return df
    # مثال: نسخ مؤشرات موجودة
    df["Feature1"] = df["EMA20"] - df["EMA50"]
    df["Feature2"] = df["Momentum"] * df["Volatility"]
    return df
