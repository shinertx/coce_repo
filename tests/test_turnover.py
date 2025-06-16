from src.risk_guardrails.turnover import TurnoverLimiter


def test_turn():
    tl = TurnoverLimiter(10)
    w0 = {"A": 0.5, "B": 0.5}
    tl.limit(w0)
    w1 = {"A": 1.0, "B": 0.0}
    out = tl.limit(w1)
    assert sum(abs(out[k] - w0.get(k, 0)) for k in out) <= 0.10 + 1e-6
