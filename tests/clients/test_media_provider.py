import unittest
from unittest.mock import patch, MagicMock
from tradebot.clients.media_provider import NewsDataProvider, TwitterDataProvider


class TestNewsDataProvider(unittest.TestCase):
    def setUp(self):
        self.provider = NewsDataProvider(api_key="test_key")

    @patch("newsapi.NewsApiClient.get_top_headlines")
    def test_get_top_headlines_success(self, mock_get_top_headlines):
        mock_get_top_headlines.return_value = {"articles": [{"title": "Test Article"}]}
        articles = self.provider.get_top_headlines("test-source")
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]["title"], "Test Article")

    @patch("newsapi.NewsApiClient.get_everything")
    def test_get_everything_success(self, mock_get_everything):
        mock_get_everything.return_value = {"articles": [{"title": "Test Article"}]}
        articles = self.provider.get_everything("test-query")
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]["title"], "Test Article")


class TestTwitterDataProvider(unittest.TestCase):
    def setUp(self):
        self.provider = TwitterDataProvider(
            api_key="test_key",
            api_secret="test_secret",
            access_token="test_token",
            access_token_secret="test_token_secret",
            bearer_token="test_bearer",
        )

    @patch("tweepy.Client.get_home_timeline")
    def test_get_user_timeline_success(self, mock_get_home_timeline):
        mock_tweet = MagicMock()
        mock_tweet.text = "Test Tweet"
        mock_get_home_timeline.return_value = ([mock_tweet], {"result_count": 1})
        tweets, meta = self.provider.get_user_timeline("test_user")
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0].text, "Test Tweet")
        self.assertEqual(meta["result_count"], 1)

    @patch("tweepy.Client.search_recent_tweets")
    def test_search_tweets_success(self, mock_search_recent_tweets):
        mock_tweet = MagicMock()
        mock_tweet.text = "Test Tweet"
        mock_search_recent_tweets.return_value = ([mock_tweet], {"result_count": 1})
        tweets, meta = self.provider.search_tweets("test-query")
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0].text, "Test Tweet")
        self.assertEqual(meta["result_count"], 1)


if __name__ == "__main__":
    unittest.main()
