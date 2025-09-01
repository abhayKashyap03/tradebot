import logging
import robin_stocks.robinhood as rh
from typing import List, Union


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
            raise Exception(e) from e
    
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
            raise Exception(e) from e

    def get_latest_price(self, ticker: Union[List[str], str]):
        if not self.authenticated:
            logger.warning("User is not logged in")
            return None

        try:
            price = rh.get_latest_price(ticker)
            logger.info(f"Got latest price for {', '.join(ticker)}...")
            return price
        except Exception as e:
            logger.error(f"Failed to get latest price for {ticker}: {e}")
            raise Exception(e) from e
