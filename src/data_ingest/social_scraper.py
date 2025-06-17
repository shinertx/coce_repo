import os
import tweepy
from textblob import TextBlob

TWITTER_BEARER = os.environ.get("TWITTER_BEARER", "")

class SocialScraper:
    def __init__(self) -> None:
        if not TWITTER_BEARER:
            raise RuntimeError("Missing TWITTER_BEARER in .env")
        self.client = tweepy.Client(bearer_token=TWITTER_BEARER, wait_on_rate_limit=True)

    def fetch_recent(self, symbol: str, n: int = 20) -> list[str]:
        """
        Fetches recent tweets mentioning the base asset (BTC, ETH, etc.)
        Returns a list of tweet texts (English, no retweets).
        """
        base = symbol.split("/")[0]
        try:
            query = f'"{base}" -is:retweet lang:en'
            tweets = self.client.search_recent_tweets(query=query, max_results=min(n, 100)).data or []
            return [t.text for t in tweets]
        except Exception as exc:
            print(f"[Sentiment] Failed to fetch tweets for {base}: {exc}")
            return []

    def polarity(self, posts: list[str]) -> float:
        """
        Returns the average sentiment polarity across all posts.
        """
        if not posts:
            return 0.0
        try:
            polarities = [float(TextBlob(p).sentiment.polarity) for p in posts]
            return sum(polarities) / len(polarities)
        except Exception as exc:
            print(f"[Sentiment] Error computing polarity: {exc}")
            return 0.0
