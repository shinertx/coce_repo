from __future__ import annotations
import functools
import logging
import os
import time
from typing import Dict

import requests

logger = logging.getLogger(__name__)

COINGECKO_API_KEY = os.environ.get("COINGECKO_API_KEY", "")

# Map from ticker (BTC, ETH, SOL) to CoinGecko's coin_id
COINGECKO_ID_MAP: Dict[str, str] = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "ADA": "cardano",
    "DOGE": "dogecoin",
    # Add more as needed
}


@functools.lru_cache(maxsize=128)
def coingecko_supply(symbol: str) -> float:
    """Fetch circulating supply from CoinGecko for the base asset of ``symbol``."""
    ticker = symbol.split("/")[0].upper()
    coin_id = COINGECKO_ID_MAP.get(ticker, ticker.lower())
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    headers = {"x-cg-pro-api-key": COINGECKO_API_KEY} if COINGECKO_API_KEY else {}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 429:
            time.sleep(1)
            r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        supply = r.json()["market_data"]["circulating_supply"]
        logger.info(f"CoinGecko supply for {symbol}: {supply}")
        return float(supply)
    except Exception as exc:  # pragma: no cover - network errors
        logger.warning(f"Failed to fetch supply for {symbol}: {exc}")
        return 0.0
