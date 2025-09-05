import logging
from typing import Optional
import pandas as pd
import pandas_ta as ta


logger = logging.getLogger(__name__)


def get_latest_indicator(data: pd.Series):
    if data is None or data.empty:
        logger.warning("No data available to get the latest indicator")
        return None

    return data.iloc[-1]


def calculate_sma(data: pd.DataFrame, period: int = 20) -> Optional[pd.Series]:
    if data is None or "close" not in data.columns:
        logger.warning("No data available or no close column found in data")
        return None

    if len(data) < period:
        return None

    try:
        sma = ta.sma(data["close"], length=period)
        return sma
    except Exception as e:
        logger.error(f"Failed to calculate SMA: {e}")
        return None


def calculate_rsi(data: pd.DataFrame, period: int = 14) -> Optional[pd.Series]:
    if data is None or "close" not in data.columns:
        logger.warning("No data available or no close column found in data")
        return None

    if len(data) < period:
        return None

    try:
        rsi = ta.rsi(data["close"], length=period)
        return rsi
    except Exception as e:
        logger.error(f"Failed to calculate RSI: {e}")
        return None


def calculate_macd(
    data: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9
) -> Optional[pd.DataFrame]:
    if data is None or "close" not in data.columns:
        logger.warning("No data available or no close column found in data")
        return None

    try:
        data.sort_index(inplace=True)
        macd = ta.macd(data["close"], fast=fast, slow=slow, signal=signal)
        return macd

    except Exception as e:
        logger.error(f"Failed to calculate MACD: {e}")
        return None
