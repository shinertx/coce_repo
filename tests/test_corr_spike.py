import pandas as pd
from src.risk_guardrails.corr_spike import CorrSpikeSentinel


def test_corr_spike_write_throttle(tmp_path, monkeypatch):
    path = tmp_path / 'corr.csv'
    monkeypatch.setattr('src.risk_guardrails.corr_spike._MEDIAN_CACHE', path)
    sent = CorrSpikeSentinel(1.0)
    btc = pd.Series([1, 2, 3])
    alt = pd.DataFrame({'ALT': [1, 2, 3]}, index=btc.index)
    assert not sent.check(btc, alt)
    first = path.read_text()
    sent.check(btc, alt)
    second = path.read_text()
    assert first == second

