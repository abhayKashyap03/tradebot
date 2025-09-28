from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union

from google import genai
from google.genai import types


class Signal(Enum):
    BUY = 1
    SELL = -1
    HOLD = 0


@dataclass
class TradeSignal:
    signal: Signal
    reasoning: str
    confidence: str


@dataclass
class StockData:
    ticker: str
    price: float
    volume: int
    sma: float
    rsi: float
    macd: float
    pe_ratio: float
    peg_ratio: float
    roe: float
    revenue_growth: float
    eps_growth: float
    de_ratio: float
    news_articles: List[dict]
    tweets: List

    def get_basic_info(self) -> Dict[str, Optional[Union[float, str]]]:
        return {
            "Ticker": self.ticker,
            "Latest Price": self.price,
            "Latest Volume": self.volume,
        }

    def get_fundamentals(self) -> Dict[str, Optional[float]]:
        return {
            "PE Ratio": self.pe_ratio,
            "PEG Ratio": self.peg_ratio,
            "ROE": self.roe,
            "Revenue Growth": self.revenue_growth,
            "EPS Growth": self.eps_growth,
            "D/E Ratio": self.de_ratio,
        }

    def get_technicals(self) -> Dict[str, Optional[float]]:
        return {
            "SMA": self.sma,
            "RSI": self.rsi,
            "MACD": self.macd,
        }

    def get_media(self) -> Dict[str, Optional[List[dict]]]:
        return {
            "News Articles": self.news_articles,
            "Tweets": self.tweets,
        }


class StrategyEngine:
    def __init__(self):
        self.llm_client = genai.Client()

    def _load_prompt_template(self, template_name: str) -> str:
        templates = {
            "basic_analysis": (
                "Given the following stock data:\n"
                "Basic Info: {basic_info}\n"
                "Fundamentals: {fundamentals}\n"
                "Technicals: {technicals}\n"
                "News Articles: {news_articles}\n"
                "Tweets: {tweets}\n"
                "Provide a concise trading signal (BUY, SELL, HOLD) with reasoning in this format:\n"
                "{\n"
                '"signal": BUY/SELL/HOLD,\n'
                '"reasoning": "Detailed reasoning here",\n'
                '"confidence": "High/Medium/Low"\n'
                "}"
            ),
        }
        return templates.get(template_name, "")

    def _format_prompt(self, template: str, stock_data: StockData) -> str:
        return template.format(
            basic_info=stock_data.get_basic_info(),
            fundamentals=stock_data.get_fundamentals(),
            technicals=stock_data.get_technicals(),
            news_articles=stock_data.news_articles[:3],
            tweets=[tweet.text for tweet in stock_data.tweets[:3]],
        )

    def decide_trade(
        self, stock_data: StockData, strategy: str = "basic_analysis"
    ) -> tuple[Signal, Any]:
        prompt_template = self._load_prompt_template(strategy)
        if not prompt_template:
            raise ValueError(f"Unknown strategy: {strategy}")

        prompt = self._format_prompt(prompt_template, stock_data)

        response = self.llm_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f'"role": "user", "content": "{prompt}"',
            config=types.GenerateContentConfig(
                system_instruction=[
                    "You are a financial trading assistant. \
                    Provide clear and concise trading signals based on the data provided \
                    along with a detailed research and reasoning for your decision.",
                ],
                response_mime_type="application/json",
                response_schema=list[TradeSignal],
            ),
        )

        answer = response.parsed

        if "BUY" in answer["signal"]:
            return Signal.BUY, answer
        elif "SELL" in answer["signal"]:
            return Signal.SELL, answer
        else:
            return Signal.HOLD, answer
