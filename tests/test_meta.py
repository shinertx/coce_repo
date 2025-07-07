import json
import pytest
import pandas as pd
from src.agent.meta_controller import MetaController

def test_meta(tmp_path):
    log = tmp_path / "x.jsonl"
    mc = MetaController(log)
    mc.evaluate()  # no crash on missing file

    log.write_text(
        json.dumps({"ts": pd.Timestamp.utcnow().isoformat(), "pnl": -1}) + "\n"
    )
    mc = MetaController(log, sharpe_floor=1.0, hitrate_floor=1.0)
    with pytest.raises(RuntimeError):
        mc.evaluate()
