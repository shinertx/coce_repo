from src.risk_guardrails.liquidity_limits import adv_cap_check

def test_cap():
    assert adv_cap_check(1000, 100_000, 2)
    assert not adv_cap_check(5000, 100_000, 2)
