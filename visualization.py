import plotly.graph_objects as go

def plot_signals(df, predicted_price, decision):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Close Price"))
    fig.add_trace(go.Scatter(x=[df.index[-1]], y=[predicted_price], mode="markers", marker=dict(color="red", size=10), name="Predicted Price"))
    return fig
