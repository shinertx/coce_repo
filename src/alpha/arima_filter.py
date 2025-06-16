from __future__ import annotations
import logging
from typing import Sequence, Tuple
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

logger = logging.getLogger(__name__)

def arima_signal(prices: Sequence[float], order: Tuple[int, int, int], zcut: float) -> bool:
    """Return True if ARIMA forecast > current price by zcut·σ."""
    series = pd.Series(prices)
    if len(series) < 60:
        return False
    σ = series.pct_change().std(ddof=0)
    if σ == 0:
        return False
    try:
        fcast = ARIMA(series, order=order).fit().forecast()[0]
        z = (fcast - series.iloc[-1]) / (σ * series.iloc[-1])
        return z > zcut
    except Exception as exc:  # noqa: BLE001
        logger.warning("ARIMA fail: %s", exc)
        return False
