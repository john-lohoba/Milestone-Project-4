from django.utils.timezone import now
from django.core.exceptions import ValidationError
from .models import BacktestRun, BacktestResult
from celery import shared_task
from backtesting.lib import FractionalBacktest

from strategies.registry import load_strategy_class
from marketdata.services import get_ohlcv
import pandas as pd
import numpy as np
import json


def df_to_json_records(df: pd.DataFrame):
    return json.loads(
        df.to_json(orient="records", date_format="iso")
    )


def series_to_json_dict(s: pd.Series):
    return json.loads(
        s.to_json(date_format="iso")
    )


@shared_task(bind=True)
def run_backtest_task(self, run_id: int):
    try:
        run = BacktestRun.objects.get(pk=run_id)
        run.mark_running()

        StrategyClass = load_strategy_class(run.strategy.python_class_path)
        df = get_ohlcv(symbol=run.symbol, days=365)

        if df is None or df.empty:
            raise ValidationError("Received empty market data.")

        bt = FractionalBacktest(
            df,
            StrategyClass,
            cash=10_000,
            trade_on_close=True,
        )

        stats = bt.run(**run.parameters)

        BacktestResult.objects.create(
            run=run,
            data=series_to_json_dict(stats),
            raw_stats=series_to_json_dict(stats),
            trades=df_to_json_records(stats._trades),
            equity_curve=df_to_json_records(stats._equity_curve.reset_index()),
        )

        run.mark_completed()
        return True

    except Exception as exc:
        BacktestRun.objects.filter(pk=run_id).update(
            status=BacktestRun.STATUS_FAILED,
            error_message=str(exc),
            finished_on=now(),
        )
        raise self.retry(exc=exc, countdown=5, max_retries=1)


