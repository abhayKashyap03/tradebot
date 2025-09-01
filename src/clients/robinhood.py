import logging
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
        logger.warning("MANUAL ACTION REQUIRED: Please approve the login request on your Robinhood app.")
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
