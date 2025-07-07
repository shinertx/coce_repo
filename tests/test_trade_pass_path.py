import pandas as pd
from src.execution.trade_manager import TradeManager, Trade


def test_execute_trade_pass_path(monkeypatch, price_series):
    """TradeManager returns Trade on risk pass and updates drawdown."""
    # disable persistence
    monkeypatch.setattr("src.execution.trade_manager.load_state", lambda: None)
    monkeypatch.setattr("src.execution.trade_manager.save_state", lambda state: None)

    risk_cfg = {"max_drawdown_pct": 18, "adv_cap_pct": 2, "var_confidence": 0.95, "corr_spike_thresh": 1.0}
    tm = TradeManager(10000, risk_cfg)

    monkeypatch.setattr(tm.router, "place_order", lambda symbol, side, size, price=None: None)
    monkeypatch.setattr(tm.sentinel, "check", lambda btc, alt: True)
    monkeypatch.setattr("src.execution.trade_manager.hist_var_check", lambda *a, **k: True)

    btc_series = pd.Series([1, 1.1, 1.2])
    alt_df = pd.DataFrame({"ALT": [0.1, 0.2, 0.3]}, index=btc_series.index)
    adv_usd = 100_000

    before = len(tm.drawdown.equity_curve)
    trade = tm.execute_signal("BTC/USDT", 0.8, price_series, adv_usd, btc_series, alt_df, 0.1)

    assert isinstance(trade, Trade)
    assert trade.risk == "PASS"
    assert len(tm.drawdown.equity_curve) == before + 1
