from __future__ import annotations
import logging, networkx as nx, numpy as np, pandas as pd
from scipy.sparse.csgraph import minimum_spanning_tree

logger = logging.getLogger(__name__)

def build_mst(corr: pd.DataFrame) -> nx.Graph:
    """Build a Minimum-Spanning-Tree from a correlation matrix."""
    distance = np.sqrt(2 * (1 - corr))
    mst = minimum_spanning_tree(distance.values)
    g = nx.Graph()
    syms = corr.columns.tolist()
    for i, j in zip(*mst.nonzero()):
        g.add_edge(syms[i], syms[j], weight=float(distance.iat[i, j]))
    logger.debug("MST edges=%d", g.number_of_edges())
    return g
