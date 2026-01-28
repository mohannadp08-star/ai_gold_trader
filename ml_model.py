import numpy as np

def load_models():
    """
    Placeholder لتحميل نماذج LSTM و RandomForest
    """
    lstm_model = None
    rf_model = None
    return lstm_model, rf_model

def predict(df, lstm_model, rf_model):
    """
    توقع السعر باستخدام LSTM (سلسلة) و Random Forest (تصنيف)
    هنا نستخدم قيمة بسيطة للعرض التجريبي
    """
    # إذا df فارغ، نرجع 0
    if df.empty:
        predicted_price = 0.0
    else:
        # خذ آخر سعر وأضف زيادة 1% كمثال
        predicted_price = float(df["Close"].iloc[-1] * 1.01)

    confidence = 0.85  # قيمة تجريبية
    return predicted_price, confidence
