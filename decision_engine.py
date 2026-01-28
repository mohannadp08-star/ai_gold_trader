# decision_engine.py


def make_decision(rf_pred, pred_price, current_price, rsi, anomaly):
if anomaly:
return "HOLD"
if rf_pred == 1 and rsi < 70:
return "BUY"
elif rf_pred == 0 and rsi > 30:
return "SELL"
return "HOLD"

