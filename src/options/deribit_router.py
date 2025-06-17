from __future__ import annotations

import os
from typing import Any, Dict, cast

import requests
from dotenv import load_dotenv

load_dotenv()


class DeribitRouter:
    """Simple router for Deribit option trading."""

    BASE = "https://www.deribit.com/api/v2/"

    def __init__(self) -> None:
        """Create a session and authenticate using environment credentials."""

        self.client_id = os.getenv("DERIBIT_CLIENT_ID")
        self.client_secret = os.getenv("DERIBIT_CLIENT_SECRET")
        self.session = requests.Session()
        self.token = None
        self.authenticate()

    def authenticate(self) -> None:
        """Obtain an access token from Deribit."""

        payload: Dict[str, str] = {
            "client_id": self.client_id or "",
            "client_secret": self.client_secret or "",
            "grant_type": "client_credentials",
        }
        resp = self.session.post(self.BASE + "public/auth", params=payload)
        resp.raise_for_status()
        data = resp.json()
        self.token = cast(Dict[str, Any], data)["result"]["access_token"]
        self.session.headers["Authorization"] = f"Bearer {self.token}"

    def fetch_price(self, symbol: str) -> float:
        """Latest trade price for ``symbol``."""

        resp = self.session.get(
            self.BASE + "public/get_last_trades_by_instrument",
            params={"instrument_name": symbol, "count": "1"},
        )
        resp.raise_for_status()
        data = resp.json()
        return float(cast(Dict[str, Any], data)["result"]["trades"][0]["price"])

    def place_order(
        self, symbol: str, side: str, size: float, price: float | None = None
    ) -> Dict[str, Any]:
        """Place a limit order and return the API response."""

        resp = self.session.post(
            # TODO: validate live endpoint naming for buy/sell
            self.BASE + f"private/{'buy' if side == 'buy' else 'sell'}",
            params={
                "instrument_name": symbol,
                "amount": str(size),
                "type": "limit",
                "price": str(price) if price is not None else None,
            },
        )
        resp.raise_for_status()
        return cast(Dict[str, Any], resp.json())
