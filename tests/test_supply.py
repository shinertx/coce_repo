from src.universe.filter import UniverseFilter
from src.universe import supply as supply_mod


class DummyResponse:
    def __init__(self, data):
        self.data = data
        self.status_code = 200

    def raise_for_status(self):
        pass

    def json(self):
        return self.data


def test_coingecko_supply(monkeypatch):
    def fake_get(*args, **kwargs):
        return DummyResponse({"market_data": {"circulating_supply": 1_000_000_000}})

    monkeypatch.setattr(supply_mod.requests, "get", fake_get)

    uf = UniverseFilter(min_adv_usd=0, min_mcap_usd=0)
    monkeypatch.setattr(uf.ex, "fetch_ticker", lambda s: {"last": 2})
    assert uf._mcap("BTC/USDT") == 2_000_000_000
