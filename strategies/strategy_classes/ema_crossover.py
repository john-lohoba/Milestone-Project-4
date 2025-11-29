from backtesting import Strategy
from backtesting.lib import crossover
import pandas as pd


class EmaCrossover(Strategy):
    """
    Simple trend following strategy with (EMAs),
    Exponential Moving Averages.
    """

    # Default values
    fast = 12
    slow = 26

    def init(self):
        close = self.data.Close

        self.fast_ema = self.I(
            lambda c: pd.Series(c).ewm(span=self.fast, adjust=False).mean(),
            close,
        )

        self.slow_ema = self.I(
            lambda c: pd.Series(c).ewm(span=self.slow, adjust=False).mean(),
            close,
        )

    def next(self):
        if crossover(self.fast_ema, self.slow_ema):  # type: ignore[arg-type]
            if not self.position.is_long:
                self.position.close()
            self.buy()

        elif crossover(self.slow_ema, self.fast_ema):  # type: ignore[arg-type]
            if not self.position.is_short:
                self.position.close()
            self.sell()
