import logging
import pandas as pd
from typing import Optional, Literal
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.timeseries import TimeSeries


logger = logging.getLogger(__name__)


class FinDataProvider:
    def __init__(self, api_key):
        self.av_fund = FundamentalData(key=api_key, output_format="pandas")
        self.av_ts = TimeSeries(key=api_key, output_format="pandas")

    def get_latest_price(self, ticker: str) -> Optional[float]:
        try:
            quote = self.av_ts.get_quote_endpoint(ticker.upper())[0]

            if quote.empty or quote is None:
                logger.warning(f"No price data found for ticker: {ticker.upper()}")
                return None

            price = float(quote["05. price"].iloc[0])
            logger.info(f"Got latest price for {ticker}: {price:.2f}")
            return price

        except Exception as e:
            logger.error(f"Failed to get latest price for {ticker}: {e}")
            return None

    def get_historical_data(
        self, ticker: str, span: Literal["month", "year", "5year", "full"] = "full"
    ) -> Optional[pd.DataFrame]:
        try:
            raw_historical = self.av_ts.get_daily(ticker, "full")[0]

            if raw_historical is None or raw_historical.empty:
                logger.warning(f"No historical data found for {ticker.upper()}")
                return None

            raw_historical.sort_index(inplace=True)

            # rename columns: "1. open" ... "5. volume" -> "open" ... "volume"
            raw_historical.columns = [col.split()[-1] for col in raw_historical.columns]

            if span == "full":
                return raw_historical

            start_date = raw_historical.index.max()
            if span == "month":
                end_date = start_date - pd.DateOffset(months=1)
            elif span == "year":
                end_date = start_date - pd.DateOffset(years=1)
            elif span == "5year":
                end_date = start_date - pd.DateOffset(years=5)
            return raw_historical[raw_historical.index >= end_date]

        except Exception as e:
            logger.error(f"Failed to get historical data for {ticker}: {e}")
            return None

    def get_company_overview(self, ticker: str) -> Optional[pd.DataFrame]:
        try:
            response = self.av_fund.get_company_overview(ticker)[0]

            if response is None or response.empty:
                logger.warning(f"No overview data found for ticker: {ticker.upper()}")
                return None

            return response

        except Exception as e:
            logger.error(f"Error fetching company overview for {ticker}: {e}")
            return None

    def get_balance_sheet(self, ticker: str) -> Optional[pd.DataFrame]:
        try:
            balance_sheet = self.av_fund.get_balance_sheet_quarterly(ticker)[0]

            if balance_sheet is None or balance_sheet.empty:
                logger.warning(
                    f"No balance sheet data found for ticker: {ticker.upper()}"
                )
                return None

            balance_sheet = balance_sheet.set_index("fiscalDateEnding")
            balance_sheet.index = pd.to_datetime(balance_sheet.index)
            return balance_sheet

        except Exception as e:
            logger.error(f"Error fetching balance sheet for {ticker}: {e}")
            return None

    def get_earnings_history(self, ticker: str) -> Optional[pd.DataFrame]:
        try:
            earnings = self.av_fund.get_earnings_quarterly(ticker)[0]

            if earnings is None or earnings.empty:
                logger.warning(
                    f"No earnings history data found for ticker: {ticker.upper()}"
                )
                return None

            earnings = earnings.set_index("fiscalDateEnding")
            earnings.index = pd.to_datetime(earnings.index)
            return earnings

        except Exception as e:
            logger.error(f"Error fetching earnings history for {ticker}: {e}")
            return None
