from __future__ import annotations
import logging, pandas as pd
from typing import Dict

logger = logging.getLogger(__name__)

def build_feature_frame(
    price_df: pd.DataFrame,
    clusters: Dict[str, int],
    volume_df: pd.DataFrame,
    sentiment: Dict[str, float],
) -> pd.DataFrame:
    """Assemble per-asset feature dataframe for pump classification."""
    pct = price_df.pct_change().iloc[-1].rename("ret_1d")
    vol_z = ((volume_df.iloc[-1] - volume_df.mean()) / volume_df.std(ddof=0)).rename("vol_z")
    cluster = pd.Series(clusters, name="cluster")
    sent = pd.Series(sentiment, name="sentiment")
    df = pd.concat([pct, vol_z, cluster, sent], axis=1)
    logger.debug("Feature frame shape=%s", df.shape)
    return df.dropna()
