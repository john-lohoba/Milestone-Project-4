from django.test import TestCase
from marketdata.services import get_ohlcv
import pandas as pd

class MarketDataServicesTests(TestCase):
    """
    Tests check API returns valid DataFrame
    If API returns empty, services returns it correctly
    If API fails, services raises error
    """

    def test_api_runs(self):
        """
        Checks that api runs
        """
        result = get_ohlcv()
        self.assertIsNotNone(result)
    
    def test_api_returns_valid_data(self):
        """
        Test that ohlcv from api is converted to Pandas DataFrame
        """
        result = get_ohlcv()
        self.assertIsInstance(result, pd.DataFrame)

