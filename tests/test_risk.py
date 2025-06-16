import numpy as np
import pandas as pd
from src.risk_guardrails.var_check import var_check

def test_var():
    r = pd.Series(np.random.normal(0, 0.01, 500))
    assert var_check(r, 0.95)
