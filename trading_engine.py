"""
Trading Engine Module
Implements the core trading logic for buying and selling stocks.
"""

import pandas as pd
import numpy as np


class TradingEngine:
    """
    Executes trading logic based on weekly price changes.
    - Buy $5 if stock drops 5% or more in the last week
    - Sell $10 if stock rises 10% or more in the last week
    """
    
    def __init__(self, buy_threshold=-0.05, sell_threshold=0.10, 
                 buy_amount=5.0, sell_amount=10.0):
        """
        Initialize the trading engine with trading parameters.
        
        Args:
            buy_threshold (float): Percentage drop to trigger buy (negative value, e.g., -0.05 for 5% drop)
            sell_threshold (float): Percentage rise to trigger sell (positive value, e.g., 0.10 for 10% rise)
            buy_amount (float): Dollar amount to buy when triggered
            sell_amount (float): Dollar amount to sell when triggered
        """
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.buy_amount = buy_amount
        self.sell_amount = sell_amount
    
    def calculate_weekly_change(self, prices):
        """
        Calculate the percentage change over the last week (7 days).
        
        Args:
            prices (pd.Series): Historical prices (indexed by date)
            
        Returns:
            float: Percentage change over the last week, or None if insufficient data
        """
        if len(prices) < 2:
            return None
        
        # Get the most recent price
        current_price = prices.iloc[-1]
        
        # Get price from 7 days ago (or closest available)
        if len(prices) >= 7:
            week_ago_price = prices.iloc[-7]
        else:
            # Use earliest available price if less than 7 days of data
            week_ago_price = prices.iloc[0]
        
        if np.isnan(week_ago_price) or np.isnan(current_price) or abs(week_ago_price) < 1e-10:
            return None
        
        # Calculate percentage change
        pct_change = (current_price - week_ago_price) / week_ago_price
        return pct_change
    
    def generate_signal(self, prices):
        """
        Generate a trading signal (BUY, SELL, or HOLD) based on weekly price change.
        
        Args:
            prices (pd.Series): Historical prices
            
        Returns:
            tuple: (signal, amount, pct_change) where signal is 'BUY', 'SELL', or 'HOLD'
        """
        pct_change = self.calculate_weekly_change(prices)
        
        if pct_change is None:
            return ('HOLD', 0.0, None)
        
        # Check for buy signal (price dropped by threshold or more)
        if pct_change <= self.buy_threshold:
            return ('BUY', self.buy_amount, pct_change)
        
        # Check for sell signal (price rose by threshold or more)
        elif pct_change >= self.sell_threshold:
            return ('SELL', self.sell_amount, pct_change)
        
        # No signal
        else:
            return ('HOLD', 0.0, pct_change)
    
    def execute_trades(self, stock_data):
        """
        Execute trades for all stocks in the trading universe.
        
        Args:
            stock_data (dict): Dictionary with stock symbols as keys and price series as values
            
        Returns:
            dict: Dictionary with stock symbols as keys and trade details as values
        """
        trades = {}
        
        for symbol, prices in stock_data.items():
            signal, amount, pct_change = self.generate_signal(prices)
            
            if signal != 'HOLD':
                current_price = prices.iloc[-1] if len(prices) > 0 else None
                shares = amount / current_price if current_price and abs(current_price) > 1e-10 else 0
                
                trades[symbol] = {
                    'signal': signal,
                    'amount': amount,
                    'shares': shares,
                    'price': current_price,
                    'weekly_change': pct_change
                }
        
        return trades
    
    def get_trade_summary(self, trades):
        """
        Generate a summary of all trades.
        
        Args:
            trades (dict): Dictionary of trades from execute_trades()
            
        Returns:
            dict: Summary statistics
        """
        if not trades:
            return {
                'total_buys': 0,
                'total_sells': 0,
                'buy_value': 0.0,
                'sell_value': 0.0,
                'net_position': 0.0
            }
        
        buy_trades = [t for t in trades.values() if t['signal'] == 'BUY']
        sell_trades = [t for t in trades.values() if t['signal'] == 'SELL']
        
        total_buys = len(buy_trades)
        total_sells = len(sell_trades)
        buy_value = sum(t['amount'] for t in buy_trades)
        sell_value = sum(t['amount'] for t in sell_trades)
        
        return {
            'total_buys': total_buys,
            'total_sells': total_sells,
            'buy_value': buy_value,
            'sell_value': sell_value,
            'net_position': sell_value - buy_value
        }
