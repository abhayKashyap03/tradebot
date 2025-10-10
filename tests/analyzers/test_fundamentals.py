import unittest
import pandas as pd
from tradebot.analyzers.fundamentals import (
    get_pe_ratio,
    get_peg_ratio,
    get_roe,
    get_revenue_growth,
    get_eps_growth,
    calculate_de_ratio,
)


class TestFundamentals(unittest.TestCase):
    def test_get_pe_ratio_success(self):
        data = {"PERatio": ["25.0"]}
        df = pd.DataFrame(data)
        self.assertEqual(get_pe_ratio(df), 25.0)

    def test_get_peg_ratio_success(self):
        data = {"PEGRatio": ["1.5"]}
        df = pd.DataFrame(data)
        self.assertEqual(get_peg_ratio(df), 1.5)

    def test_get_roe_success(self):
        data = {"ReturnOnEquityTTM": ["0.15"]}
        df = pd.DataFrame(data)
        self.assertEqual(get_roe(df), 0.15)

    def test_get_revenue_growth_success(self):
        data = {"QuarterlyRevenueGrowthYOY": ["0.1"]}
        df = pd.DataFrame(data)
        self.assertEqual(get_revenue_growth(df), 0.1)

    def test_get_eps_growth_success(self):
        data = {"reportedEPS": ["1.0", "1.2"]}
        index = pd.to_datetime(["2022-01-01", "2023-01-01"])
        df = pd.DataFrame(data, index=index)
        self.assertAlmostEqual(get_eps_growth(df), 20.0)

    def test_calculate_de_ratio_success(self):
        data = {"totalLiabilities": [100], "totalShareholderEquity": [200]}
        df = pd.DataFrame(data)
        self.assertEqual(calculate_de_ratio(df), 0.5)

    def test_get_pe_ratio_missing_column(self):
        data = {"SomeOtherRatio": ["25.0"]}
        df = pd.DataFrame(data)
        with self.assertRaises(KeyError):
            get_pe_ratio(df)


if __name__ == "__main__":
    unittest.main()
