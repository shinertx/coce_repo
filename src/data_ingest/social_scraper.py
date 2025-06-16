from __future__ import annotations
import logging
from typing import List
from textblob import TextBlob

logger = logging.getLogger(__name__)

class SocialScraper:
    """Placeholder sentiment - replace with real scrape."""
    def fetch_recent(self, symbol: str, n: int = 20) -> List[str]:
        return [f"{symbol} to the moon!"] * n  # TODO: real posts

    def polarity(self, posts: List[str]) -> float:
        return sum(TextBlob(p).sentiment.polarity for p in posts) / max(len(posts), 1)
