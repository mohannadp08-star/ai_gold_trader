import pandas as pd
import numpy as np

def simple_backtest(df, decisions):
    # decisions: list of "BUY"/"SELL"/"HOLD"
    returns = df['XAU'].pct_change().fillna(0)
    strategy_returns = pd.Series(0.0, index=returns.index)

    position = 0
    for i, dec in enumerate(decisions):
        if dec == "BUY":
            position = 1
        elif dec == "SELL":
            position = -1
        strategy_returns.iloc[i] = position * returns.iloc[i]

    cum_ret = (1 + strategy_returns).cumprod() - 1
    sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252*24) if strategy_returns.std() != 0 else 0
    max_dd = (cum_ret.cummax() - cum_ret).max()

    return {
        "Cumulative Return": cum_ret.iloc[-1],
        "Sharpe Ratio": sharpe,
        "Max Drawdown": max_dd
    }
