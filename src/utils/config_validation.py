from __future__ import annotations

from typing import Any, Dict


def validate_cfg(cfg: Dict[str, Any]) -> None:
    """Validate config invariants from AGENTS.md."""
    risk = cfg.get("risk", {})
    if risk.get("max_drawdown_pct", 100) > 18:
        raise ValueError("max_drawdown_pct > 18")
    if risk.get("adv_cap_pct", 100) > 2:
        raise ValueError("adv_cap_pct > 2")
    sleeve = cfg.get("sleeve", {})
    if sleeve.get("budget_pct_nav", 1.0) > 0.5:
        raise ValueError("sleeve.budget_pct_nav > 0.5")
