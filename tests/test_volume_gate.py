import numpy as np
import pandas as pd
from src.data_ingest.volume_anomaly import volume_zscore

def test_volume_gate():
    vol = pd.Series(np.concatenate([np.ones(29), [10]]))
    z = volume_zscore(vol)
    assert z.iloc[-1] > 3
