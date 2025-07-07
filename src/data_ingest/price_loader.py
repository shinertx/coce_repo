from __future__ import annotations
from datetime import datetime
from typing import Literal

import ccxt
import pandas as pd
import logging
import time


class PriceLoader:
    """Fetch OHLCV data from exchanges via ccxt."""

    def __init__(self, exchange: str = "kraken") -> None:
        """Initialize loader with the given exchange."""

        self.ex = getattr(ccxt, exchange)()
        self.logger = logging.getLogger(__name__)

    def load(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: Literal["1h", "1d"] = "1d",
        limit: int = 1000,
    ) -> pd.DataFrame:
        """Return OHLCV frame for ``symbol`` between ``start`` and ``end``."""
        start_utc = pd.to_datetime(start, utc=True)
        end_utc = pd.to_datetime(end, utc=True)
        last_exc: Exception | None = None
        for _ in range(3):
            try:
                ohlcv = self.ex.fetch_ohlcv(
                    symbol,
                    timeframe,
                    since=int(start_utc.timestamp() * 1000),
                    limit=limit,
                )
                break
            except Exception as exc:  # ccxt base error
                last_exc = exc
                self.logger.warning("fetch_ohlcv failed: %s", exc)
                time.sleep(0.5)
        else:
            raise RuntimeError(f"failed to fetch {symbol}") from last_exc

        df = pd.DataFrame(ohlcv, columns=["ts", "o", "h", "l", "c", "v"])
        df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
        return df.set_index("ts").loc[start_utc:end_utc]
