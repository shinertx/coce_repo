from src.utils.config_validation import validate_cfg


def test_validate_cfg_ok():
    cfg = {
        "risk": {"max_drawdown_pct": 18, "adv_cap_pct": 2},
        "sleeve": {"budget_pct_nav": 0.5, "enabled": False},
    }
    validate_cfg(cfg)


def test_validate_cfg_fail():
    cfg = {"risk": {"max_drawdown_pct": 20}}
    try:
        validate_cfg(cfg)
    except ValueError:
        return
    assert False, "expected ValueError"
