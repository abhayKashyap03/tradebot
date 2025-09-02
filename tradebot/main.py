import logging

from tradebot.configs.config import ROBINHOOD_EMAIL, ROBINHOOD_PWD
from tradebot.configs.logger_config import setup_logger
from tradebot.clients.robinhood import RobinhoodClient
from tradebot.analyzers.technical import calculate_sma


logger = logging.getLogger(__name__)


def main():
    """Main entry point for the trading bot."""
    setup_logger()
    logger.info("Bot starting...")

    client = None
    try:
        client = RobinhoodClient(email=ROBINHOOD_EMAIL, password=ROBINHOOD_PWD)
        client.login()
        test_ticker = ["AAPL", "TSLA", "GARBAGE"]
        for ticker in test_ticker:
            price = client.get_latest_price(ticker)

            if price is None:
                logger.warning(f"Could not get price for {ticker}. Skipping...")
            else:
                hist_data = client.get_historical_data(ticker)

                if hist_data is None:
                    logger.warning(
                        f"Could not get historical data for {ticker}. Skipping SMA calculation..."
                    )
                else:
                    sma = calculate_sma(hist_data, period=50).iloc[-1]
                    if sma is None:
                        logger.warning(f"Could not calculate SMA for {ticker}.")
                    else:
                        logger.info(
                            f"Analysis for {ticker}: Price=${price:.2f}, SMA(50)=${sma:.2f}"
                        )

    except Exception as e:
        logger.error(
            f"An unexpected error occurred during bot execution: {e}", exc_info=True
        )
    finally:
        if client and client.authenticated:
            client.logout()
        logger.info("Bot shutting down.")


if __name__ == "__main__":
    main()
