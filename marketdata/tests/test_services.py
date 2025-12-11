from django.test import TestCase
from django.core.exceptions import ValidationError
from marketdata.services import get_ohlcv
import pandas as pd

class MarketDataServicesTests(TestCase):
    """
    Tests check API returns valid DataFrame
    If API returns empty, services returns it correctly
    If API fails, services raises error
    If invalid data is submitted validation error raised
    """

    def test_api_runs(self):
        """
        Checks that api runs
        """
        result = get_ohlcv("btc", 365)
        self.assertIsNotNone(result)
    
    def test_api_returns_valid_data(self):
        """
        Test that ohlcv from api is converted to Pandas DataFrame
        """
        result = get_ohlcv("sol", 365)
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_api_fails_with_invalid_coin(self):
        """
        Prevents api url submission if invalid coin symbol is given
        """
        with self.assertRaises(ValidationError):
            get_ohlcv("zcn", 365)

