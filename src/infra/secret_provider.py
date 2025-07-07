from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()


def get_secret(key: str) -> str:
    """Return a secret from environment variables."""
    value = os.getenv(key)
    if not value:
        raise KeyError(f"Missing secret {key}")
    return value
