from __future__ import annotations
import pandas as pd
from dataclasses import dataclass, field
from typing import Sequence


@dataclass
class DrawdownTracker:
    """Track cumulative returns and enforce drawdown limits."""

    starting_equity: float
    equity_curve: pd.Series = field(default_factory=lambda: pd.Series(dtype=float))

    def update(self, returns: Sequence[float]) -> None:
        """Append returns and update the equity curve."""

        self.equity_curve = (
            pd.concat([self.equity_curve, pd.Series(returns)], ignore_index=True).cumsum()
            + self.starting_equity
        )

    def within_limit(self, max_dd_pct: float) -> bool:
        """Check if drawdown remains below ``max_dd_pct``."""

        if self.equity_curve.empty:
            return True
        peak, trough = self.equity_curve.max(), self.equity_curve.min()
        return (peak - trough) / peak * 100 <= max_dd_pct
