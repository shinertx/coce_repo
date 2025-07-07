from src.execution.ccxt_router import CcxtRouter


def _fake_secret(key: str) -> str:
    return "x"


def test_ccxt_router(monkeypatch):
    monkeypatch.setattr("src.execution.ccxt_router.get_secret", _fake_secret)
    router = CcxtRouter()
    called = {}
    monkeypatch.setattr(router.client, "create_limit_order", lambda s, side, size, price: called.setdefault("limit", price))
    monkeypatch.setattr(router.client, "create_market_order", lambda s, side, size: called.setdefault("market", size))
    monkeypatch.setattr(router.client, "fetch_ticker", lambda s: {"last": 1.5})

    router.place_order("BTC", "buy", 1, price=1.1)
    router.place_order("BTC", "buy", 1)
    price = router.fetch_price("BTC")
    assert called["limit"] == 1.1
    assert called["market"] == 1
    assert price == 1.5
