from __future__ import annotations
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class TurnoverLimiter:
    """Throttle portfolio turnover to cap_pct_nav per rebalance."""
    def __init__(self, cap_pct_nav: float) -> None:
        self.cap = cap_pct_nav / 100
        self.prev: Dict[str, float] = {}

    def limit(self, new: Dict[str, float]) -> Dict[str, float]:
        if not self.prev:
            self.prev = new
            return new
        turn = sum(abs(new.get(k, 0) - self.prev.get(k, 0)) for k in set(new) | set(self.prev))
        if turn <= self.cap:
            self.prev = new
            return new
        scale = self.cap / turn
        throttled = {
            k: self.prev.get(k, 0) + (new.get(k, 0) - self.prev.get(k, 0)) * scale
            for k in set(new) | set(self.prev)
        }
        logger.info("Turnover throttled from %.2f to %.2f", turn, self.cap)
        self.prev = throttled
        return throttled
