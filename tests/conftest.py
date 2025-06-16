import numpy as np, pandas as pd, pytest

@pytest.fixture
def price_series():
    return pd.Series(np.random.lognormal(size=120))
