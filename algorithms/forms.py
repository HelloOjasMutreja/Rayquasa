from django import forms
from .models import TradingAlgorithm, BacktestResult


class TradingAlgorithmForm(forms.ModelForm):
    """Form for creating/editing trading algorithms"""
    
    class Meta:
        model = TradingAlgorithm
        fields = [
            'name', 'description',
            'buy_threshold', 'sell_threshold', 'buy_amount', 'sell_amount',
            'min_volatility', 'max_volatility', 'min_data_points'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'buy_threshold': forms.NumberInput(attrs={'step': '0.01'}),
            'sell_threshold': forms.NumberInput(attrs={'step': '0.01'}),
            'buy_amount': forms.NumberInput(attrs={'step': '0.01'}),
            'sell_amount': forms.NumberInput(attrs={'step': '0.01'}),
            'min_volatility': forms.NumberInput(attrs={'step': '0.01'}),
            'max_volatility': forms.NumberInput(attrs={'step': '0.01'}),
        }


class BacktestForm(forms.Form):
    """Form for running a backtest"""
    
    STOCK_UNIVERSES = {
        'default': 'AAPL, GOOGL, MSFT, AMZN, TSLA, META, NVDA, JPM',
        'tech': 'AAPL, GOOGL, MSFT, META, NVDA, AMD, INTC, CSCO, ORCL, IBM',
        'finance': 'JPM, BAC, WFC, GS, MS, C, USB, PNC, TFC, COF',
        'energy': 'XOM, CVX, COP, SLB, EOG, MPC, PSX, VLO, OXY, HAL',
        'healthcare': 'JNJ, UNH, PFE, MRK, ABBV, TMO, DHR, ABT, LLY, BMY',
        'consumer': 'AMZN, WMT, HD, MCD, NKE, SBUX, TGT, LOW, TJX, COST',
        'small': 'AAPL, MSFT, GOOGL',
    }
    
    universe = forms.ChoiceField(
        choices=[(k, k.title()) for k in STOCK_UNIVERSES.keys()],
        required=False,
        initial='default',
        help_text='Select a predefined stock universe or enter custom symbols below'
    )
    
    symbols = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g., AAPL, MSFT, GOOGL'}),
        help_text='Comma-separated stock symbols (leave blank to use selected universe)'
    )
    
    weeks = forms.IntegerField(
        initial=52,
        min_value=1,
        max_value=260,
        help_text='Number of weeks to backtest (1-260)'
    )
    
    initial_cash = forms.FloatField(
        initial=10000.0,
        min_value=100.0,
        help_text='Initial portfolio cash'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        symbols = cleaned_data.get('symbols', '').strip()
        universe = cleaned_data.get('universe')
        
        # Use universe if no custom symbols provided
        if not symbols and universe:
            cleaned_data['symbols'] = self.STOCK_UNIVERSES[universe]
        elif not symbols:
            raise forms.ValidationError('Please either select a universe or enter custom symbols')
        
        return cleaned_data
