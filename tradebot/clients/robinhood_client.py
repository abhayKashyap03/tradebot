import logging
from ast import literal_eval

import robin_stocks.robinhood as rh


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
            logger.info("Successfully logged in to Robinhood after verification.")
        except Exception as e:
            logger.error(f"Failed to log in to Robinhood: {e}")
            raise

    def logout(self):
        if not self.authenticated:
            logger.error("User is not logged in.")
            raise Exception("User is not logged in.")

        try:
            rh.logout()
            self.authenticated = False
            logger.info("Successfully logged out of Robinhood.")
        except Exception as e:
            logger.error(f"Failed to log out of Robinhood: {e}")
            raise

    def get_portfolio_state(self):
        if not self.authenticated:
            logger.error("User is not logged in.")
            raise Exception("User is not logged in.")

        try:
            portfolio = {
                "equity": rh.build_holdings(),
                "cash": rh.build_user_profile(),
                "crypto": [],
            }

            crypto_positions = rh.get_crypto_positions()
            print(f"crypto positions: {crypto_positions}")
            for position in crypto_positions:
                print(position)
                if literal_eval(position["quantity"]) > 0:
                    portfolio["crypto"].append(position)

            logger.info(f"User Portfolio: {portfolio}")
            return portfolio

        except Exception as e:
            logger.error(f"Failed to get user portfolio: {e}")
            raise
