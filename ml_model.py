from sklearn.ensemble import RandomForestClassifier

def train_rf(df, features):
    """
    تدريب نموذج Random Forest.
    """
    df = df.dropna()
    if df.empty:
        raise ValueError("DataFrame فارغ بعد تنظيف البيانات")
    X = df[features]
    y = (df["XAU"].shift(-1) > df["XAU"]).astype(int)  # 1 = صعود
    y = y[:-1]
    X = X[:-1]
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X, y)
    return model
