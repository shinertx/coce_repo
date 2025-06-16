from __future__ import annotations
from datetime import datetime
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
        ohlcv = self.ex.fetch_ohlcv(symbol, timeframe, since=int(start.timestamp() * 1000), limit=limit)
        df = pd.DataFrame(ohlcv, columns=["ts", "o", "h", "l", "c", "v"])
        df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
        return df.set_index("ts").loc[start:end]
