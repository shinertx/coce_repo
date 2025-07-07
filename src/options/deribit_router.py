from __future__ import annotations

import os
from typing import Any, Dict, Mapping, cast

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException
from urllib3.util import Retry
from dotenv import load_dotenv

load_dotenv()


class DeribitRouter:
    """Simple router for Deribit option trading."""

    BASE = "https://www.deribit.com/api/v2/"

    def __init__(self) -> None:
        """Create a session and authenticate using environment credentials."""

        self.client_id: str | None = os.getenv("DERIBIT_CLIENT_ID")
        self.client_secret: str | None = os.getenv("DERIBIT_CLIENT_SECRET")
        if not self.client_id or not self.client_secret:
            raise ValueError("Missing Deribit credentials")

        self.session = requests.Session()
        adapter = HTTPAdapter(
            max_retries=Retry(total=3, backoff_factor=0.5, status_forcelist=[502, 503, 504])
        )
        self.session.mount("https://", adapter)
        self.token: str | None = None
        self.authenticate()

    def authenticate(self) -> None:
        """Obtain an access token from Deribit."""

        payload: Dict[str, str] = {
            "client_id": cast(str, self.client_id),
            "client_secret": cast(str, self.client_secret),
            "grant_type": "client_credentials",
        }
        resp = self._post("public/auth", payload)
        data = resp.json()
        self.token = cast(Dict[str, Any], data)["result"]["access_token"]
        self.session.headers["Authorization"] = f"Bearer {self.token}"

    def fetch_price(self, symbol: str) -> float:
        """Latest trade price for ``symbol``."""

        resp = self._get(
            "public/get_last_trades_by_instrument",
            {"instrument_name": symbol, "count": "1"},
        )
        data = resp.json()
        return float(cast(Dict[str, Any], data)["result"]["trades"][0]["price"])

    def place_order(
        self, symbol: str, side: str, size: float, price: float | None = None
    ) -> Dict[str, Any]:
        """Place a limit order and return the API response."""

        resp = self._post(
            f"private/{'buy' if side == 'buy' else 'sell'}",
            {
                "instrument_name": symbol,
                "amount": str(size),
                "type": "limit",
                "price": str(price) if price is not None else None,
            },
        )
        return cast(Dict[str, Any], resp.json())

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get(self, endpoint: str, params: Dict[str, str]) -> requests.Response:
        url = self.BASE + endpoint
        try:
            resp = self.session.get(url, params=params, timeout=10)
            resp.raise_for_status()
            return resp
        except RequestException as exc:
            raise RuntimeError(f"GET {endpoint} failed: {exc}") from exc

    def _post(self, endpoint: str, params: Mapping[str, str | None]) -> requests.Response:
        url = self.BASE + endpoint
        try:
            resp = self.session.post(url, params=params, timeout=10)
            resp.raise_for_status()
            return resp
        except RequestException as exc:
            raise RuntimeError(f"POST {endpoint} failed: {exc}") from exc
