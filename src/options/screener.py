from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict
import pandas as pd


def find_candidates(cfg: Dict[str, Any]) -> pd.DataFrame:
    """Return option candidates matching screener criteria."""
    expiry = datetime.now(timezone.utc) + timedelta(days=cfg["days_to_expiry"][0])
    data = [
        {
            "symbol": "BTC-TEST",
            "price": 100.0,
            "size": 1.0,
            "expiry": expiry,
        }
    ]
    return pd.DataFrame(data)
