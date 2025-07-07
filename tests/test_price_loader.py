from datetime import datetime, timedelta, timezone
import pandas as pd
from src.data_ingest.price_loader import PriceLoader

def test_loader(monkeypatch):
    pl = PriceLoader()
    monkeypatch.setattr(
        pl.ex, "fetch_ohlcv",
        lambda *a, **k: [[0,1,1,1,1,10],[60_000,1,1,1,1,11]]
    )
    df = pl.load(
        "BTC/USDT",
        datetime(1970, 1, 1, tzinfo=timezone.utc),
        datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(minutes=1),
    )
    assert isinstance(df, pd.DataFrame)


def test_loader_retries(monkeypatch):
    pl = PriceLoader()
    calls = {"n": 0}

    def fail_once(*a, **k):
        if calls["n"] == 0:
            calls["n"] += 1
            raise Exception("oops")
        return [[0, 1, 1, 1, 1, 10], [60_000, 1, 1, 1, 1, 11]]

    monkeypatch.setattr(pl.ex, "fetch_ohlcv", fail_once)
    df = pl.load(
        "BTC/USDT",
        datetime(1970, 1, 1, tzinfo=timezone.utc),
        datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(minutes=1),
    )
    assert not df.empty
