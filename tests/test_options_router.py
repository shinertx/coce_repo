import requests_mock
from requests import Response
from src.options.deribit_router import DeribitRouter


def test_deribit_router(monkeypatch):
    monkeypatch.setenv("DERIBIT_CLIENT_ID", "id")
    monkeypatch.setenv("DERIBIT_CLIENT_SECRET", "secret")
    with requests_mock.Mocker() as m:
        m.post(
            "https://www.deribit.com/api/v2/public/auth",
            json={"result": {"access_token": "tok"}},
        )
        m.get(
            "https://www.deribit.com/api/v2/public/get_last_trades_by_instrument",
            json={"result": {"trades": [{"price": 1.1}]}},
        )
        m.post(
            "https://www.deribit.com/api/v2/private/buy",
            json={"result": "ok"},
        )
        router = DeribitRouter()
        assert router.token == "tok"

        called = {}
        real_get = router.session.get

        def wrapped(url: str, **kw) -> Response:
            called["timeout"] = kw.get("timeout")
            return real_get(url, **kw)

        router.session.get = wrapped

        assert router.fetch_price("BTC") == 1.1
        assert called["timeout"] == 10
        res = router.place_order("BTC", "buy", 1, 1.1)
        assert res["result"] == "ok"
