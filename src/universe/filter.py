import requests
import functools
import os

COINGECKO_API_KEY = os.environ.get("COINGECKO_API_KEY", "")

@functools.lru_cache(maxsize=128)
def coingecko_supply(symbol: str) -> float:
    # symbol expected like "BTC/USDT" → coin_id = "bitcoin"
    coin_id_map = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "SOL": "solana",
        "ADA": "cardano",
        "DOGE": "dogecoin",
        # add more as needed
    }
    ticker = symbol.split("/")[0].upper()
    coin_id = coin_id_map.get(ticker, ticker.lower())
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    headers = {"x-cg-pro-api-key": COINGECKO_API_KEY} if COINGECKO_API_KEY else {}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        return r.json()["market_data"]["circulating_supply"]
    except Exception as exc:
        print(f"[WARN] Failed to fetch supply for {symbol} ({coin_id}): {exc}")
        return 0.0
