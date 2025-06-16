from __future__ import annotations
from pathlib import Path
import pandas as pd
from .model import PumpClassifier

def offline_train(csv_path: Path = Path("data/pump_events.csv")) -> None:
    df = pd.read_csv(csv_path)
    PumpClassifier().fit(df.drop(columns=["is_pump"]), df["is_pump"].astype(int))
