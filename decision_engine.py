def make_decision(rf_signal, lstm_price, current_price, rsi, anomaly):
    """
    القرار النهائي للنظام:
    - rf_signal: 1 إذا RF يتوقع صعود، 0 إذا هبوط
    - lstm_price: السعر المتوقع من LSTM
    - current_price: السعر الحالي
    - rsi: مؤشر القوة النسبية RSI
    - anomaly: قيمة بوليان True/False (آخر صف فقط)
    """

    # تأكد أن anomaly قيمة مفردة
    if not isinstance(anomaly, bool):
        anomaly = bool(anomaly)

    # شرط شراء
    if rf_signal == 1 and lstm_price > current_price and rsi < 70 and not anomaly:
        return "BUY"

    # شرط بيع
    elif rf_signal == 0 and lstm_price < current_price and rsi > 30 and not anomaly:
        return "SELL"

    # الاحتفاظ
    else:
        return "HOLD"
