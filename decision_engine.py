def decide_trade(predicted_price, confidence):
    if confidence > 0.8:
        return "BUY" if predicted_price > 0 else "SELL"
    return "HOLD"
