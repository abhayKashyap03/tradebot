import unittest
from unittest.mock import patch, MagicMock
from tradebot.risk_mgmt import RiskManager, TradeDecision
from tradebot.strategy import StockData
from tradebot.clients.robinhood_client import RobinhoodClient
from tradebot.configs.config import MAX_DAILY_TRADES


class TestRiskManager(unittest.TestCase):
    def setUp(self):
        self.mock_rh_client = MagicMock(spec=RobinhoodClient)
        self.manager = RiskManager(self.mock_rh_client)
        self.mock_stock_data = StockData(
            ticker="AAPL",
            price=150.0,
            volume=1000000,
            sma=145.0,
            rsi=60.0,
            macd=1.5,
            pe_ratio=25.0,
            peg_ratio=1.5,
            roe=0.15,
            revenue_growth=0.1,
            eps_growth=0.2,
            de_ratio=0.5,
            news_articles=[{"title": "Test News"}],
            tweets=[MagicMock(text="Test Tweet")],
        )
        self.mock_portfolio = {"cash": 10000}

    @patch("google.genai.client.Client")
    def test_assess_risk_approved(self, mock_genai_client):
        mock_response = MagicMock()
        mock_response.parsed = {"decision": "APPROVED", "reasoning": "Looks good"}
        mock_genai_client.models.generate_content.return_value = mock_response
        self.manager.llm_client = mock_genai_client

        decision, _ = self.manager.assess_risk(
            self.mock_stock_data, self.mock_portfolio
        )

        self.assertEqual(decision, TradeDecision.APPROVED)
        self.assertEqual(self.manager.daily_trades, 1)

    def test_assess_risk_max_trades_exceeded(self):
        self.manager.daily_trades = MAX_DAILY_TRADES
        decision, result = self.manager.assess_risk(
            self.mock_stock_data, self.mock_portfolio
        )
        self.assertEqual(decision, TradeDecision.VETOED)
        self.assertEqual(result["reasoning"], "Exceeded max daily number of trades.")


if __name__ == "__main__":
    unittest.main()
