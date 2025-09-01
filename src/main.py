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
        test_ticker = ['AAPL', 'TSLA', 'GARBAGE']
        for ticker in test_ticker:
            price = client.get_latest_price(ticker)

            if price is not None:
                logger.info(f"Successfully processed {ticker} at price ${price:.2f}")
            else:
                logger.warning(f"Could not get price for {ticker}. Skipping...")

    except Exception as e:
        logger.error(f"An unexpected error occurred during bot execution: {e}", exc_info=True)
    finally:
        if client and client.authenticated:
            client.logout()
        logger.info("Bot shutting down.")

if __name__ == "__main__":
    main()
