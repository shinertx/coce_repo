from __future__ import annotations

import json
import logging
from pathlib import Path
import pandas as pd
from src.infra import send_alert

logger = logging.getLogger(__name__)
_LOG = Path("logs/meta_events.jsonl")

class MetaController:
    """Weekly performance auditor with kill-switch enforcement."""

    def __init__(
        self,
        trade_log: Path = Path("logs/trades.jsonl"),
        sharpe_floor: float = 1.0,
        hitrate_floor: float = 0.5,
    ) -> None:
        self.trade_log = trade_log
        self.sharpe_floor = sharpe_floor
        self.hitrate_floor = hitrate_floor

    def evaluate(self) -> None:
        if not self.trade_log.exists():
            return
        df = pd.read_json(self.trade_log, lines=True)
        df["ts"] = pd.to_datetime(df["ts"], utc=True)
        week = df[df["ts"] > (pd.Timestamp.utcnow() - pd.Timedelta(days=7))]
        if week.empty:
            return
        std = week["pnl"].std(ddof=0)
        if std == 0:
            sharpe = float("inf")
        else:
            sharpe = week["pnl"].mean() / std
        hit = (week["pnl"] > 0).mean()
        evt = {"ts": pd.Timestamp.utcnow().isoformat(), "sharpe": sharpe, "hit": hit}
        with _LOG.open("a") as f:
            f.write(json.dumps(evt) + "\n")
        logger.info("Meta eval %s", evt)
        if sharpe < self.sharpe_floor or hit < self.hitrate_floor:
            send_alert("Kill-switch triggered")
            raise RuntimeError("Kill-switch triggered")
