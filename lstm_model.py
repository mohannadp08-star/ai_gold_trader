import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def prepare_lstm(df):
    """
    تحضير بيانات LSTM (سلاسل زمنية).
    """
    df = df[['XAU']].dropna()
    data = df.values
    X, y = [], []
    seq_len = 10
    for i in range(len(data) - seq_len):
        X.append(data[i:i+seq_len])
        y.append(data[i+seq_len])
    X = np.array(X)
    y = np.array(y)
    return X, y

def build_lstm(prepared_data):
    """
    تدريب نموذج LSTM وتوليد توقعات.
    """
    X, y = prepared_data
    model = Sequential()
    model.add(LSTM(50, input_shape=(X.shape[1], X.shape[2])))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=5, batch_size=16, verbose=0)
    pred = model.predict(X, verbose=0)
    pred_series = pd.Series(pred.flatten(), index=pd.date_range(start=0, periods=len(pred)))
    return pred_series
