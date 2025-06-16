from __future__ import annotations

import logging
from typing import Any, Dict, Optional, cast

import yaml  # type: ignore

from ..options.deribit_router import DeribitRouter
from ..options.position_manager import PositionManager
from ..options.screener import find_candidates

logger = logging.getLogger(__name__)


def load_cfg(path: str) -> Dict[str, Any]:
    with open(path) as f:
        data = yaml.safe_load(f)
    return cast(Dict[str, Any], data)




def run_convex(
    nav: float,
    cfg_path: str,
    *,
    router: Optional[DeribitRouter] = None,
    pm: Optional[PositionManager] = None,
) -> PositionManager:
    """Execute convexity sleeve single-cycle."""

    cfg = load_cfg(cfg_path)
    budget = nav * cfg["budget_pct_nav"]
    logger.info("Convex sleeve budget %s", budget)

    router = router or DeribitRouter()
    pm = pm or PositionManager()

    for _, opt in find_candidates(cfg).iterrows():
        price = opt["price"]
        size = opt.get("size", 1.0)
        premium = price * size
        if pm.budget_spent + premium > budget:
            logger.info("Budget exhausted")
            continue
        try:
            router.place_order(opt["symbol"], "buy", size, price)
        except Exception as exc:  # pragma: no cover - network failure
            logger.error("Order failed for %s: %s", opt["symbol"], exc)
            continue
        pm.add_position(
            opt["symbol"],
            size,
            price,
            opt["expiry"],
            cfg["take_profit_pct"],
        )

    for pos in pm.check_exits(lambda s: router.fetch_price(s)):
        try:
            router.place_order(pos.symbol, "sell", pos.size, None)
        except Exception as exc:  # pragma: no cover - network failure
            logger.error("Sell failed for %s: %s", pos.symbol, exc)
            continue

    return pm
