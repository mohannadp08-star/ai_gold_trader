import plotly.graph_objects as go

def plot_gold_chart(df, pred_price=None, sl=None, tp=None):
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['XAU'], high=df['XAU'], low=df['XAU'], close=df['XAU'],
        name='Gold Price'
    ))

    fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], name='EMA20', line=dict(color='orange')))
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA50'], name='EMA50', line=dict(color='purple')))

    if pred_price:
        fig.add_hline(y=pred_price, line_dash="dash", line_color="blue", annotation_text="Predicted")

    if sl:
        fig.add_hline(y=sl, line_dash="dot", line_color="red", annotation_text="SL")
    if tp:
        fig.add_hline(y=tp, line_dash="dot", line_color="green", annotation_text="TP")

    fig.update_layout(title="Gold Price & Signals", xaxis_title="Time", yaxis_title="Price (USD)")
    return fig
