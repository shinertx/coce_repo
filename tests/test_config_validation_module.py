import pytest
from src.utils.config_validation import validate_cfg


def test_validate_cfg_ok():
    validate_cfg({"risk": {"max_drawdown_pct": 10, "adv_cap_pct": 1}, "sleeve": {"budget_pct_nav": 0.4, "enabled": False}})


def test_validate_cfg_fail():
    with pytest.raises(ValueError):
        validate_cfg({"risk": {"max_drawdown_pct": 20}})
