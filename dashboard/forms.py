from django import forms
from backtests.models import BacktestRun

SUPPORTED_SYMBOLS = [("BTC", "Bitcoin"), ("ETH", "Ethereum"), ("SOL", "Solana")]
class BacktestSubmissionForm(forms.ModelForm):
    class Meta:
        model = BacktestRun
        fields = ("strategy", "symbol", "timeframe", "parameters")
        widgets = {"symbol": forms.Select(choices=[("BTC", "Bitcoin"), ("ETH", "Ethereum"), ("SOL", "Solana")])}