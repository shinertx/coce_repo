from __future__ import annotations
import pandas as pd

def volume_zscore(vol: pd.Series, window: int = 30) -> pd.Series:
    return (vol - vol.rolling(window).mean()) / vol.rolling(window).std(ddof=0)
