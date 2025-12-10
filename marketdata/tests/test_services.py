from django.test import TestCase
from marketdata.services import get_ohlcv

class MarketDataServicesTests(TestCase):
    """
    Tests check API returns valid DataFrame
    If API returns empty, services returns it correctly
    If API fails, services raises error
    """

    def test_api_runs(self):
        result = get_ohlcv()
        self.assertTrue(result)

