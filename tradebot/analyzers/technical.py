import logging
from typing import Optional
import pandas as pd
import pandas_ta as ta


logger = logging.getLogger(__name__)


def calculate_sma(data: pd.DataFrame, period: int = 5) -> Optional[pd.Series]:
    if data is None or "close_price" not in data.columns:
        return None
    if len(data) < period:
        return None

    sma = ta.sma(data["close_price"], length=period)
    return sma
