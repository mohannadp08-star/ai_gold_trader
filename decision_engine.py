def make_decision(rf_signal, lstm_price, current_price, rsi, anomaly):
    """
    القرار النهائي للنظام
    جميع المتغيرات يجب أن تكون قيم مفردة (int, float, bool)
    
    rf_signal   : int   -> 1 إذا RF يتوقع صعود، 0 إذا هبوط
    lstm_price  : float -> السعر المتوقع من LSTM
    current_price: float -> السعر الحالي
    rsi         : float -> مؤشر القوة النسبية RSI
    anomaly     : bool  -> True إذا سلوك شاذ
    """

    # شراء
    if rf_signal == 1 and lstm_price > current_price and rsi < 70 and not anomaly:
        return "BUY"

    # بيع
    elif rf_signal == 0 and lstm_price < current_price and rsi > 30 and not anomaly:
        return "SELL"

    # الاحتفاظ
    else:
        return "HOLD"
