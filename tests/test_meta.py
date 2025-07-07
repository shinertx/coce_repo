import json
from pathlib import Path

import pandas as pd
import pytest

from src.agent.meta_controller import MetaController


def _write_log(path: Path, pnls: list[float]) -> None:
    entries = [json.dumps({"ts": pd.Timestamp.utcnow().isoformat(), "pnl": p}) for p in pnls]
    path.write_text("\n".join(entries) + "\n")


def test_meta_two_stage(tmp_path: Path) -> None:
    log = tmp_path / "good.jsonl"
    _write_log(log, [-1, 1])

    mc = MetaController(log, sharpe_floor=1.0, hitrate_floor=0.1)
    mc.evaluate()  # only Sharpe below floor

    mc = MetaController(log, sharpe_floor=-0.1, hitrate_floor=0.9)
    mc.evaluate()  # only hit rate below floor

    bad = tmp_path / "bad.jsonl"
    _write_log(bad, [-1, -2])
    mc = MetaController(bad, sharpe_floor=1.0, hitrate_floor=0.5)
    with pytest.raises(RuntimeError):
        mc.evaluate()


def test_meta_manual_override(tmp_path: Path) -> None:
    log = tmp_path / "bad.jsonl"
    _write_log(log, [-1, -1])
    override = tmp_path / "override.yaml"
    override.write_text("disable_kill_switch: true")

    mc = MetaController(log, sharpe_floor=1.0, hitrate_floor=0.5, override_file=override)
    mc.evaluate()  # no exception due to override
