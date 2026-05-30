from django import forms
from strategies.models import Strategy

SUPPORTED_SYMBOLS = [
    ("BTC", "Bitcoin"), 
    ("ETH", "Ethereum"), 
    ("SOL", "Solana")
    ]


class BacktestSubmissionForm(forms.Form):
    
    strategy = forms.ModelChoiceField(
        queryset=Strategy.objects.filter(name="EMA Crossover"))
    
    symbol = forms.ChoiceField(choices=SUPPORTED_SYMBOLS,)

    timeframe = forms.ChoiceField(choices=[("1d", "1D")])

    fast = forms.IntegerField(
        max_value=365,
        widget=forms.NumberInput(
            attrs={"placeholder": "Fast Ema e.g. 11"})
    )
    slow = forms.IntegerField(
        max_value=365,
        widget=forms.NumberInput(
            attrs={"placeholder": "Slow Ema e.g. 22"})
    )
    position_size = forms.DecimalField(
        max_value= 1,
        min_value = 0.01,
        

        widget=forms.NumberInput(attrs={
        "placeholder": "Position size e.g. 0.02",
        })
    )

    notes = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"placeholder": "Notes"}))

    def get_parameters(self):
        return {
            "fast": self.cleaned_data["fast"],
            "slow": self.cleaned_data["slow"],
            "position_size": float(
                self.cleaned_data["position_size"]
                ),
        }

