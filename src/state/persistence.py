from pathlib import Path
import joblib
from typing import Any, Dict

_STATE = Path("data/state.joblib")


def save_state(obj: Dict[str, Any]) -> None:
    """Persist internal state to disk."""

    _STATE.parent.mkdir(exist_ok=True)
    joblib.dump(obj, _STATE)


def load_state() -> Dict[str, Any] | None:
    """Return saved state if present."""

    return joblib.load(_STATE) if _STATE.exists() else None
