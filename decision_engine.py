def make_decision(rf_pred, lstm_pred_price, current_price, rsi, anomaly, confidence_threshold=0.6):
    diff_pct = (lstm_pred_price - current_price) / current_price * 100

    if anomaly:
        return "HOLD", 0.50  # ثقة منخفضة بسبب حركة غير طبيعية

    if rf_pred == 1 and diff_pct > 0.3 and rsi < 68:
        confidence = min(0.95, 0.65 + abs(diff_pct)/5)
        return "BUY", round(confidence, 2)
    elif rf_pred == 0 and diff_pct < -0.3 and rsi > 32:
        confidence = min(0.95, 0.65 + abs(diff_pct)/5)
        return "SELL", round(confidence, 2)
    else:
        return "HOLD", 0.55
