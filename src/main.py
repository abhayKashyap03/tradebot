import logging
from src.configs.config import ROBINHOOD_EMAIL, ROBINHOOD_PWD
from src.configs.logger_config import setup_logger
from src.clients.robinhood import RobinhoodClient

logger = logging.getLogger(__name__)

def main():
    """Main entry point for the trading bot."""
    setup_logger()
    logger.info("Bot starting...")

    client = None
    try:
        client = RobinhoodClient(email=ROBINHOOD_EMAIL, password=ROBINHOOD_PWD)
        client.login()
        # We will add more logic here in the future
        test_tickers = ['AAPL', 'TSLA', 'NVDA']
        logger.info(f"Getting latest price for {', '.join(test_tickers)}...")
        prices = client.get_latest_price(test_tickers)
        for ticker, price in zip(test_tickers, prices):
            logger.info(f"Latest price for {ticker}: {price}")

    except Exception as e:
        logger.error(f"An error occurred during bot execution: {e}")
    finally:
        if client and client.authenticated:
            client.logout()
        logger.info("Bot shutting down.")

if __name__ == "__main__":
    main()
