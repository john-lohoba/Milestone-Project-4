from backtesting import Strategy
from backtesting.lib import FractionalBacktest
import pandas as pd


class RsiMeanReversion(Strategy):
    """
    RSI mean reversion strategy.
    """

    # Default values
    rsi_length = 14
    oversold = 30
    overbought = 70
    position_size = 0.02

    def init(self):
        def rsi(series, n):
            delta = pd.Series(series).diff()
            gain = delta.clip(lower=0).rolling(n).mean()
            loss = -delta.clip(upper=0).rolling(n).mean()
            rs = gain / loss
            return 100 - (100 / (1 + rs))

        close = self.data.Close
        self.rsi = self.I(lambda c: rsi(c, self.rsi_length), close)

    def next(self):
        rsi_value = self.rsi[-1]

        if rsi_value < self.oversold:
            if not self.position.is_long:
                self.position.close()
            self.buy(size=self.position_size)

        elif rsi_value > self.overbought:
            if not self.position.is_short:
                self.position.close()
            self.buy(size=self.position_size)
