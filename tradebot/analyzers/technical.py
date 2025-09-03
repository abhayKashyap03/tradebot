import logging
from typing import Optional
import pandas as pd
import pandas_ta as ta


logger = logging.getLogger(__name__)


def get_latest_indicator(data: pd.Series):
    if data is None or data.empty:
        return None
    return data.iloc[-1]


def calculate_sma(data: pd.DataFrame, period: int = 20) -> Optional[pd.Series]:
    if data is None or "close_price" not in data.columns:
        return None
    if len(data) < period:
        return None

    try:
        sma = ta.sma(data["close_price"], length=period)
        return sma
    except Exception as e:
        logger.error(f"Failed to calculate SMA: {e}")
        return None


def calculate_rsi(data: pd.DataFrame, period: int = 14) -> Optional[pd.Series]:
    if data is None or "close_price" not in data.columns:
        return None
    if len(data) < period:
        return None

    try:
        rsi = ta.rsi(data["close_price"], length=period)
        return rsi
    except Exception as e:
        logger.error(f"Failed to calculate RSI: {e}")
        return None


def calculate_macd(
    data: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9
) -> Optional[pd.DataFrame]:
    if data is None or "close_price" not in data.columns:
        return None

    try:
        macd = ta.macd(data["close_price"], fast=fast, slow=slow, signal=signal)
        return macd
    except Exception as e:
        logger.error(f"Failed to calculate MACD: {e}")
        return None
