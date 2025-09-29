import unittest
import pandas as pd
from tradebot.analyzers.technical import calculate_sma


class TestTechnicalAnalyzers(unittest.TestCase):
    def test_calculate_sma(self):
        # Test with enough data
        data = pd.DataFrame({"close": [10, 12, 15, 14, 16, 18, 20]})
        sma = calculate_sma(data, period=5)
        self.assertIsNotNone(sma)
        self.assertEqual(len(sma), len(data))
        self.assertAlmostEqual(sma.iloc[-1], 16.6)

        # Test with not enough data
        data = pd.DataFrame({"close": [10, 12, 15]})
        sma = calculate_sma(data, period=5)
        self.assertIsNone(sma)

        # Test with no data
        data = pd.DataFrame({"close": []})
        sma = calculate_sma(data, period=5)
        self.assertIsNone(sma)

        # Test with None data
        sma = calculate_sma(None, period=5)
        self.assertIsNone(sma)


if __name__ == "__main__":
    unittest.main()
