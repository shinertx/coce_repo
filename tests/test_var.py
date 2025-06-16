from src.risk_guardrails.max_drawdown import DrawdownTracker

def test_dd():
    tr = DrawdownTracker(10000)
    tr.update([0.01]*100)
    assert tr.within_limit(25)
