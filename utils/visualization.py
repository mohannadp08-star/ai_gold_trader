import plotly.graph_objects as go

def plot_signals(df, predicted_price, decision):
    """
    رسم شارت الذهب مع EMA، إشارة التداول، SL و TP
    """
    current_price = df["Close"].iloc[-1]

    # حساب SL و TP
    price_diff = predicted_price - current_price
    take_profit = current_price + price_diff * 1.5
    stop_loss = current_price - price_diff * 0.5

    fig = go.Figure()

    # --- Close Price ---
    fig.add_trace(go.Scatter(
        x=df.index, y=df["Close"], mode="lines", name="Close Price",
        line=dict(color="blue")
    ))

    # --- EMA20 & EMA50 ---
    if "EMA20" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["EMA20"], mode="lines", name="EMA20",
            line=dict(color="orange", dash="dash")
        ))
    if "EMA50" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["EMA50"], mode="lines", name="EMA50",
            line=dict(color="green", dash="dash")
        ))

    # --- Predicted Price ---
    fig.add_trace(go.Scatter(
        x=[df.index[-1]], y=[predicted_price], mode="markers",
        marker=dict(color="red", size=12), name="Predicted Price"
    ))

    # --- Take Profit ---
    fig.add_t_
