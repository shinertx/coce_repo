import pandas as pd
from src.options.screener import find_candidates


def test_find_candidates():
    cfg = {"days_to_expiry": [1]}
    df = find_candidates(cfg)
    assert isinstance(df, pd.DataFrame)
    assert {"symbol", "price", "size", "expiry"}.issubset(df.columns)
