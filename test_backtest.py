"""
Test script for the backtesting functionality
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from backtest import Portfolio, Backtester


class TestPortfolio(unittest.TestCase):
    """Test Portfolio class"""
    
    def test_initial_state(self):
        """Test portfolio initialization"""
        portfolio = Portfolio(initial_cash=10000.0)
        self.assertEqual(portfolio.cash, 10000.0)
        self.assertEqual(len(portfolio.holdings), 0)
    
    def test_buy(self):
        """Test buying stocks"""
        portfolio = Portfolio(initial_cash=10000.0)
        
        # Buy 10 shares at $100 each
        success = portfolio.buy('AAPL', 10, 100)
        self.assertTrue(success)
        self.assertEqual(portfolio.cash, 9000.0)
        self.assertEqual(portfolio.holdings['AAPL'], 10)
        
        # Try to buy more than we can afford
        success = portfolio.buy('MSFT', 100, 200)
        self.assertFalse(success)
        self.assertEqual(portfolio.cash, 9000.0)
        self.assertNotIn('MSFT', portfolio.holdings)
    
    def test_sell(self):
        """Test selling stocks"""
        portfolio = Portfolio(initial_cash=10000.0)
        
        # Buy and then sell
        portfolio.buy('AAPL', 10, 100)
        success = portfolio.sell('AAPL', 5, 110)
        
        self.assertTrue(success)
        self.assertEqual(portfolio.holdings['AAPL'], 5)
        self.assertEqual(portfolio.cash, 9000.0 + 5 * 110)
        
        # Try to sell more than we have
        success = portfolio.sell('AAPL', 10, 110)
        self.assertFalse(success)
    
    def test_get_value(self):
        """Test portfolio value calculation"""
        portfolio = Portfolio(initial_cash=10000.0)
        
        # Buy some stocks
        portfolio.buy('AAPL', 10, 100)  # $1000
        portfolio.buy('MSFT', 20, 50)   # $1000
        
        # Portfolio should be $8000 cash + holdings value
        current_prices = {'AAPL': 110, 'MSFT': 60}
        value = portfolio.get_value(current_prices)
        
        expected = 8000 + (10 * 110) + (20 * 60)
        self.assertEqual(value, expected)
    
    def test_record_state(self):
        """Test recording portfolio state"""
        portfolio = Portfolio(initial_cash=10000.0)
        
        date = datetime.now()
        current_prices = {'AAPL': 100}
        
        portfolio.buy('AAPL', 10, 100)
        portfolio.record_state(date, current_prices)
        
        self.assertEqual(len(portfolio.history), 1)
        self.assertEqual(portfolio.history[0]['cash'], 9000.0)
        self.assertEqual(portfolio.history[0]['total_value'], 10000.0)


class TestBacktester(unittest.TestCase):
    """Test Backtester class"""
    
    def create_mock_data(self, symbols, days=90):
        """Create mock stock data for testing"""
        stock_data = {}
        dates = pd.date_range(end=pd.Timestamp.now(), periods=days, freq='D')
        
        for i, symbol in enumerate(symbols):
            # Create prices with some volatility and trend
            base_price = 100 + i * 20
            trend = np.linspace(0, 10, days)
            noise = np.random.randn(days) * 5
            prices = base_price + trend + noise
            
            # Add a couple of buy signals (drops > 5%)
            if days > 14:
                prices[30:37] = prices[30] * np.linspace(1.0, 0.93, 7)  # 7% drop
            
            # Add a couple of sell signals (rises > 10%)
            if days > 28:
                prices[60:67] = prices[60] * np.linspace(1.0, 1.12, 7)  # 12% rise
            
            stock_data[symbol] = pd.Series(prices, index=dates)
        
        return stock_data
    
    def test_backtester_initialization(self):
        """Test backtester initialization"""
        symbols = ['AAPL', 'MSFT']
        backtester = Backtester(symbols, weeks=12, initial_cash=10000.0)
        
        self.assertEqual(backtester.symbols, symbols)
        self.assertEqual(backtester.weeks, 12)
        self.assertEqual(backtester.initial_cash, 10000.0)
        self.assertEqual(backtester.portfolio.cash, 10000.0)
    
    def test_backtest_run(self):
        """Test running a backtest"""
        symbols = ['STOCK_A', 'STOCK_B']
        backtester = Backtester(symbols, weeks=12, initial_cash=10000.0)
        
        # Create mock data
        stock_data = self.create_mock_data(symbols, days=90)
        
        # Run backtest
        results = backtester.run(stock_data)
        
        # Check results structure
        self.assertIsNotNone(results)
        self.assertIn('initial_value', results)
        self.assertIn('final_value', results)
        self.assertIn('total_return', results)
        self.assertIn('total_return_pct', results)
        self.assertIn('max_drawdown', results)
        self.assertIn('total_trades', results)
        self.assertIn('buy_trades', results)
        self.assertIn('sell_trades', results)
        self.assertIn('portfolio_history', results)
        self.assertIn('trade_log', results)
        
        # Check that initial value is correct
        self.assertEqual(results['initial_value'], 10000.0)
        
        # Check that we have some history
        self.assertGreater(len(results['portfolio_history']), 0)
    
    def test_backtest_with_insufficient_data(self):
        """Test backtest with insufficient data"""
        symbols = ['STOCK_A']
        backtester = Backtester(symbols, weeks=12, initial_cash=10000.0)
        
        # Create very limited data
        dates = pd.date_range(end=pd.Timestamp.now(), periods=5, freq='D')
        stock_data = {'STOCK_A': pd.Series([100, 101, 102, 103, 104], index=dates)}
        
        # Run backtest - should return None due to insufficient data
        results = backtester.run(stock_data)
        self.assertIsNone(results)


if __name__ == '__main__':
    unittest.main()
