from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

_LOG_DIR = Path("logs")
_LOG_DIR.mkdir(exist_ok=True)


def _iso_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat(timespec="seconds")


class JsonlFormatter(logging.Formatter):
    """Format log records as JSON lines."""

    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "ts": _iso_now(),
            "level": record.levelname,
            "module": record.name,
            "msg": record.getMessage(),
        }
        if record.args:
            payload["args"] = record.args
        return json.dumps(payload, separators=(",", ":"))


def setup_logging() -> None:
    """Configure root logger with JSONL formatter."""

    handler = logging.StreamHandler()
    handler.setFormatter(JsonlFormatter())
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), handlers=[handler], force=True)
