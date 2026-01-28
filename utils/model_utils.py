import joblib
import os
from tensorflow.keras.models import load_model, save_model

LSTM_MODEL_PATH = "lstm_gold.h5"
RF_MODEL_PATH = "rf_gold.pkl"

def save_rf(model):
    joblib.dump(model, RF_MODEL_PATH)

def load_rf():
    if os.path.exists(RF_MODEL_PATH):
        return joblib.load(RF_MODEL_PATH)
    return None

def save_lstm(model):
    model.save(LSTM_MODEL_PATH)

def load_lstm():
    if os.path.exists(LSTM_MODEL_PATH):
        return load_model(LSTM_MODEL_PATH)
    return None
