def confidence_score(rf, lstm_price, current, rsi, anomaly):
    score = 0
    if rf == 1: score += 30
    if lstm_price > current: score += 30
    if 30 < rsi < 70: score += 20
    if not anomaly: score += 20
    return score
