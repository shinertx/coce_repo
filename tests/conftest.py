import numpy as np
import pandas as pd
import pytest

@pytest.fixture
def price_series():
    return pd.Series(np.random.lognormal(size=120))
