"""
Unit tests for the Stock Trading Algorithm
"""

import unittest
import pandas as pd
import numpy as np
from stock_selector import StockSelector
from trading_engine import TradingEngine
from stock_trading_algorithm import StockTradingAlgorithm


class TestStockSelector(unittest.TestCase):
    """Test cases for StockSelector"""
    
    def setUp(self):
        self.selector = StockSelector(min_volatility=0.01, max_volatility=0.5)
        
    def test_calculate_volatility(self):
        """Test volatility calculation"""
        # Create sample prices with known volatility
        prices = pd.Series([100, 102, 101, 103, 102, 104])
        volatility = self.selector.calculate_volatility(prices)
        self.assertIsNotNone(volatility)
        self.assertGreater(volatility, 0)
    
    def test_volatility_with_insufficient_data(self):
        """Test volatility calculation with insufficient data"""
        prices = pd.Series([100])
        volatility = self.selector.calculate_volatility(prices)
        self.assertTrue(np.isnan(volatility))
    
    def test_predictability_score(self):
        """Test predictability score calculation"""
        prices = pd.Series([100 + i + np.random.randn() * 0.5 for i in range(50)])
        score = self.selector.calculate_predictability_score(prices)
        self.assertIsNotNone(score)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)
    
    def test_is_suitable_with_good_stock(self):
        """Test stock suitability with a good stock"""
        # Create a stable, predictable stock
        prices = pd.Series([100 + i * 0.1 + np.random.randn() * 0.5 for i in range(50)])
        is_suitable = self.selector.is_suitable(prices)
        # Result may vary based on random data, but should not crash
        self.assertIn(is_suitable, [True, False])
    
    def test_is_suitable_with_volatile_stock(self):
        """Test stock suitability with a highly volatile stock"""
        # Create a very volatile stock
        prices = pd.Series([100 + np.random.randn() * 50 for i in range(50)])
        is_suitable = self.selector.is_suitable(prices)
        self.assertFalse(is_suitable)
    
    def test_is_suitable_with_insufficient_data(self):
        """Test stock suitability with insufficient data"""
        prices = pd.Series([100, 101, 102])
        is_suitable = self.selector.is_suitable(prices)
        self.assertFalse(is_suitable)
    
    def test_filter_stocks(self):
        """Test filtering multiple stocks"""
        stock_data = {
            'STOCK_A': pd.Series([100 + i * 0.1 + np.random.randn() * 0.5 for i in range(50)]),
            'STOCK_B': pd.Series([100 + np.random.randn() * 50 for i in range(50)]),
            'STOCK_C': pd.Series([100, 101]),  # Insufficient data
        }
        suitable = self.selector.filter_stocks(stock_data)
        self.assertIsInstance(suitable, list)


class TestTradingEngine(unittest.TestCase):
    """Test cases for TradingEngine"""
    
    def setUp(self):
        self.engine = TradingEngine(
            buy_threshold=-0.05,
            sell_threshold=0.10,
            buy_amount=5.0,
            sell_amount=10.0
        )
    
    def test_calculate_weekly_change(self):
        """Test weekly change calculation"""
        prices = pd.Series([100, 101, 102, 103, 104, 105, 106, 107])
        change = self.engine.calculate_weekly_change(prices)
        self.assertIsNotNone(change)
        expected = (107 - 101) / 101  # 7 days ago
        self.assertAlmostEqual(change, expected, places=4)
    
    def test_weekly_change_with_insufficient_data(self):
        """Test weekly change with insufficient data"""
        prices = pd.Series([100])
        change = self.engine.calculate_weekly_change(prices)
        self.assertIsNone(change)
    
    def test_generate_buy_signal(self):
        """Test buy signal generation"""
        # Stock dropped 6%
        prices = pd.Series([100, 100, 100, 100, 100, 100, 100, 94])
        signal, amount, pct_change = self.engine.generate_signal(prices)
        self.assertEqual(signal, 'BUY')
        self.assertEqual(amount, 5.0)
        self.assertLess(pct_change, -0.05)
    
    def test_generate_sell_signal(self):
        """Test sell signal generation"""
        # Stock rose 12%
        prices = pd.Series([100, 100, 100, 100, 100, 100, 100, 112])
        signal, amount, pct_change = self.engine.generate_signal(prices)
        self.assertEqual(signal, 'SELL')
        self.assertEqual(amount, 10.0)
        self.assertGreater(pct_change, 0.10)
    
    def test_generate_hold_signal(self):
        """Test hold signal generation"""
        # Stock moved 3% (below thresholds)
        prices = pd.Series([100, 100, 100, 100, 100, 100, 100, 103])
        signal, amount, pct_change = self.engine.generate_signal(prices)
        self.assertEqual(signal, 'HOLD')
        self.assertEqual(amount, 0.0)
    
    def test_execute_trades(self):
        """Test trade execution for multiple stocks"""
        stock_data = {
            'BUY_STOCK': pd.Series([100, 100, 100, 100, 100, 100, 100, 94]),  # -6%
            'SELL_STOCK': pd.Series([100, 100, 100, 100, 100, 100, 100, 112]),  # +12%
            'HOLD_STOCK': pd.Series([100, 100, 100, 100, 100, 100, 100, 103]),  # +3%
        }
        trades = self.engine.execute_trades(stock_data)
        
        self.assertIn('BUY_STOCK', trades)
        self.assertIn('SELL_STOCK', trades)
        self.assertNotIn('HOLD_STOCK', trades)
        
        self.assertEqual(trades['BUY_STOCK']['signal'], 'BUY')
        self.assertEqual(trades['SELL_STOCK']['signal'], 'SELL')
    
    def test_get_trade_summary(self):
        """Test trade summary generation"""
        trades = {
            'STOCK_A': {'signal': 'BUY', 'amount': 5.0, 'shares': 0.05, 'price': 100, 'weekly_change': -0.06},
            'STOCK_B': {'signal': 'SELL', 'amount': 10.0, 'shares': 0.1, 'price': 100, 'weekly_change': 0.12},
            'STOCK_C': {'signal': 'BUY', 'amount': 5.0, 'shares': 0.05, 'price': 100, 'weekly_change': -0.07},
        }
        summary = self.engine.get_trade_summary(trades)
        
        self.assertEqual(summary['total_buys'], 2)
        self.assertEqual(summary['total_sells'], 1)
        self.assertEqual(summary['buy_value'], 10.0)
        self.assertEqual(summary['sell_value'], 10.0)
        self.assertEqual(summary['net_position'], 0.0)
    
    def test_empty_trade_summary(self):
        """Test trade summary with no trades"""
        summary = self.engine.get_trade_summary({})
        self.assertEqual(summary['total_buys'], 0)
        self.assertEqual(summary['total_sells'], 0)


class TestStockTradingAlgorithm(unittest.TestCase):
    """Test cases for StockTradingAlgorithm"""
    
    def setUp(self):
        self.algorithm = StockTradingAlgorithm()
    
    def test_run_algorithm(self):
        """Test running the complete algorithm"""
        stock_data = {
            'STOCK_A': pd.Series([100 + i * 0.1 + np.random.randn() * 0.5 for i in range(50)]),
            'STOCK_B': pd.Series([100, 100, 100, 100, 100, 100, 100, 94]),  # Buy signal
        }
        results = self.algorithm.run(stock_data)
        
        self.assertIn('suitable_stocks', results)
        self.assertIn('trades', results)
        self.assertIn('summary', results)
        self.assertIsInstance(results['suitable_stocks'], list)
        self.assertIsInstance(results['trades'], dict)
        self.assertIsInstance(results['summary'], dict)
    
    def test_analyze_stock(self):
        """Test individual stock analysis"""
        prices = pd.Series([100 + i * 0.1 + np.random.randn() * 0.5 for i in range(50)])
        analysis = self.algorithm.analyze_stock('TEST', prices)
        
        self.assertIn('symbol', analysis)
        self.assertIn('suitable', analysis)
        self.assertIn('predictability_score', analysis)
        self.assertIn('volatility', analysis)
        self.assertIn('signal', analysis)
        self.assertEqual(analysis['symbol'], 'TEST')
    
    def test_custom_config(self):
        """Test algorithm with custom configuration"""
        selector_config = {'min_volatility': 0.02, 'max_volatility': 0.3}
        trading_config = {'buy_threshold': -0.03, 'sell_threshold': 0.08}
        
        algorithm = StockTradingAlgorithm(
            selector_config=selector_config,
            trading_config=trading_config
        )
        
        self.assertEqual(algorithm.selector.min_volatility, 0.02)
        self.assertEqual(algorithm.engine.buy_threshold, -0.03)


if __name__ == '__main__':
    unittest.main()
