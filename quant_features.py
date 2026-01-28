# quant_features.py

import pandas as pd

def add_quant_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add extra engineered features for ML models.
    Currently minimal – can be expanded later with MACD, ATR, OBV, etc.
    """
    # Placeholder - return the same dataframe
    # You can add code here later, for example:
    # df['MACD'] = ... 
    # df['Signal'] = ...
    return df
