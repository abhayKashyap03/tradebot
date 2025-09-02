import logging
import pandas as pd
import robin_stocks.robinhood as rh
from typing import Optional


logger = logging.getLogger(__name__)


class RobinhoodClient:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.authenticated = False

    def login(self):
        logger.info("Attempting to log into Robinhood...")
        logger.warning(
            "MANUAL ACTION REQUIRED: Please approve the login request on your Robinhood app."
        )
        try:
            rh.login(username=self.email, password=self.password)
            self.authenticated = True
            logger.info("Successfully logged in to Robinhood after verification")
        except Exception as e:
            logger.error(f"Failed to log in to Robinhood: {e}")
            raise

    def logout(self):
        if not self.authenticated:
            logger.warning("User is not logged in")
            return

        try:
            rh.logout()
            self.authenticated = False
            logger.info("Successfully logged out of Robinhood")
        except Exception as e:
            logger.error(f"Failed to log out of Robinhood: {e}")
            raise

    def get_latest_price(self, ticker: str) -> Optional[float]:
        if not self.authenticated:
            logger.warning("User is not logged in")
            return None

        try:
            price = rh.get_latest_price(ticker)

            if not price or price[0] is None:
                logger.warning(f"No price data found for ticker: {ticker.upper()}")
                return None

            price = float(price[0])
            logger.info(f"Got latest price for {ticker}: {price:.2f}")
            return price
        except Exception as e:
            logger.error(f"Failed to get latest price for {ticker}: {e}")
            return None

    def get_historical_data(
        self, ticker: str, interval: str = "hour", span: str = "month"
    ) -> Optional[pd.DataFrame]:
        if not self.authenticated:
            logger.warning("User is not logged in")
            return None

        try:
            raw_historicals = rh.get_stock_historicals(
                ticker.upper(), interval=interval, span=span
            )

            if not raw_historicals or raw_historicals[0] is None:
                logger.warning(f"No historical data found for {ticker.upper()}")
                return None

            # 2. Convert the list of dictionaries into a pandas DataFrame
            data = pd.DataFrame(raw_historicals)

            # 3. Clean and format the DataFrame
            data.set_index(pd.to_datetime(data["begins_at"]), inplace=True)
            data[["close_price", "open_price", "high_price", "low_price", "volume"]] = (
                data[
                    ["close_price", "open_price", "high_price", "low_price", "volume"]
                ].astype(float)
            )
            return data[
                ["open_price", "high_price", "low_price", "close_price", "volume"]
            ]

        except Exception as e:
            logger.error(f"Failed to get historical data for {ticker}: {e}")
            return None
