from __future__ import annotations
import pandas as pd

def rolling_corr(price_df: pd.DataFrame, window: int = 30) -> pd.DataFrame:
    """Rolling Pearson correlation matrices."""
    return price_df.pct_change().rolling(window).corr().dropna()
