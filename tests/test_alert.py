import json
from datetime import datetime, timedelta, timezone

import pandas as pd
import pytest
import yaml

from src.agent.meta_controller import MetaController
from src.agent.convex_controller import run_convex
from src.data_ingest.price_loader import PriceLoader


class FakeRouter:
    def __init__(self):
        self.orders = []

    def place_order(self, symbol, side, size, price=None):
        self.orders.append({"symbol": symbol, "side": side, "size": size, "price": price})

    def fetch_price(self, symbol):
        return 0.0


def fake_find_candidates(_cfg):
    exp = datetime.now(timezone.utc) + timedelta(days=1)
    return pd.DataFrame(
        [
            {"symbol": "BTC", "price": 30.0, "size": 1.0, "expiry": exp},
            {"symbol": "ETH", "price": 30.0, "size": 1.0, "expiry": exp},
        ]
    )


def test_kill_switch_alert(tmp_path, monkeypatch):
    log = tmp_path / "trades.jsonl"
    log.write_text(json.dumps({"ts": datetime.now(timezone.utc).isoformat(), "pnl": -1}) + "\n")
    mc = MetaController(log, sharpe_floor=1.0, hitrate_floor=1.0)
    called = []
    monkeypatch.setattr("src.agent.meta_controller.send_alert", lambda msg: called.append(msg))
    with pytest.raises(RuntimeError):
        mc.evaluate()
    assert called


def test_ccxt_error_alert(monkeypatch):
    pl = PriceLoader()
    monkeypatch.setattr(pl.ex, "fetch_ohlcv", lambda *a, **k: (_ for _ in ()).throw(Exception("fail")))
    called = []
    monkeypatch.setattr("src.data_ingest.price_loader.send_alert", lambda msg: called.append(msg))
    with pytest.raises(RuntimeError):
        pl.load("BTC/USDT", datetime(1970, 1, 1, tzinfo=timezone.utc), datetime(1970, 1, 2, tzinfo=timezone.utc))
    assert called


def test_convex_budget_alert(tmp_path, monkeypatch):
    cfg = {
        "budget_pct_nav": 0.5,
        "exchange": "deribit",
        "moneyness": 1.0,
        "days_to_expiry": [1],
        "iv_percentile_max": 100,
        "slippage_bps": 0,
        "take_profit_pct": 100,
        "cache_ttl_min": 1,
    }
    path = tmp_path / "sleeve.yaml"
    path.write_text(yaml.safe_dump(cfg))

    router = FakeRouter()
    called = []
    monkeypatch.setattr("src.agent.convex_controller.send_alert", lambda msg: called.append(msg))
    monkeypatch.setattr("src.agent.convex_controller.find_candidates", fake_find_candidates)
    run_convex(100.0, str(path), router=router)
    assert called
