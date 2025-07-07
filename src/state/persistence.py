from pathlib import Path
import json
from typing import Any, Dict, cast

_STATE = Path("data/state.json")


def save_state(obj: Dict[str, Any]) -> None:
    """Persist internal state safely as JSON."""

    _STATE.parent.mkdir(exist_ok=True)
    tmp = _STATE.with_suffix(".tmp")
    with tmp.open("w") as f:
        json.dump(obj, f)
    tmp.replace(_STATE)


def load_state() -> Dict[str, Any] | None:
    """Return saved state if present and valid."""

    if not _STATE.exists():
        return None
    try:
        with _STATE.open() as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("State must be a JSON object")
        return cast(Dict[str, Any], data)
    except (json.JSONDecodeError, ValueError):
        return None
