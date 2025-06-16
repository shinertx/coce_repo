"""Standalone pump-classifier training."""
from pathlib import Path
import pandas as pd
from src.alpha.trainer import offline_train
from .label_pumps import label_pumps

CSV = Path("data/pump_events.csv")

if __name__ == "__main__":
    if not CSV.exists() or len(pd.read_csv(CSV)) < 30:
        label_pumps(CSV)
    offline_train(CSV)
