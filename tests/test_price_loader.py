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
        datetime.now(timezone.utc) - timedelta(days=1),
        datetime.now(timezone.utc),
    )
    assert isinstance(df, pd.DataFrame)
