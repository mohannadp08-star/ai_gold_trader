# ml_model.py
from sklearn.ensemble import RandomForestClassifier


def train_rf(df, features):
df = df.dropna()
if df.empty:
raise ValueError("DataFrame is empty after dropping NaNs")
df['Target'] = (df['XAU'].shift(-1) > df['XAU']).astype(int)
X = df[features]
y = df['Target']
model = RandomForestClassifier(n_estimators=200)
model.fit(X, y)
return model
