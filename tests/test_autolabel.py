from datetime import timedelta
import pandas as pd
from sim.label_pumps import label_pumps
from src.data_ingest.price_loader import PriceLoader


def test_label_pumps(monkeypatch, tmp_path):
    def fake_load(self, symbol, start, end, timeframe="1d", limit=1000):
        dates = pd.date_range(end - timedelta(days=89), end, freq="D")
        df = pd.DataFrame({
            "o": 1.0,
            "h": 1.0,
            "l": 1.0,
            "c": 1.0,
            "v": 1.0,
        }, index=dates)
        spike_idx = dates[-2]
        df.loc[spike_idx, ["o", "h", "l", "c"]] = 2.0
        df.loc[spike_idx, "v"] = 100.0
        return df

    monkeypatch.setattr(PriceLoader, "load", fake_load)
    out = tmp_path / "pump_events.csv"
    label_pumps(out)
    df = pd.read_csv(out)
    assert (df["is_pump"] == 1).any()
