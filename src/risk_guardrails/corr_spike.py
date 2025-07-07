from __future__ import annotations

import logging
import pandas as pd
from pathlib import Path

_MEDIAN_CACHE = Path("data/btc_alt_corr.csv")
logger = logging.getLogger(__name__)


def median_btc_alt_corr(btc: pd.Series, alt: pd.DataFrame) -> float:
    """Median correlation between BTC and each alt series."""

    joined = alt.loc[btc.index]
    return joined.apply(lambda s: s.corr(btc)).median()


class CorrSpikeSentinel:
    """Block trading when BTC-alt median corr ≥ threshold."""

    def __init__(self, threshold: float) -> None:
        """Create sentinel with correlation ``threshold``."""

        self.threshold = threshold
        self._last_write: float = 0.0

    def check(self, btc: pd.Series, alt_df: pd.DataFrame) -> bool:
        """Return ``True`` if trading is allowed."""

        med = median_btc_alt_corr(btc, alt_df) if not btc.empty else 0.0
        now = pd.Timestamp.utcnow().timestamp()
        if now - self._last_write > 60:
            _MEDIAN_CACHE.write_text(f"{med}\n")
            self._last_write = now
        return med < self.threshold
