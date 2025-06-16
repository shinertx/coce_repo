import numpy as np, pandas as pd
from src.portfolio.hrp_allocator import cluster_aware_hrp

def test_hrp():
    returns = pd.DataFrame(np.random.randn(100,4), columns=list("ABCD"))
    clusters = {"A":0,"B":0,"C":1,"D":1}
    w = cluster_aware_hrp(returns, clusters, 0.5)
    assert abs(sum(w.values())-1) < 1e-6
