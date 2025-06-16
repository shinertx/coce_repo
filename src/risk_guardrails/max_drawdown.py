from __future__ import annotations
import pandas as pd
from dataclasses import dataclass
from typing import Sequence

@dataclass
class DrawdownTracker:
    starting_equity: float
    equity_curve: pd.Series = pd.Series(dtype=float)

    def update(self, returns: Sequence[float]) -> None:
        self.equity_curve = pd.concat(
            [self.equity_curve, pd.Series(returns)], ignore_index=True
        ).cumsum() + self.starting_equity

    def within_limit(self, max_dd_pct: float) -> bool:
        if self.equity_curve.empty:
            return True
        peak, trough = self.equity_curve.max(), self.equity_curve.min()
        return (peak - trough) / peak * 100 <= max_dd_pct
