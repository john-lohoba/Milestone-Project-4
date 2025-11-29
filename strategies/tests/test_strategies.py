from django.test import TestCase
from backtesting.lib import FractionalBacktest
from backtesting.test import BTCUSD


class StrategyTests(TestCase):
    """
    Test checks if the stats object is returned after
    running the strategie,
    confirming that the strategie class isn't broken.
    These test are run against BTCUSD data from backtesting.test
    """

    def test_ema_crossover_runs(self):
        from strategies.strategy_classes.ema_crossover import EmaCrossover

        bt = FractionalBacktest(BTCUSD, EmaCrossover, cash=10_000)
        stats = bt.run()
        # Checks if return value exists in stats object
        self.assertIn("Return [%]", stats.keys(), msg="Ema crossover test failed")

    def test_rsi_mean_reversion_runs(self):
        from strategies.strategy_classes.rsi_mean_reversion import RsiMeanReversion

        bt = FractionalBacktest(BTCUSD, RsiMeanReversion, cash=10_000)
        stats = bt.run()

        self.assertIn("Return [%]", stats.keys(), msg="RSI mean reversion test failed")

    def test_bollinger_breakout_runs(self):
        from strategies.strategy_classes.bollinger_breakout import BollingerBreakout

        bt = FractionalBacktest(BTCUSD, BollingerBreakout, cash=10_000)
        stats = bt.run()

        self.assertIn("Return [%]", stats.keys(), msg="Bollinger breakout test failed")
