import logging
import pandas as pd
from typing import Optional


logger = logging.getLogger(__name__)


def get_pe_ratio(fundamentals: pd.DataFrame) -> Optional[float]:
    """
    Get the Price-to-Earnings (P/E) ratio from the fundamentals DataFrame.

    Args:
        fundamentals (pd.DataFrame): The fundamentals DataFrame.

    Returns:
        Optional[float]: The P/E ratio if available, otherwise None.
    """
    try:
        return float(fundamentals["PERatio"].iloc[0])

    except KeyError as e:
        raise KeyError(f"Invalid column name: {e}") from e

    except Exception as e:
        logger.error(f"Error fetching P/E ratio: {e}")
        return None


def get_peg_ratio(fundamentals: pd.DataFrame) -> Optional[float]:
    """
    Get the Price-to-Earnings Growth (PEG) ratio from the fundamentals DataFrame.

    Args:
        fundamentals (pd.DataFrame): The fundamentals DataFrame.

    Returns:
        Optional[float]: The PEG ratio if available, otherwise None.
    """
    try:
        return float(fundamentals["PEGRatio"].iloc[0])

    except KeyError as e:
        raise KeyError(f"Invalid column name: {e}") from e

    except Exception as e:
        logger.error(f"Error fetching PEG ratio: {e}")
        return None


def get_roe(fundamentals: pd.DataFrame) -> Optional[float]:
    """
    Get the Return on Equity (ROE) from the fundamentals DataFrame.

    Args:
        fundamentals (pd.DataFrame): The fundamentals DataFrame.

    Returns:
        Optional[float]: The ROE if available, otherwise None.
    """
    try:
        return float(fundamentals["ReturnOnEquityTTM"].iloc[0])

    except KeyError as e:
        raise KeyError(f"Invalid column name: {e}") from e

    except Exception as e:
        logger.error(f"Error fetching ROE: {e}")
        return None


def get_revenue_growth(fundamentals: pd.DataFrame) -> Optional[float]:
    """
    Get the Revenue Growth from the fundamentals DataFrame.

    Args:
        fundamentals (pd.DataFrame): The fundamentals DataFrame.

    Returns:
        Optional[float]: The Revenue Growth if available, otherwise None.
    """
    try:
        return float(fundamentals["QuarterlyRevenueGrowthYOY"].iloc[0])

    except KeyError as e:
        raise KeyError(f"Invalid column name: {e}") from e

    except Exception as e:
        logger.error(f"Error fetching Revenue Growth: {e}")
        return None


def get_eps_growth(fundamentals: pd.DataFrame) -> Optional[float]:
    """
    Get the Earnings Per Share (EPS) growth YoY from the fundamentals DataFrame.

    Args:
        fundamentals (pd.DataFrame): The fundamentals DataFrame.

    Returns:
        Optional[float]: The EPS growth if available, otherwise None.
    """
    try:
        eps = fundamentals["reportedEPS"]
        now = eps.index.max()
        target_prev = eps.index.max() - pd.DateOffset(years=1)
        # find the index label closest to our target date
        prev = eps.index.get_indexer([target_prev], method="nearest")[0]
        return (
            100
            * (float(eps.loc[now]) - float(eps.iloc[prev]))
            / abs(float(eps.iloc[prev]))
        )

    except ZeroDivisionError:
        raise

    except KeyError as e:
        raise KeyError(f"Invalid column name: {e}") from e

    except Exception as e:
        logger.error(f"Error fetching EPS Growth: {e}")
        return None


def calculate_de_ratio(fundamentals: pd.DataFrame) -> Optional[float]:
    """
    Get the Debt/Equity Ratio from the fundamentals DataFrame.

    Args:
        fundamentals (pd.DataFrame): The fundamentals DataFrame.

    Returns:
        Optional[float]: The Debt/Equity Ratio if available, otherwise None.
    """
    try:
        latest = fundamentals.iloc[0]
        return float(latest["totalLiabilities"]) / float(
            latest["totalShareholderEquity"]
        )

    except KeyError as e:
        raise KeyError(f"Invalid column name: {e}") from e

    except Exception as e:
        logger.error(f"Error fetching Debt/Equity Ratio: {e}")
        return None
