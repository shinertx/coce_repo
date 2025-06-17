from __future__ import annotations
import pandas as pd


def volume_zscore(vol: pd.Series, window: int = 30) -> pd.Series:
    """Z-score of volume relative to a rolling window."""

    return (vol - vol.rolling(window).mean()) / vol.rolling(window).std(ddof=0)
