from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Callable, List

import ccxt
import pandas as pd

from .supply import coingecko_supply

logger = logging.getLogger(__name__)


class UniverseFilter:
    """Filter symbols by ADV and market-cap thresholds."""

    def __init__(
        self,
        *,
        min_adv_usd: float,
        min_mcap_usd: float,
        exchange: str = "binance",
        supply_fetcher: Callable[[str], float] = coingecko_supply,
    ) -> None:
        self.min_adv, self.min_mcap = min_adv_usd, min_mcap_usd
        self.ex = getattr(ccxt, exchange)({"enableRateLimit": True})
        self.supply_fetcher = supply_fetcher

    def _adv(self, symbol: str, days: int = 30) -> float:
        since = int((datetime.utcnow() - timedelta(days=days)).timestamp() * 1000)
        ohlcv = self.ex.fetch_ohlcv(symbol, "1d", since=since, limit=days)
        df = pd.DataFrame(ohlcv, columns=["ts", "o", "h", "l", "c", "v"])
        return float((df["c"] * df["v"]).mean())

    def _mcap(self, symbol: str) -> float:
        price = self.ex.fetch_ticker(symbol)["last"]
        supply = self.supply_fetcher(symbol)
        return price * supply if supply > 0 else 0.0

    def filter(self, symbols: List[str]) -> List[str]:
        """Return symbols passing ADV and market-cap thresholds."""

        tradable: List[str] = []
        for s in symbols:
            try:
                adv, mcap = self._adv(s), self._mcap(s)
                if adv >= self.min_adv and mcap >= self.min_mcap:
                    tradable.append(s)
                    logger.info(f"Universe OK: {s} ADV={adv:.0f} MCAP={mcap:.0f}")
                else:
                    logger.info(f"Universe drop: {s} ADV={adv:.0f} MCAP={mcap:.0f}")
            except Exception as exc:
                logger.warning(f"UniverseFilter error {s}: {exc}")
        return tradable
