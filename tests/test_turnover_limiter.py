from src.risk_guardrails.turnover import TurnoverLimiter


def test_turnover_limiter():
    tl = TurnoverLimiter(10)
    w1 = {"A": 0.5, "B": 0.5}
    w2 = {"A": 0.7, "B": 0.3}
    assert tl.limit(w1) == w1
    res = tl.limit(w2)
    assert abs(sum(res.values()) - 1) < 1e-6
