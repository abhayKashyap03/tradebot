import unittest
import pandas as pd
from unittest.mock import patch
from tradebot.clients.fin_provider import FinDataProvider


class TestFinDataProvider(unittest.TestCase):
    def setUp(self):
        self.provider = FinDataProvider(api_key="test_key")

    @patch("alpha_vantage.timeseries.TimeSeries.get_quote_endpoint")
    def test_get_latest_price_success(self, mock_get_quote):
        mock_get_quote.return_value = (pd.DataFrame([{"05. price": "150.0"}]), None)
        price = self.provider.get_latest_price("AAPL")
        self.assertEqual(price, 150.0)

    @patch(
        "alpha_vantage.timeseries.TimeSeries.get_quote_endpoint",
        return_value=(None, None),
    )
    def test_get_latest_price_no_data(self, mock_get_quote):
        price = self.provider.get_latest_price("AAPL")
        self.assertIsNone(price)

    @patch(
        "alpha_vantage.timeseries.TimeSeries.get_quote_endpoint",
        side_effect=Exception("API error"),
    )
    def test_get_latest_price_exception(self, mock_get_quote):
        price = self.provider.get_latest_price("AAPL")
        self.assertIsNone(price)

    @patch("alpha_vantage.timeseries.TimeSeries.get_daily")
    def test_get_historical_data_success(self, mock_get_daily):
        data = {
            "1. open": [100, 101],
            "2. high": [102, 103],
            "3. low": [99, 100],
            "4. close": [101, 102],
            "5. volume": [1000, 1100],
        }
        mock_get_daily.return_value = (
            pd.DataFrame(data, index=pd.to_datetime(["2023-01-01", "2023-01-02"])),
            None,
        )
        historical_data = self.provider.get_historical_data("AAPL")
        self.assertIsNotNone(historical_data)
        self.assertEqual(len(historical_data), 2)

    @patch("alpha_vantage.fundamentaldata.FundamentalData.get_company_overview")
    def test_get_company_overview_success(self, mock_get_overview):
        mock_get_overview.return_value = (pd.DataFrame([{"Symbol": "AAPL"}]), None)
        overview = self.provider.get_company_overview("AAPL")
        self.assertIsNotNone(overview)
        self.assertEqual(overview["Symbol"].iloc[0], "AAPL")

    @patch("alpha_vantage.fundamentaldata.FundamentalData.get_balance_sheet_quarterly")
    def test_get_balance_sheet_success(self, mock_get_balance_sheet):
        data = {"fiscalDateEnding": ["2023-03-31"], "totalAssets": [1000]}
        mock_get_balance_sheet.return_value = (pd.DataFrame(data), None)
        balance_sheet = self.provider.get_balance_sheet("AAPL")
        self.assertIsNotNone(balance_sheet)
        self.assertEqual(balance_sheet["totalAssets"].iloc[0], 1000)

    @patch("alpha_vantage.fundamentaldata.FundamentalData.get_earnings_quarterly")
    def test_get_earnings_history_success(self, mock_get_earnings):
        data = {"fiscalDateEnding": ["2023-03-31"], "reportedEPS": [1.52]}
        mock_get_earnings.return_value = (pd.DataFrame(data), None)
        earnings = self.provider.get_earnings_history("AAPL")
        self.assertIsNotNone(earnings)
        self.assertEqual(earnings["reportedEPS"].iloc[0], 1.52)


if __name__ == "__main__":
    unittest.main()
