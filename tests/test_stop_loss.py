import pandas as pd
from src.execution.trade_manager import TradeManager


def _fake_secret(key: str) -> str:
    return "x"


def test_stop_loss(monkeypatch):
    risk = {
        "max_drawdown_pct": 18,
        "adv_cap_pct": 2,
        "var_confidence": 0.95,
        "corr_spike_thresh": 1.0,
        "stop_loss_pct": 10,
        "depth_impact_pct": 1,
    }
    monkeypatch.setattr("src.execution.ccxt_router.get_secret", _fake_secret)
    tm = TradeManager(1000, risk)
    monkeypatch.setattr("src.execution.trade_manager.load_state", lambda: None)
    monkeypatch.setattr("src.execution.trade_manager.save_state", lambda s: None)
    calls = []
    monkeypatch.setattr(tm.router, "place_order", lambda *a, **k: calls.append(a))
    monkeypatch.setattr(tm.router.client, "fetch_order_book", lambda symbol: {"asks": [[100, 1]], "bids": []})
    monkeypatch.setattr(tm.sentinel, "check", lambda btc, alt: True)
    monkeypatch.setattr("src.execution.trade_manager.hist_var_check", lambda *a, **k: True)

    price1 = pd.Series([100, 100, 100])
    btc = pd.Series([1, 1, 1])
    alt = pd.DataFrame({"ALT": [0.1, 0.1, 0.1]})
    tm.execute_signal("BTC", 0.9, price1, 1_000_000, btc, alt, 1)

    for price in [100, 90]:
        tm.monitor_position("BTC", price)

    assert any(call[1] == "sell" for call in calls)
