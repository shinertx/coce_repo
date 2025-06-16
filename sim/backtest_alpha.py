"""Standalone pump-classifier training."""
from pathlib import Path
from src.alpha.trainer import offline_train

if __name__ == "__main__":
    offline_train(Path("data/pump_events.csv"))
