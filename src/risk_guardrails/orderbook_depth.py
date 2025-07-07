from __future__ import annotations

import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)


def executable_size(order_book: dict[str, List[Tuple[float, float]]], side: str = "buy", impact_pct: float = 1.0) -> float:
    """Return cumulative volume executable within ``impact_pct`` price move."""
    levels: List[Tuple[float, float]] = order_book.get("asks" if side == "buy" else "bids", [])
    if not levels:
        return 0.0
    best_price = float(levels[0][0])
    if side == "buy":
        threshold = best_price * (1 + impact_pct / 100)
        qty = sum(float(q) for p, q in levels if p <= threshold)
    else:
        threshold = best_price * (1 - impact_pct / 100)
        qty = sum(float(q) for p, q in levels if p >= threshold)
    logger.debug("Depth size %.4f", qty)
    return qty

