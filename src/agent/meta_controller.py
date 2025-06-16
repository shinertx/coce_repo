from __future__ import annotations
import json, logging
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)
_LOG = Path("logs/meta_events.jsonl")

class MetaController:
    """Weekly performance auditor (placeholder for kill-switch)."""
    def __init__(self, trade_log: Path = Path("logs/trades.jsonl")) -> None:
        self.trade_log = trade_log

    def evaluate(self) -> None:
        if not self.trade_log.exists():
            return
        df = pd.read_json(self.trade_log, lines=True)
        week = df[df["ts"] > (pd.Timestamp.utcnow() - pd.Timedelta(days=7))]
        if week.empty:
            return
        sharpe = week["pnl"].mean() / week["pnl"].std(ddof=0)
        hit = (week["pnl"] > 0).mean()
        evt = {"ts": pd.Timestamp.utcnow().isoformat(), "sharpe": sharpe, "hit": hit}
        with _LOG.open("a") as f:
            f.write(json.dumps(evt) + "\n")
        logger.info("Meta eval %s", evt)
