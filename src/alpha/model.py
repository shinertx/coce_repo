from __future__ import annotations
import logging
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)
_MODEL = Path("data/pump_model.joblib")


class PumpClassifier:
    """Logistic classifier for pump probability."""

    def __init__(self) -> None:
        """Initialize scaler and classifier."""

        self.scaler, self.clf = StandardScaler(), LogisticRegression(max_iter=200)

    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Train the classifier and persist to disk."""

        self.scaler.fit(X)
        self.clf.fit(self.scaler.transform(X), y)
        joblib.dump({"scaler": self.scaler, "clf": self.clf}, _MODEL)

    def load_or_train(self, csv: Path = Path("data/pump_events.csv")) -> None:
        """Load a saved model or train from ``csv`` if missing."""

        if _MODEL.exists():
            b = joblib.load(_MODEL)
            self.scaler, self.clf = b["scaler"], b["clf"]
            logger.info("Pump model loaded")
            return
        df = pd.read_csv(csv)
        if len(df) < 30:  # guard against nonsense sample
            logger.warning("Pump events <30 rows; classifier disabled")
            return
        self.fit(df.drop(columns=["is_pump"]), df["is_pump"].astype(int))
        logger.info("Pump model trained")

    def predict_proba(self, X: pd.DataFrame) -> pd.Series:
        """Probability of pump for each asset."""

        if not hasattr(self.clf, "coef_"):
            return pd.Series(0.0, index=X.index)
        return pd.Series(self.clf.predict_proba(self.scaler.transform(X))[:, 1], index=X.index)
