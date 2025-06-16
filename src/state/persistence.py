from pathlib import Path
import joblib
from typing import Any, Dict

_STATE = Path("data/state.joblib")

def save_state(obj: Dict[str, Any]) -> None:
    _STATE.parent.mkdir(exist_ok=True)
    joblib.dump(obj, _STATE)

def load_state() -> Dict[str, Any] | None:
    return joblib.load(_STATE) if _STATE.exists() else None
