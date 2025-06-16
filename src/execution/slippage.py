from __future__ import annotations

import logging
import math

logger = logging.getLogger(__name__)

def sqrt_slippage(order_usd: float, adv_usd: float, alpha_bps: float = 20.0) -> float:
    """Square-root impact model; returns fraction (e.g., 0.001 for 10 bps)."""
    if adv_usd <= 0:
        return 0.0
    bps = alpha_bps * math.sqrt(order_usd / adv_usd)
    logger.debug("slippage %.2fbps", bps)
    return bps / 10_000
