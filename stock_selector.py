"""
Stock Selector Module
Filters stocks based on predictability criteria to build a trading universe.
"""

import pandas as pd
import numpy as np


class StockSelector:
    """
    Selects stocks suitable for the trading universe based on predictability metrics.
    Filters out highly unpredictable stocks.
    """
    
    def __init__(self, min_volatility=0.01, max_volatility=0.5, min_data_points=30):
        """
        Initialize the stock selector with filtering criteria.
        
        Args:
            min_volatility (float): Minimum acceptable volatility (too low = low liquidity)
            max_volatility (float): Maximum acceptable volatility (too high = unpredictable)
            min_data_points (int): Minimum number of data points required for analysis
        """
        self.min_volatility = min_volatility
        self.max_volatility = max_volatility
        self.min_data_points = min_data_points
    
    def calculate_volatility(self, prices):
        """
        Calculate annualized volatility of returns.
        
        Args:
            prices (pd.Series): Historical prices
            
        Returns:
            float: Annualized volatility
        """
        if len(prices) < 2:
            return np.nan
        
        returns = prices.pct_change().dropna()
        if len(returns) == 0:
            return np.nan
        
        # Annualized volatility (assuming daily data, 252 trading days)
        volatility = returns.std() * np.sqrt(252)
        return volatility
    
    def calculate_predictability_score(self, prices):
        """
        Calculate a predictability score based on multiple metrics.
        Higher score = more predictable.
        
        Args:
            prices (pd.Series): Historical prices
            
        Returns:
            float: Predictability score (0-1)
        """
        if len(prices) < self.min_data_points:
            return 0.0
        
        # Calculate volatility
        volatility = self.calculate_volatility(prices)
        if np.isnan(volatility):
            return 0.0
        
        # Volatility score (normalized between min and max)
        if volatility < self.min_volatility or volatility > self.max_volatility:
            volatility_score = 0.0
        else:
            # Linear scoring: optimal at middle of range
            mid_point = (self.min_volatility + self.max_volatility) / 2
            distance_from_mid = abs(volatility - mid_point)
            max_distance = (self.max_volatility - self.min_volatility) / 2
            volatility_score = 1.0 - (distance_from_mid / max_distance)
        
        # Calculate trend consistency (how often price moves in same direction)
        returns = prices.pct_change().dropna()
        if len(returns) < 2:
            return 0.0
        
        # Check for consistent patterns (autocorrelation)
        if len(returns) > 1:
            # Simple measure: what % of returns have same sign as previous
            same_direction = (returns[1:].values * returns[:-1].values > 0).sum()
            consistency_score = same_direction / (len(returns) - 1)
        else:
            consistency_score = 0.5
        
        # Combined score (weighted average)
        predictability = 0.6 * volatility_score + 0.4 * consistency_score
        return predictability
    
    def is_suitable(self, prices):
        """
        Determine if a stock is suitable for the trading universe.
        
        Args:
            prices (pd.Series): Historical prices
            
        Returns:
            bool: True if stock is suitable, False otherwise
        """
        if len(prices) < self.min_data_points:
            return False
        
        volatility = self.calculate_volatility(prices)
        if np.isnan(volatility):
            return False
        
        # Check volatility bounds
        if volatility < self.min_volatility or volatility > self.max_volatility:
            return False
        
        # Check predictability score threshold
        predictability = self.calculate_predictability_score(prices)
        return predictability > 0.3  # Minimum threshold
    
    def filter_stocks(self, stock_data):
        """
        Filter a dictionary of stocks to create a trading universe.
        
        Args:
            stock_data (dict): Dictionary with stock symbols as keys and price series as values
            
        Returns:
            list: List of suitable stock symbols
        """
        suitable_stocks = []
        
        for symbol, prices in stock_data.items():
            if self.is_suitable(prices):
                suitable_stocks.append(symbol)
        
        return suitable_stocks
