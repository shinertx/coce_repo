from __future__ import annotations

import logging
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import squareform
from typing import Dict

logger = logging.getLogger(__name__)

def _leaf_weights(cov: pd.DataFrame) -> Dict[str, float]:
    corr = cov.corr()
    dist = ((1 - corr) / 2) ** 0.5
    link = linkage(squareform(dist), "single")
    order = dendrogram(link, labels=dist.index, no_plot=True)["ivl"]
    ivp = 1 / np.diag(cov.loc[order, order])
    return dict(zip(order, ivp / ivp.sum()))

def cluster_aware_hrp(
    returns: pd.DataFrame, clusters: Dict[str, int], cluster_cap: float
) -> Dict[str, float]:
    """HRP allocation with per-cluster cap."""
    weights: Dict[str, float] = {}
    k = len(set(clusters.values()))
    per_cluster = min(1 / k, cluster_cap)
    for cid in set(clusters.values()):
        members = [m for m, c in clusters.items() if c == cid]
        if len(members) == 1:
            weights[members[0]] = per_cluster
        else:
            sub = _leaf_weights(returns[members].cov())
            for s, w in sub.items():
                weights[s] = w * per_cluster
    factor = 1 / sum(weights.values())
    return {k: v * factor for k, v in weights.items()}
