from datetime import datetime, timedelta, timezone

from src.options.position_manager import PositionManager


def test_add_and_premium():
    pm = PositionManager()
    expiry = datetime.now(timezone.utc) + timedelta(days=1)
    pm.add_position("BTC", 2, 100.0, expiry, tp_pct=10)
    pm.add_position("ETH", 1, 50.0, expiry, tp_pct=20)
    assert len(pm.positions) == 2
    assert pm.open_premium() == 250.0
    assert pm.budget_spent == 250.0


def test_check_exits(monkeypatch):
    pm = PositionManager()
    past = datetime.now(timezone.utc) - timedelta(seconds=1)
    future = datetime.now(timezone.utc) + timedelta(days=1)
    pm.add_position("BTC", 1, 100.0, past, tp_pct=10)
    pm.add_position("ETH", 1, 100.0, future, tp_pct=10)

    def price_fn(symbol: str) -> float:
        return 200.0 if symbol == "ETH" else 0.0

    exited = pm.check_exits(price_fn)
    assert {p.symbol for p in exited} == {"BTC", "ETH"}
    assert pm.positions == []
    assert pm.budget_spent == 0.0
