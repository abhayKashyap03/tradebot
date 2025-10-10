import logging
from enum import Enum
from typing import Tuple, Optional, Dict
from google import genai
from google.genai.types import GenerateContentConfig

from tradebot.strategy import StockData
from tradebot.configs.config import (
    MAX_POSITION_SIZE,
    MAX_DAILY_TRADES,
    MAX_PORTFOLIO_SHARE,
)
from tradebot.clients.robinhood_client import RobinhoodClient


logger = logging.getLogger(__name__)


class TradeDecision(Enum):
    APPROVED = 1
    VETOED = -1


class RiskDecision:
    decision: TradeDecision
    reasoning: str


class RiskManager:
    def __init__(self, rh_client: RobinhoodClient):
        self.llm_client = genai.Client()
        self.rh_client = rh_client
        self.daily_trades = 0

    def can_trade(self) -> bool:
        if self.daily_trades >= MAX_DAILY_TRADES:
            logger.info("Reached maximum daily trades limit.")
            return False
        return True

    def assess_risk(
        self, stock_data: StockData, portfolio: Dict
    ) -> Optional[Tuple[TradeDecision, dict]]:
        if not self.can_trade():
            return TradeDecision.VETOED, {
                "decision": TradeDecision.VETOED,
                "reasoning": "Exceeded max daily number of trades.",
            }

        prompt = (
            f"Given the following stock data:\n"
            f"Ticker: {stock_data.ticker}\n"
            f"Price: {stock_data.price}\n"
            f"SMA: {stock_data.sma}\n"
            f"RSI: {stock_data.rsi}\n"
            f"MACD: {stock_data.macd}\n"
            f"PE Ratio: {stock_data.pe_ratio}\n"
            f"PEG Ratio: {stock_data.peg_ratio}\n"
            f"ROE: {stock_data.roe}\n"
            f"Revenue Growth: {stock_data.revenue_growth}\n"
            f"EPS Growth: {stock_data.eps_growth}\n"
            f"D/E Ratio: {stock_data.de_ratio}\n"
            f"News Articles: {stock_data.news_articles} articles\n"
            f"Tweets: {stock_data.tweets} tweets\n"
            f"Portfolio: {portfolio}\n\n"
            "Evaluate the risk of trading this stock and respond with 'APPROVE' or 'REJECT'.\n"
            "Consider factors like volatility, fundamentals, and market sentiment.\n"
            "Along with the decision, provide the position size you think is appropriate, "
            f"if the trade is safe and the maximum size for one trade is ${MAX_POSITION_SIZE}."
            f"Make sure the position is not over {MAX_PORTFOLIO_SHARE}% of the total portfolio."
        )

        try:
            response = self.llm_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f'"role": "user", "content": {prompt}',
                config=GenerateContentConfig(
                    system_instruction=[
                        "You are a risk management assistant. \
                        Provide clear and concise risk analyses based on the data provided \
                        along with a detailed research and reasoning for your decision."
                    ],
                    response_mime_type="application/json",
                    response_schema=RiskDecision,
                ),
            )

            decision = response.parsed
            if "APPROVED" in decision["decision"]:
                logger.info(f"Risk assessment APPROVED for {stock_data.ticker}.")
                self.daily_trades += 1
                return TradeDecision.APPROVED, decision
            else:
                logger.info(f"Risk assessment REJECTED for {stock_data.ticker}.")
                return TradeDecision.VETOED, decision

        except Exception as e:
            logger.error(f"Risk assessment failed for {stock_data.ticker}: {e}")
            return None
