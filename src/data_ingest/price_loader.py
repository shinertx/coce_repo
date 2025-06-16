from __future__ import annotations
from datetime import datetime, timezone
from typing import Literal
import ccxt, pandas as pd

class PriceLoader:
    def __init__(self, exchange: str = "binance") -> None:
        self.ex = getattr(ccxt, exchange)()

    def load(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: Literal["1h", "1d"] = "1d",
        limit: int = 1000,
    ) -> pd.DataFrame:
        start_utc = pd.to_datetime(start, utc=True)
        end_utc = pd.to_datetime(end, utc=True)
        ohlcv = self.ex.fetch_ohlcv(symbol, timeframe, since=int(start_utc.timestamp() * 1000), limit=limit)
        df = pd.DataFrame(ohlcv, columns=["ts", "o", "h", "l", "c", "v"])
        df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
        return df.set_index("ts").loc[start_utc:end_utc]
