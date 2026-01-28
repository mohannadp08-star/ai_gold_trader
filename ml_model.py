# ml_model.py
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import os

MODEL_PATH = "lstm_gold_model.h5"
LOOKBACK = 60  # عدد الخطوات السابقة (أفضل قيمة لأسعار الذهب)

def prepare_lstm_data(df, lookback=LOOKBACK):
    """تحضير البيانات لـ LSTM: scaling + sequences"""
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df['XAU'].values.reshape(-1, 1))
    
    X, y = [], []
    for i in range(lookback, len(scaled_data)):
        X.append(scaled_data[i-lookback:i, 0])
        y.append(scaled_data[i, 0])
    
    X = np.array(X).reshape((len(X), lookback, 1))
    y = np.array(y)
    
    return X, y, scaler

def train_lstm(df):
    """تدريب نموذج LSTM إذا لم يكن موجودًا"""
    if os.path.exists(MODEL_PATH):
        print("📥 تحميل نموذج LSTM المدرب مسبقًا...")
        return load_model(MODEL_PATH)
    
    print("🧠 تدريب نموذج LSTM جديد...")
    X, y, scaler = prepare_lstm_data(df)
    
    # تقسيم البيانات (80% تدريب)
    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    model = Sequential()
    model.add(LSTM(100, return_sequences=True, input_shape=(LOOKBACK, 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(25))
    model.add(Dense(1))
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    model.fit(X_train, y_train, batch_size=32, epochs=100, validation_data=(X_test, y_test), callbacks=[early_stop], verbose=1)
    
    model.save(MODEL_PATH)
    print("✅ تم حفظ نموذج LSTM في", MODEL_PATH)
    return model

def predict_lstm(model, df, scaler, steps=1):
    """توقع السعر المستقبلي (الخطوة التالية)"""
    scaled_data = scaler.transform(df['XAU'].values[-LOOKBACK:].reshape(-1, 1))
    input_seq = scaled_data.reshape((1, LOOKBACK, 1))
    
    pred_scaled = model.predict(input_seq)
    pred_price = scaler.inverse_transform(pred_scaled)[0][0]
    
    return float(pred_price)

def train_rf(df, features):
    """تدريب Random Forest (كما كان سابقًا)"""
    df['Target'] = (df['XAU'].shift(-1) > df['XAU']).astype(int)
    train_df = df.dropna()
    X = train_df[features]
    y = train_df['Target']
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model
