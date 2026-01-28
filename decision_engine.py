def decide_trade(predicted_price, confidence):
    """
    اتخاذ القرار BUY / SELL / HOLD بناءً على السعر المتوقع والثقة
    """
    # تأكد أن predicted_price عدد (float) وليس Series
    if hasattr(predicted_price, "iloc"):
        price = float(predicted_price.iloc[-1])
    else:
        price = float(predicted_price)

    if confidence > 0.8:
        return "BUY" if price > 0 else "SELL"
    return "HOLD"
