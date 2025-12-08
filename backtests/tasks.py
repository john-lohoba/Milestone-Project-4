from django.utils.timezone import now
from django.core.exceptions import ValidationError
from .models import BacktestRun, BacktestResult
from celery import shared_task
from backtesting.lib import FractionalBacktest

from strategies.registry import load_strategy_class

@shared_task(bin=True)
def run_backtest_task(self,run_id: int):
    """
    Executes backtests asynchronously
    """
    
    try:

        run = BacktestRun.objects.get(pk=run_id)
        run.mark_running()

        StrategyClass = load_strategy_class(run.strategy.python_class_path)
        df = get_ohlcv(
            symbol=run.symbol,
            timeframe=run.timeframe,
            start=run.start_date,
            end=run.end_date,
        )

        if df in None or df.empty:
            raise ValueError("Recieved empy market data.")
        
        bt = FractionalBacktest(
            df,
            StrategyClass,
            cash=10_000,
            trade_on_close=True,
        )

        results = bt.run(**run.parameters)

        BacktestResult.objects.create(
            run=run,
            data=results.to_dict(),
            trades=results._trades.to_dict("records"),
            equity_curve=results.equity_curve.to_dict(),
            raw_stats=results,
        )

        run.mark_completed()
        return True
    
    except Exception as exc:
        BacktestRun.objects.filter(pk=run_id).update(
            stats=BacktestRun.STATUS_FAILED,
            error_message=str(exc),
            finished_on=now(),
        )
        raise self.retry(exc=exc, countdown=5, max_retries=1)
    