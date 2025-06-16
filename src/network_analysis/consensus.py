from __future__ import annotations
import logging
from collections import Counter, deque
from typing import Deque, Dict
import networkx as nx, numpy as np, pandas as pd
from community import community_louvain
from scipy.sparse.csgraph import minimum_spanning_tree

logger = logging.getLogger(__name__)

class ConsensusClusters:
    """Sliding-window consensus Louvain clustering."""
    def __init__(self, window: int = 30, threshold: float = 0.6) -> None:
        self.partitions: Deque[Dict[str, int]] = deque(maxlen=window)
        self.window, self.threshold = window, threshold

    def _snapshot_partition(self, corr: pd.DataFrame) -> Dict[str, int]:
        dist = np.sqrt(2 * (1 - corr))
        mst = minimum_spanning_tree(dist.values)
        g = nx.Graph()
        syms = corr.columns.tolist()
        for i, j in zip(*mst.nonzero()):
            g.add_edge(syms[i], syms[j], weight=float(dist.iloc[i, j]))
        return community_louvain.best_partition(g)

    def update(self, corr: pd.DataFrame) -> Dict[str, int]:
        part = self._snapshot_partition(corr)
        self.partitions.append(part)
        if len(self.partitions) < self.partitions.maxlen:   # warm-up
            return part

        votes: Counter = Counter()
        for p in self.partitions:
            for i, ci in p.items():
                for j, cj in p.items():
                    if i < j and ci == cj:
                        votes[(i, j)] += 1

        stable = nx.Graph()
        for (i, j), v in votes.items():
            if v / self.window >= self.threshold:
                stable.add_edge(i, j)

        stable.add_nodes_from(corr.columns)
        return community_louvain.best_partition(stable) if stable.edges else part
