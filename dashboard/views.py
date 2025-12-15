from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import BacktestSubmissionForm
from strategies.models import Strategy
from backtests.tasks import run_backtest_task


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
    if request.method == "POST":
        backtest_form = BacktestSubmissionForm(request.POST)
        if backtest_form.is_valid():
            form = backtest_form.save(commit=False)
            form.user = request.user
            form.save()
            run_backtest_task(form.pk)
            print("WORKING TEST SENT")
        else:
            print("FAILED TO RUN TEST")
            print(backtest_form)
    return redirect("backtest-view")