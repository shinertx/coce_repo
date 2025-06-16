from __future__ import annotations
import numpy as np, pandas as pd, logging
logger = logging.getLogger(__name__)

def hist_var_check(returns: pd.Series, conf: float) -> bool:
    """Historical 1-day VaR at confidence `conf`."""
    if returns.empty:
        return True
    var = np.percentile(returns, (1 - conf) * 100)
    logger.debug("Hist VaR %.4f", var)
    return var > -0.03

# backward-compat for tests
def var_check(series, conf):  # noqa: N802
    return hist_var_check(series, conf)
