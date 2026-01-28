from sklearn.ensemble import RandomForestClassifier

def train_rf(df, features):
    df["Target"] = (df["XAU"].shift(-1) > df["XAU"]).astype(int)
    df = df.dropna()

    X = df[features]
    y = df["Target"]

    model = RandomForestClassifier(n_estimators=200)
    model.fit(X, y)

    return model
