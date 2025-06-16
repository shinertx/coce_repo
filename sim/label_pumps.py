from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
import yaml
import pandas as pd

from src.data_ingest.price_loader import PriceLoader
from src.data_ingest.volume_anomaly import volume_zscore


def label_pumps(output: Path = Path("data/pump_events.csv")) -> Path:
    """Label pump events across configured universe and save to CSV."""
    with open("config/base.yaml") as f:
        cfg = yaml.safe_load(f)
    symbols = cfg.get("universe", {}).get("symbols", [])

    end = datetime.now(timezone.utc)
    start = end - timedelta(days=90)
    loader = PriceLoader()
    frames = []
    for sym in symbols:
        df = loader.load(sym, start, end)
        if df.empty:
            continue
        df["ret"] = df["c"].pct_change()
        df["vol_z"] = volume_zscore(df["v"])
        df["is_pump"] = ((df["ret"] > 0.9) & (df["vol_z"] > 4)).astype(int)
        frames.append(df[["ret", "vol_z", "is_pump"]])

    if not frames:
        return output

    all_rows = pd.concat(frames).dropna()
    if output.exists():
        prev = pd.read_csv(output)
        all_rows = pd.concat([prev, all_rows])
    all_rows = all_rows.drop_duplicates()
    all_rows.to_csv(output, index=False)
    return output


if __name__ == "__main__":  # pragma: no cover - manual invocation
    label_pumps()
