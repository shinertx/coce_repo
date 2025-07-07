import pandas as pd
from src.alpha.model import PumpClassifier


def test_pump_classifier(tmp_path, monkeypatch):
    df = pd.DataFrame({"f": [0, 1, 2, 3], "is_pump": [0, 0, 1, 1]})
    csv = tmp_path / "events.csv"
    df.to_csv(csv, index=False)
    model_path = tmp_path / "model.joblib"
    monkeypatch.setattr("src.alpha.model._MODEL", model_path)
    pc = PumpClassifier()
    pc.load_or_train(csv)
    proba = pc.predict_proba(pd.DataFrame({"f": [1, 2]}))
    assert len(proba) == 2
