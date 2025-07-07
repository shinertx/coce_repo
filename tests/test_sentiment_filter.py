from types import SimpleNamespace
from datetime import datetime, timedelta, timezone

import sys


class DummyTweepy:
    class Client:
        def __init__(self, *a, **k) -> None:
            pass


sys.modules.setdefault("tweepy", DummyTweepy)

from src.data_ingest import social_scraper  # noqa: E402
from src.data_ingest.social_scraper import SocialScraper  # noqa: E402


class DummyClient:
    def __init__(self) -> None:
        ts = datetime(1970, 1, 1, tzinfo=timezone.utc)
        self.data = [
            SimpleNamespace(text="hello world", author_id="u1", created_at=ts),
            SimpleNamespace(text="bonjour le monde", author_id="u1", created_at=ts + timedelta(minutes=1)),
            SimpleNamespace(text="spam spam", author_id="u1", created_at=ts + timedelta(minutes=2)),
            SimpleNamespace(text="another tweet", author_id="u2", created_at=ts + timedelta(minutes=1)),
        ]

    def search_recent_tweets(self, *a, **k):
        return SimpleNamespace(data=self.data)


def test_filter_and_polarity(monkeypatch):
    monkeypatch.setenv("TWITTER_BEARER", "x")
    monkeypatch.setattr(social_scraper, "TWITTER_BEARER", "x")
    sc = SocialScraper()
    monkeypatch.setattr(sc, "client", DummyClient())
    posts = sc.fetch_recent("BTC/USDT")
    assert len(posts) == 2  # dedup + language filter
    assert sc.polarity(posts) == 0.0  # fewer than 3 unique tweets

