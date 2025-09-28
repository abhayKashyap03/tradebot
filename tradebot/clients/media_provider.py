import logging
import tweepy
from newsapi import NewsApiClient
from datetime import date
from dateutil.relativedelta import relativedelta  # type: ignore
from typing import Optional, List


logger = logging.getLogger(__name__)


class NewsDataProvider:
    def __init__(self, api_key: str):
        self.news_client = NewsApiClient(api_key=api_key)

    def get_top_headlines(
        self, source: str, language: str = "en"
    ) -> Optional[List[dict]]:
        try:
            response = self.news_client.get_top_headlines(
                sources=source, language=language
            )
            articles = response.get("articles", [])
            logger.info(f"Fetched {len(articles)} articles for source: {source}")
            return articles
        except Exception as e:
            logger.error(f"Error fetching top headlines for {source}: {e}")
            return None

    def get_everything(
        self,
        query: str,
        from_param: Optional[str] = None,
        to: Optional[str] = None,
        language: str = "en",
    ) -> Optional[List[dict]]:
        try:
            if from_param and to:
                logger.info(
                    f"Fetching articles for {query} from {from_param} to {to}..."
                )
            else:
                logger.info(
                    f"Fetching recent articles for {query} from today to a month ago..."
                )
                from_param = (date.today() - relativedelta(months=1)).strftime(
                    "%Y-%m-%d"
                )
                to = date.today().strftime("%Y-%m-%d")
            response = self.news_client.get_everything(
                q=query, from_param=from_param, to=to, language=language
            )
            articles = response.get("articles", [])
            logger.info(
                f"Fetched {len(articles)} articles for query: {query} from {from_param} to {to}"
            )
            return articles
        except Exception as e:
            logger.error(f"Error fetching everything for {query}: {e}")
            return None


class TwitterDataProvider:
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        access_token: str,
        access_token_secret: str,
        bearer_token: str,
    ):
        self.twitter_client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

    def get_user_timeline(self, username: str, count: int = 10):
        try:
            response = self.twitter_client.get_home_timeline(max_results=count)
            tweets, meta = response[0], response[-1]
            logger.info(f"Fetched {meta['result_count']} tweets for user: {username}")
            return tweets, meta
        except Exception as e:
            logger.error(f"Error fetching tweets for {username}: {e}")
            return None

    def search_tweets(self, query: str, count: int = 10):
        try:
            response = self.twitter_client.search_recent_tweets(
                query=query, max_results=count
            )
            tweets, meta = response[0], response[-1]
            logger.info(f"Fetched {meta['result_count']} tweets for query: {query}")
            return tweets, meta
        except Exception as e:
            logger.error(f"Error searching tweets for {query}: {e}")
            return None


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    news_api_key = os.getenv("NEWS_API_KEY")
    twitter_api_key = os.getenv("TWITTER_API_KEY")
    twitter_api_secret = os.getenv("TWITTER_API_SECRET")
    twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    twitter_bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

    if news_api_key:
        news_provider = NewsDataProvider(news_api_key)
        articles = news_provider.get_everything("apple")
        print(f"Everything news: {articles}")

    if (
        twitter_api_key
        and twitter_api_secret
        and twitter_access_token
        and twitter_access_token_secret
        and twitter_bearer_token
    ):
        twitter_provider = TwitterDataProvider(
            twitter_api_key,
            twitter_api_secret,
            twitter_access_token,
            twitter_access_token_secret,
            twitter_bearer_token,
        )
        tweets, meta = twitter_provider.search_tweets("OpenAI", count=15)
        print(f"Recent tweets: {[tweet.text for tweet in tweets]}")
