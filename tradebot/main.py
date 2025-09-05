import logging

from tradebot.configs.config import ROBINHOOD_EMAIL, ROBINHOOD_PWD, AV_API_KEY
from tradebot.configs.logger_config import setup_logger
from tradebot.clients.robinhood import RobinhoodClient
from tradebot.clients.fin_provider import FinDataProvider
from tradebot.analyzers.technical import (
    calculate_sma,
    calculate_rsi,
    calculate_macd,
    get_latest_indicator,
)
from tradebot.analyzers.fundamentals import (
    get_pe_ratio,
    get_peg_ratio,
    get_roe,
    get_revenue_growth,
    get_eps_growth,
    calculate_de_ratio,
)


logger = logging.getLogger(__name__)


def main():
    """Main entry point for the trading bot."""
    setup_logger()
    logger.info("Bot starting...")

    rh_client = None
    try:
        rh_client = RobinhoodClient(email=ROBINHOOD_EMAIL, password=ROBINHOOD_PWD)
        rh_client.login()

        fd_client = FinDataProvider(api_key=AV_API_KEY)

        test_ticker = ["AAPL", "TSLA", "GARBAGE"]
        for ticker in test_ticker:
            # latest price query
            price = fd_client.get_latest_price(ticker)
            if price is None:
                logger.warning(f"Could not get price for {ticker}. Skipping...")
                continue

            # historical data query
            hist_data = fd_client.get_historical_data(ticker)
            if hist_data is None:
                logger.warning(
                    f"Could not get historical data for {ticker}. Skipping..."
                )
                continue

            # technicals
            sma = get_latest_indicator(calculate_sma(hist_data, period=50))
            rsi = get_latest_indicator(calculate_rsi(hist_data, period=14))
            macd = get_latest_indicator(calculate_macd(hist_data))
            if sma is None or rsi is None or macd is None:
                logger.warning(
                    f"Could not calculate indicators for {ticker}. Skipping..."
                )
                continue
            else:
                logger.info(
                    f"Analysis for {ticker}: Price=${price:.2f}, SMA(50)=${sma:.2f}, RSI(14)={rsi:.2f}, MACD(12,26,9)=${macd.to_dict()}"
                )

            # fundamentals
            overview = fd_client.get_company_overview(ticker)
            balance_sheet = fd_client.get_balance_sheet(ticker)
            earnings = fd_client.get_earnings_history(ticker)
            if overview is None or balance_sheet is None or earnings is None:
                logger.warning(
                    f"Could not retrieve all fundamental data for {ticker}. Skipping..."
                )
                continue
            logger.info(f"Fundamental analysis for {ticker}:")
            logger.info(f"  P/E Ratio: {get_pe_ratio(overview)}")
            logger.info(f"  PEG Ratio: {get_peg_ratio(overview)}")
            logger.info(f"  ROE: {get_roe(overview)}")
            logger.info(f"  Revenue Growth: {get_revenue_growth(overview)}")
            logger.info(f"  EPS Growth: {get_eps_growth(earnings)}")
            logger.info(f"  Debt/Equity Ratio: {calculate_de_ratio(balance_sheet)}")

    except Exception as e:
        logger.error(
            f"An unexpected error occurred during bot execution: {e}", exc_info=True
        )
    finally:
        if rh_client and rh_client.authenticated:
            rh_client.logout()
        logger.info("Bot shutting down.")


if __name__ == "__main__":
    main()
