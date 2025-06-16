from __future__ import annotations
import logging
from datetime import datetime, timedelta
from typing import List, Callable
import ccxt, pandas as pd

logger = logging.getLogger(__name__)

def default_supply_fetcher(symbol: str) -> float:
    """Placeholder – return circulating supply for <symbol> or 0 if unavailable."""
    return 0.0  # plug in external API here

class UniverseFilter:
    """Filter symbols by ADV and market-cap thresholds."""
    def __init__(
        self,
        *,
        min_adv_usd: float,
        min_mcap_usd: float,
        exchange: str = "binance",
        supply_fetcher: Callable[[str], float] = default_supply_fetcher,
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
        tradable: List[str] = []
        for s in symbols:
            try:
                adv, mcap = self._adv(s), self._mcap(s)
                if adv >= self.min_adv and mcap >= self.min_mcap:
                    tradable.append(s)
                else:
                    logger.info("UniverseFilter drop %s adv=%.0f mcap=%.0f", s, adv, mcap)
            except Exception as exc:  # noqa: BLE001
                logger.warning("UniverseFilter error %s: %s", s, exc)
        return tradable
