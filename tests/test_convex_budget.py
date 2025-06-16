from datetime import datetime, timedelta, timezone
import yaml

from src.agent.convex_controller import run_convex
import pandas as pd

class FakeRouter:
    def __init__(self):
        self.orders = []

    def place_order(self, symbol, side, size, price=None):
        self.orders.append({"symbol": symbol, "side": side, "size": size, "price": price})

    def fetch_price(self, symbol):
        return 0.0

def fake_find_candidates(cfg):
    expiry = datetime.now(timezone.utc) + timedelta(days=1)
    return pd.DataFrame(
        [
            {"symbol": "BTC", "price": 100.0, "size": 3, "expiry": expiry},
            {"symbol": "ETH", "price": 100.0, "size": 3, "expiry": expiry},
        ]
    )


def test_budget(tmp_path, monkeypatch):
    cfg = {
        "budget_pct_nav": 0.5,
        "exchange": "binance",
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
    monkeypatch.setattr(
        "src.agent.convex_controller.find_candidates",
        fake_find_candidates,
    )

    run_convex(1000, str(path), router=router)
    spent = sum(o["price"] * o["size"] for o in router.orders)
    assert spent <= 500
