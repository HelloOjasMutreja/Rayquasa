from django.contrib import admin
from .models import TradingAlgorithm, BacktestResult


@admin.register(TradingAlgorithm)
class TradingAlgorithmAdmin(admin.ModelAdmin):
    list_display = ['name', 'buy_threshold', 'sell_threshold', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description')
        }),
        ('Trading Parameters', {
            'fields': ('buy_threshold', 'sell_threshold', 'buy_amount', 'sell_amount')
        }),
        ('Stock Selection Parameters', {
            'fields': ('min_volatility', 'max_volatility', 'min_data_points')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BacktestResult)
class BacktestResultAdmin(admin.ModelAdmin):
    list_display = ['algorithm', 'symbols', 'total_return_pct', 'total_trades', 'created_at']
    list_filter = ['algorithm', 'created_at']
    search_fields = ['algorithm__name', 'symbols']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Configuration', {
            'fields': ('algorithm', 'symbols', 'weeks', 'initial_cash')
        }),
        ('Results', {
            'fields': ('final_value', 'total_return_pct', 'max_drawdown_pct', 
                      'total_trades', 'buy_trades', 'sell_trades')
        }),
        ('Detailed Data', {
            'fields': ('trade_log', 'portfolio_history', 'final_holdings'),
            'classes': ('collapse',)
        }),
        ('Visualization', {
            'fields': ('chart_path',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

