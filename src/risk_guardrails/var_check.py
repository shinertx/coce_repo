from __future__ import annotations
import numpy as np, pandas as pd, logging
logger = logging.getLogger(__name__)

def hist_var_check(returns: pd.Series, conf: float, var_floor: float = -0.03) -> bool:
    """Historical 1-day VaR at confidence `conf`."""
    if returns.empty:
        return True
    var = np.percentile(returns, (1 - conf) * 100)
    logger.debug("Hist VaR %.4f", var)
    return var > var_floor

# backward-compat for tests
def var_check(series, conf, var_floor=-0.03):  # noqa: N802
    return hist_var_check(series, conf, var_floor)
