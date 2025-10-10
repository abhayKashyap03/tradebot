import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from tradebot.main import main
from tradebot.strategy import Signal
from tradebot.risk_mgmt import TradeDecision


class TestMain(unittest.TestCase):
    @patch("tradebot.main.ROBINHOOD_EMAIL", "test_email")
    @patch("tradebot.main.ROBINHOOD_PWD", "test_pwd")
    @patch("tradebot.main.AV_API_KEY", "test_key")
    @patch("tradebot.main.NEWS_API_KEY", "test_key")
    @patch("tradebot.main.TWITTER_API_KEY", "test_key")
    @patch("tradebot.main.TWITTER_API_SECRET", "test_secret")
    @patch("tradebot.main.TWITTER_ACCESS_TOKEN", "test_token")
    @patch("tradebot.main.TWITTER_ACCESS_TOKEN_SECRET", "test_token_secret")
    @patch("tradebot.main.TWITTER_BEARER_TOKEN", "test_bearer")
    @patch("tradebot.main.setup_logger")
    @patch("tradebot.main.RobinhoodClient")
    @patch("tradebot.main.FinDataProvider")
    @patch("tradebot.main.NewsDataProvider")
    @patch("tradebot.main.TwitterDataProvider")
    @patch("tradebot.main.StrategyEngine")
    @patch("tradebot.main.RiskManager")
    def test_main_e2e(
        self,
        mock_risk_manager,
        mock_strategy_engine,
        mock_twitter_provider,
        mock_news_provider,
        mock_fin_provider,
        mock_rh_client,
        mock_setup_logger,
    ):
        # Configure mocks
        mock_rh_client.return_value.get_portfolio_state.return_value = {"cash": 10000}
        mock_fin_provider.return_value.get_latest_price.return_value = 150.0
        # Create a DataFrame with enough data points for indicator calculation
        historical_data = pd.DataFrame(
            {
                "close": [i for i in range(100, 150)],
                "volume": [1000 + i for i in range(50)],
            }
        )
        mock_fin_provider.return_value.get_historical_data.return_value = (
            historical_data
        )
        overview_data = pd.DataFrame(
            {
                "PERatio": [25],
                "PEGRatio": [1.5],
                "ReturnOnEquityTTM": [0.15],
                "QuarterlyRevenueGrowthYOY": [0.1],
            }
        )
        mock_fin_provider.return_value.get_company_overview.return_value = overview_data
        mock_fin_provider.return_value.get_balance_sheet.return_value = pd.DataFrame(
            {"totalLiabilities": [100], "totalShareholderEquity": [200]}
        )
        mock_fin_provider.return_value.get_earnings_history.return_value = pd.DataFrame(
            {"reportedEPS": [1.0, 1.2]},
            index=pd.to_datetime(["2022-01-01", "2023-01-01"]),
        )
        mock_news_provider.return_value.get_everything.return_value = [
            {"title": "Test News"}
        ]
        mock_twitter_provider.return_value.search_tweets.return_value = (
            [MagicMock(text="Test Tweet")],
            {"result_count": 1},
        )
        mock_strategy_engine.return_value.decide_trade.return_value = (
            Signal.BUY,
            {"reasoning": "Looks good"},
        )
        mock_risk_manager.return_value.assess_risk.return_value = (
            TradeDecision.APPROVED,
            {"reasoning": "Looks good"},
        )

        # Run main
        main()

        # Assertions
        mock_rh_client.return_value.login.assert_called_once()
        mock_strategy_engine.return_value.decide_trade.assert_called()
        mock_risk_manager.return_value.assess_risk.assert_called()
        mock_rh_client.return_value.logout.assert_called_once()


if __name__ == "__main__":
    unittest.main()
