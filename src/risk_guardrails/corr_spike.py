from __future__ import annotations

import logging
import pandas as pd
from pathlib import Path

_MEDIAN_CACHE = Path("data/btc_alt_corr.csv")
logger = logging.getLogger(__name__)

def median_btc_alt_corr(btc: pd.Series, alt: pd.DataFrame) -> float:
    joined = alt.loc[btc.index]
    return joined.apply(lambda s: s.corr(btc)).median()

class CorrSpikeSentinel:
    """Block trading when BTC-alt median corr ≥ threshold."""
    def __init__(self, threshold: float) -> None:
        self.threshold = threshold

    def check(self, btc: pd.Series, alt_df: pd.DataFrame) -> bool:
        med = median_btc_alt_corr(btc, alt_df) if not btc.empty else 0.0
        _MEDIAN_CACHE.write_text(f"{med}\n")
        return med < self.threshold
