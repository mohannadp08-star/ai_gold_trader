def make_decision(rf_pred, pred_price, current_price, rsi, anomaly):
    if anomaly:
        return "ALERT"
    elif rf_pred:
        return "BUY" if pred_price > current_price else "SELL"
    else:
        return "HOLD"
