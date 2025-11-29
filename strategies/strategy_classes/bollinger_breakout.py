from backtesting import Strategy
import pandas as pd


class BollingerBreakout(Strategy):
    """
    Bollinger Bands Breakout Strategy.
    Buy when price breaks ABOVE the upper band.
    Sell/short when price breaks BELOW the lower band.
    """

    length = 20
    std_dev = 2.0
    position_size = 0.02

    def init(self):
        close = self.data.Close

        self.mid = self.I(lambda c: pd.Series(c).rolling(self.length).mean(), close)
        self.std = self.I(lambda c: pd.Series(c).rolling(self.length).std(), close)

        self.upper = self.mid + self.std_dev * self.std
        self.lower = self.mid - self.std_dev * self.std

    def next(self):
        price = self.data.Close[-1]

        if price > self.upper[-1]:
            if not self.position.is_long:
                self.position.close()
                self.buy(size=self.position_size)

        elif price < self.lower[-1]:
            if not self.position.is_short:
                self.position.close()
                self.sell(size=self.position_size)
