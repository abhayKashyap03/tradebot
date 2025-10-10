import unittest
from unittest.mock import patch, MagicMock
from tradebot.strategy import StrategyEngine, StockData, Signal


class TestStrategyEngine(unittest.TestCase):
    def setUp(self):
        self.engine = StrategyEngine()
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

    @patch("google.genai.client.Client")
    def test_decide_trade_buy_signal(self, mock_genai_client):
        mock_response = MagicMock()
        mock_response.parsed = {
            "signal": "BUY",
            "reasoning": "Looks good",
            "confidence": "High",
        }
        mock_genai_client.models.generate_content.return_value = mock_response
        self.engine.llm_client = mock_genai_client

        signal, answer = self.engine.decide_trade(self.mock_stock_data)

        self.assertEqual(signal, Signal.BUY)
        self.assertEqual(answer["reasoning"], "Looks good")

    def test_decide_trade_unknown_strategy(self):
        with self.assertRaises(ValueError):
            self.engine.decide_trade(self.mock_stock_data, strategy="unknown")

    def test_format_prompt(self):
        template = "Basic Info: {basic_info}\nFundamentals: {fundamentals}"
        prompt = self.engine._format_prompt(template, self.mock_stock_data)
        self.assertIn("'Ticker': 'AAPL'", prompt)
        self.assertIn("'PE Ratio': 25.0", prompt)


if __name__ == "__main__":
    unittest.main()
