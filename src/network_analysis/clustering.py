from __future__ import annotations

import logging
import networkx as nx
from community import community_louvain
from typing import Dict, cast

logger = logging.getLogger(__name__)

def louvain_clusters(mst_graph: nx.Graph) -> Dict[str, int]:
    """Louvain partition of MST graph."""
    part = community_louvain.best_partition(mst_graph)
    logger.debug("Louvain clusters=%d", len(set(part.values())))
    return cast(Dict[str, int], part)
