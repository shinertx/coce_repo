from __future__ import annotations

import logging

import ccxt
from src.infra.secret_provider import get_secret
logger = logging.getLogger(__name__)


class CcxtRouter:
    """Thin wrapper over ccxt for order placement."""

    def __init__(self, exchange: str = "kraken") -> None:
        """Connect to the specified exchange using API keys from the environment."""

        klass = getattr(ccxt, exchange)
        self.client = klass(
            {"apiKey": get_secret("EXCHANGE_API_KEY"), "secret": get_secret("EXCHANGE_API_SECRET")}
        )

    def place_order(self, symbol: str, side: str, size: float, price: float | None = None):
        """Place a limit or market order."""

        if price:
            return self.client.create_limit_order(symbol, side, size, price)
        return self.client.create_market_order(symbol, side, size)

    def fetch_price(self, symbol: str) -> float:
        """Latest traded price from exchange."""
        try:
            return float(self.client.fetch_ticker(symbol)["last"])
        except Exception as exc:  # pragma: no cover - network errors
            logger.error("Price fetch failed %s", exc)
            return 0.0
