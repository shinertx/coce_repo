import yaml
from datetime import datetime, timedelta, timezone
import pandas as pd

from src.agent.convex_controller import run_convex


class FakeRouter:
    def __init__(self):
        self.orders = []

    def place_order(self, symbol, side, size, price=None):
        self.orders.append({"symbol": symbol, "side": side, "size": size, "price": price})

    def fetch_price(self, symbol):
        return 0.0

def fake_find_candidates(cfg):
    expiry = datetime.now(timezone.utc) + timedelta(days=1)
    return pd.DataFrame([{"symbol": "BTC-TEST", "price": 100.0, "size": 2, "expiry": expiry}])


def test_run_convex_single_order(tmp_path, monkeypatch):
    cfg = {
        "budget_pct_nav": 1.0,
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
    monkeypatch.setattr("src.agent.convex_controller.find_candidates", fake_find_candidates)

    pm = run_convex(1000, str(path), router=router)

    assert pm.open_premium() == 200.0
    assert len(router.orders) == 1
