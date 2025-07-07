from src.risk_guardrails.orderbook_depth import executable_size
from src.execution.trade_manager import TradeManager
import pandas as pd


def _fake_secret(key: str) -> str:
    return "x"


def test_executable_size():
    order_book = {"asks": [[10, 2], [10.1, 3], [10.5, 5]], "bids": [[9.9, 2]]}
    size = executable_size(order_book, "buy", 1)
    assert size == 5  # 2 + 3 within 1%


def test_depth_limit_trade(monkeypatch, price_series):
    risk = {
        "max_drawdown_pct": 18,
        "adv_cap_pct": 2,
        "var_confidence": 0.95,
        "corr_spike_thresh": 1.0,
        "depth_impact_pct": 1,
    }
    monkeypatch.setattr("src.execution.ccxt_router.get_secret", _fake_secret)
    tm = TradeManager(1000, risk)
    monkeypatch.setattr("src.execution.trade_manager.load_state", lambda: None)
    monkeypatch.setattr("src.execution.trade_manager.save_state", lambda s: None)
    monkeypatch.setattr(tm.router, "place_order", lambda *a, **k: None)
    monkeypatch.setattr(tm.sentinel, "check", lambda btc, alt: True)
    monkeypatch.setattr("src.execution.trade_manager.hist_var_check", lambda *a, **k: True)
    monkeypatch.setattr(tm.router.client, "fetch_order_book", lambda symbol: {"asks": [[10, 1]], "bids": []})

    btc = pd.Series([1, 1, 1])
    alt = pd.DataFrame({"ALT": [0.1, 0.1, 0.1]})
    trade = tm.execute_signal("BTC", 0.9, pd.Series([10, 10, 10]), 1_000_000, btc, alt, 1)
    assert trade.size == 1  # depth limited

