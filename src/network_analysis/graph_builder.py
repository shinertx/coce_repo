from __future__ import annotations

import logging
import networkx as nx
import numpy as np
import pandas as pd
from scipy.sparse.csgraph import minimum_spanning_tree

logger = logging.getLogger(__name__)

def build_mst(corr: pd.DataFrame) -> nx.Graph:
    """Build a Minimum-Spanning-Tree from a correlation matrix."""
    distance = pd.DataFrame(
        np.sqrt(2 * (1 - corr)), index=corr.index, columns=corr.columns
    )
    mst = minimum_spanning_tree(distance.values)
    g: nx.Graph = nx.Graph()
    syms = corr.columns.tolist()
    for i, j in zip(*mst.nonzero()):
        g.add_edge(syms[i], syms[j], weight=float(distance.iat[i, j]))
    logger.debug("MST edges=%d", g.number_of_edges())
    return g
