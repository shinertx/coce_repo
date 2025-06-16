from __future__ import annotations
from typing import Dict, List

def pick_representatives(clusters: Dict[str, int], adv: Dict[str, float]) -> List[str]:
    """One asset per cluster - highest ADV."""
    rep: Dict[int, str] = {}
    for s, cid in clusters.items():
        if cid not in rep or adv[s] > adv[rep[cid]]:
            rep[cid] = s
    return list(rep.values())
