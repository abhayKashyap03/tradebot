import logging

from tradebot.configs.config import (
    ROBINHOOD_EMAIL,
    ROBINHOOD_PWD,
    AV_API_KEY,
    NEWS_API_KEY,
    TWITTER_API_KEY,
    TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    TWITTER_BEARER_TOKEN,
)
from tradebot.configs.logger_config import setup_logger
from tradebot.clients.robinhood import RobinhoodClient
from tradebot.clients.fin_provider import FinDataProvider
from tradebot.clients.media_provider import NewsDataProvider, TwitterDataProvider
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
from tradebot.strategy import StrategyEngine, StockData


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

            news_provider = NewsDataProvider(api_key=NEWS_API_KEY)
            twitter_provider = TwitterDataProvider(
                api_key=TWITTER_API_KEY,
                api_secret=TWITTER_API_SECRET,
                access_token=TWITTER_ACCESS_TOKEN,
                access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
                bearer_token=TWITTER_BEARER_TOKEN,
            )
            logger.info(f"Fetching media data for {ticker}...")
            news_articles = news_provider.get_everything(query=ticker, language="en")
            tweets, _ = twitter_provider.search_tweets(query=ticker, count=10)
            logger.info(
                f"Fetched {len(news_articles) if news_articles else 0} news articles and {len(tweets) if tweets else 0} tweets for {ticker}."
            )
            if news_articles:
                logger.info(f"  Latest news headline: {news_articles[0]['title']}")
            if tweets:
                logger.info(f"  Latest tweet: {tweets[0].text}")

            stock_data = StockData(
                ticker=ticker,
                price=price,
                volume=None,
                sma=sma,
                rsi=rsi,
                macd=macd,
                pe_ratio=get_pe_ratio(overview),
                peg_ratio=get_peg_ratio(overview),
                roe=get_roe(overview),
                revenue_growth=get_revenue_growth(overview),
                eps_growth=get_eps_growth(earnings),
                de_ratio=calculate_de_ratio(balance_sheet),
                news_articles=news_articles,
                tweets=tweets,
            )
            strategy_engine = StrategyEngine()
            signal, reasoning = strategy_engine.decide_trade(stock_data)
            logger.info(f"Trading signal for {ticker}: {signal.name}")
            logger.info(f"Reasoning: {reasoning}")

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
