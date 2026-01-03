from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.timezone import now

from .forms import BacktestSubmissionForm
from strategies.models import Strategy
from backtests.tasks import run_backtest_task
from backtests.models import BacktestRun, BacktestResult
from subscription.models import UserSubscription


@login_required
def backtest_view(request):
    """
    view to display backtest form
    """
    PARAMETERS = {
        "bollinger_bands":{
            "length": "number",
            "std_dev": "number",
            "position_size":"number", 
        },
        "ema_crossover":{
            "fast": "number",
            "slow": "number",
            "position_size": "number"
        },
        "rsi_mean_reversion":{
            "rsi_length": "number",
            "oversold": "number",
            "overbought": "number",
            "position_size": "number",
        }
    }
    form = BacktestSubmissionForm()
    strategies = Strategy.objects.all().values(
        "id", "name", "parameters_schema"
    )

    return render(request, "dashboard/new_backtest.html",
                    {
                        "form": form,
                        "strategies": list(strategies),
                        "parameters": PARAMETERS,
                        })


@login_required
def backtest_post(request):
    """
    View to handle backtest post requests.
    """
    if request.method == "POST":
        backtest_form = BacktestSubmissionForm(request.POST)
    
        if backtest_form.is_valid():
            backtest = BacktestRun.objects.create(
                user = request.user,
                strategy = backtest_form.cleaned_data["strategy"],
                symbol = backtest_form.cleaned_data["symbol"],
                timeframe = backtest_form.cleaned_data["timeframe"],
                parameters = backtest_form.get_parameters(),
            )
            run_backtest_task(backtest.pk)
            messages.add_message(request, messages.SUCCESS, "New Backtest submitted")
        else:
            messages.add_message(request, messages.ERROR, "Error submitting backtest")
    return redirect("backtest-list")



ALLOWED_STATS = [
    "Start",
    "End",
    "Duration",
    "Exposure Time [%]",
    "Equity Final [$]",
    "Equity Peak [$]",
    "Return [%]",
    "Buy & Hold Return [%]",
    "Return (Ann.) [%]",
    "Volatility (Ann.) [%]",
    "CAGR [%]",
    "Sharpe Ratio",
    "Sortino Ratio",
    "Calmar Ratio",
    "Alpha [%]",
    "Beta",
    "Max. Drawdown [%]",
    "Avg. Drawdown [%]",
    "Max. Drawdown Duration",
    "Avg. Drawdown Duration",
    "# Trades",
    "Win Rate [%]",
    "Best Trade [%]",
    "Worst Trade [%]",
    "Avg. Trade [%]",
    "Max. Trade Duration",
    "Avg. Trade Duration",
    "Profit Factor",
    "Expectancy [%]",
    "SQN",
    "Kelly Criterion",
]


@login_required
def backtest_detail(request, run_id):
    """
    Displays the results of a completed backtest.
    """
    run = get_object_or_404(BacktestRun, pk=run_id, user=request.user)

    if run.status != BacktestRun.STATUS_COMPLETED:
        
        return render(request, "dashboard/backtest_result.html", {"run": run})
    
    raw_stats = run.result.raw_stats  # type: ignore

    result = run.result  # type: ignore
    filtered_stats = {
        key: raw_stats.get(key)
        for key in ALLOWED_STATS
        if key in raw_stats
    }
    context = {
        "run": run,
        "result": result,
        "stats": filtered_stats,
        "trades": result.trades,
        "equity_curve": result.equity_curve,
    }
    return render(request, "dashboard/backtest_detail.html", context)


@login_required
def backtest_list(request):
    """
    Display all backtests submitted by the logged-in user.
    """
    runs = (
        BacktestRun.objects
        .filter(user=request.user)
        .select_related("strategy")
        .order_by("-created_on")
    )

    paginator = Paginator(runs, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    user = request.user
    subscription = getattr(user, "usersubscription", None)
    today_count = BacktestRun.objects.filter(user=user, created_on__date=now().date()).count()


    return render(request, "dashboard/backtest_list.html",
                  {
                      "runs": runs,
                      "page_obj": page_obj,
                      "subscription": subscription,
                      "today_count": today_count,
                      })