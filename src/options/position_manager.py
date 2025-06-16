from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, List

@dataclass
class OptionPosition:
    symbol: str
    size: float
    entry_price: float
    expiry: datetime
    take_profit: float

class PositionManager:
    """Track open option positions and budget usage."""

    def __init__(self) -> None:
        self.positions: List[OptionPosition] = []
        self.budget_spent: float = 0.0

    def add_position(
        self,
        symbol: str,
        size: float,
        price: float,
        expiry: datetime,
        tp_pct: float,
    ) -> None:
        tp = price * (1 + tp_pct / 100)
        self.positions.append(
            OptionPosition(symbol=symbol, size=size, entry_price=price, expiry=expiry, take_profit=tp)
        )
        self.budget_spent += price * size

    def open_premium(self) -> float:
        return sum(p.entry_price * p.size for p in self.positions)

    def check_exits(self, price_fn: Callable[[str], float]) -> List[OptionPosition]:
        """Remove positions reaching take-profit or expiry."""
        exited: List[OptionPosition] = []
        now = datetime.now(timezone.utc)
        for pos in list(self.positions):
            if now >= pos.expiry or price_fn(pos.symbol) >= pos.take_profit:
                self.positions.remove(pos)
                self.budget_spent -= pos.entry_price * pos.size
                exited.append(pos)
        return exited
