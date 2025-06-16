import pandas as pd
from src.alpha.model import PumpClassifier

def test_model_predict(tmp_path):
    df = pd.DataFrame({"a": [0, 1, 0, 1], "b": [1, 0, 1, 0], "is_pump": [0, 1, 0, 1]})
    csv = tmp_path / "d.csv"
    df.to_csv(csv, index=False)
    pc = PumpClassifier()
    pc.load_or_train(csv)
    p = pc.predict_proba(df[["a","b"]])
    assert ((p>=0)&(p<=1)).all()
