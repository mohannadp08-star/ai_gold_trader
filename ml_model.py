from sklearn.ensemble import RandomForestClassifier

def train_rf(df, features):
    if df.empty:
        return None

    X = df[features]
    y = df["Unusual"]  # مثال على الهدف
    model = RandomForestClassifier(n_estimators=200)
    model.fit(X, y)
    return model
