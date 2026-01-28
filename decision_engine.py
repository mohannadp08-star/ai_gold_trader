def make_decision(rf_pred, pred_price, current_price, rsi, anomaly):
    """
    اتخاذ القرار النهائي: BUY / SELL / HOLD
    """
    if anomaly:
        return "HOLD"
    if rf_pred == 1 and pred_price > current_price and rsi < 70:
        return "BUY"
    elif rf_pred == 0 and pred_price < current_price and rsi > 30:
        return "SELL"
    else:
        return "HOLD"
