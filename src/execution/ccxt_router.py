from __future__ import annotations
import os, logging, ccxt
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class CcxtRouter:
    """Thin wrapper over ccxt for order placement."""
    def __init__(self, exchange: str = "binance") -> None:
        klass = getattr(ccxt, exchange)
        self.client = klass(
            {"apiKey": os.getenv("EXCHANGE_API_KEY"), "secret": os.getenv("EXCHANGE_API_SECRET")}
        )

    def place_order(self, symbol: str, side: str, size: float, price: float | None = None):
        if price:
            return self.client.create_limit_order(symbol, side, size, price)
        return self.client.create_market_order(symbol, side, size)
