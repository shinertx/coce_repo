from __future__ import annotations
import logging
logger = logging.getLogger(__name__)

def adv_cap_check(order_usd: float, adv_usd: float, cap_pct: float) -> bool:
    """True if order ≤ cap_pct % of ADV."""
    result = order_usd <= adv_usd * cap_pct / 100
    logger.debug("ADV cap %s", result)
    return result
