from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import json


class TradingAlgorithm(models.Model):
    """Model to store custom trading algorithms"""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    # Algorithm parameters
    buy_threshold = models.FloatField(
        default=-0.05,
        validators=[MaxValueValidator(0)],
        help_text="Percentage drop to trigger buy (negative value, e.g., -0.05 for 5% drop)"
    )
    sell_threshold = models.FloatField(
        default=0.10,
        validators=[MinValueValidator(0)],
        help_text="Percentage rise to trigger sell (positive value, e.g., 0.10 for 10% rise)"
    )
    buy_amount = models.FloatField(
        default=5.0,
        validators=[MinValueValidator(0.01)],
        help_text="Dollar amount to buy when triggered"
    )
    sell_amount = models.FloatField(
        default=10.0,
        validators=[MinValueValidator(0.01)],
        help_text="Dollar amount to sell when triggered"
    )
    
    # Stock selection parameters
    min_volatility = models.FloatField(
        default=0.01,
        validators=[MinValueValidator(0)],
        help_text="Minimum acceptable volatility"
    )
    max_volatility = models.FloatField(
        default=0.5,
        validators=[MinValueValidator(0)],
        help_text="Maximum acceptable volatility"
    )
    min_data_points = models.IntegerField(
        default=30,
        validators=[MinValueValidator(1)],
        help_text="Minimum data points required"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_selector_config(self):
        """Get configuration for StockSelector"""
        return {
            'min_volatility': self.min_volatility,
            'max_volatility': self.max_volatility,
            'min_data_points': self.min_data_points
        }
    
    def get_trading_config(self):
        """Get configuration for TradingEngine"""
        return {
            'buy_threshold': self.buy_threshold,
            'sell_threshold': self.sell_threshold,
            'buy_amount': self.buy_amount,
            'sell_amount': self.sell_amount
        }


class BacktestResult(models.Model):
    """Model to store backtest results"""
    
    algorithm = models.ForeignKey(TradingAlgorithm, on_delete=models.CASCADE, related_name='backtests')
    
    # Test configuration
    symbols = models.TextField(help_text="Comma-separated stock symbols")
    weeks = models.IntegerField(default=52)
    initial_cash = models.FloatField(default=10000.0)
    
    # Results
    final_value = models.FloatField(null=True, blank=True)
    total_return_pct = models.FloatField(null=True, blank=True)
    max_drawdown_pct = models.FloatField(null=True, blank=True)
    total_trades = models.IntegerField(null=True, blank=True)
    buy_trades = models.IntegerField(null=True, blank=True)
    sell_trades = models.IntegerField(null=True, blank=True)
    
    # Detailed results stored as JSON
    trade_log = models.TextField(blank=True, help_text="JSON-encoded trade log")
    portfolio_history = models.TextField(blank=True, help_text="JSON-encoded portfolio history")
    final_holdings = models.TextField(blank=True, help_text="JSON-encoded final holdings")
    
    # Visualization
    chart_path = models.CharField(max_length=255, blank=True, help_text="Path to result chart")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.algorithm.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    def get_symbols_list(self):
        """Get symbols as a list"""
        return [s.strip().upper() for s in self.symbols.split(',') if s.strip()]
    
    def set_symbols_list(self, symbols_list):
        """Set symbols from a list"""
        self.symbols = ', '.join(symbols_list)
    
    def get_trade_log(self):
        """Get trade log as Python object"""
        if self.trade_log:
            return json.loads(self.trade_log)
        return []
    
    def set_trade_log(self, trade_log):
        """Set trade log from Python object"""
        self.trade_log = json.dumps(trade_log, default=str)
    
    def get_portfolio_history(self):
        """Get portfolio history as Python object"""
        if self.portfolio_history:
            return json.loads(self.portfolio_history)
        return []
    
    def set_portfolio_history(self, history):
        """Set portfolio history from Python object"""
        self.portfolio_history = json.dumps(history, default=str)
    
    def get_final_holdings(self):
        """Get final holdings as Python object"""
        if self.final_holdings:
            return json.loads(self.final_holdings)
        return {}
    
    def set_final_holdings(self, holdings):
        """Set final holdings from Python object"""
        self.final_holdings = json.dumps(holdings)

