import numpy as np
import pandas as pd
from src.network_analysis.consensus import ConsensusClusters

def test_consensus():
    rng = np.random.default_rng(0)
    prices = pd.DataFrame(rng.random((60,5)), columns=list("ABCDE")).cumsum()
    cc = ConsensusClusters(window=10, threshold=0.5)
    for _ in range(cc.window):
        cc.update(prices.iloc[:30].corr())
    for i in range(30,60):
        cc.update(prices.iloc[i-30:i].corr())
    part = cc.update(prices.iloc[-30:].corr())
    assert len(part) == 5
