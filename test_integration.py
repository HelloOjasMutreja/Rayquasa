"""
Integration tests for test_with_live_data.py

These tests verify the functionality of the live data testing script
without requiring actual network access.
"""

import unittest
import sys
import io
from contextlib import redirect_stdout, redirect_stderr
from test_with_live_data import STOCK_UNIVERSES, print_header, print_section


class TestStockUniverses(unittest.TestCase):
    """Test predefined stock universes"""
    
    def test_all_universes_exist(self):
        """Test that all expected universes are defined"""
        expected_universes = ['default', 'tech', 'finance', 'energy', 'healthcare', 'consumer', 'small']
        for universe in expected_universes:
            self.assertIn(universe, STOCK_UNIVERSES)
    
    def test_universes_have_valid_symbols(self):
        """Test that all universes contain valid stock symbols"""
        for name, symbols in STOCK_UNIVERSES.items():
            self.assertIsInstance(symbols, list)
            self.assertGreater(len(symbols), 0)
            
            # Check all symbols are strings and uppercase
            for symbol in symbols:
                self.assertIsInstance(symbol, str)
                self.assertEqual(symbol, symbol.upper())
                self.assertGreater(len(symbol), 0)
    
    def test_default_universe(self):
        """Test default universe contains expected stocks"""
        default = STOCK_UNIVERSES['default']
        self.assertEqual(len(default), 8)
        # Check some expected stocks
        for symbol in ['AAPL', 'MSFT', 'GOOGL', 'AMZN']:
            self.assertIn(symbol, default)
    
    def test_small_universe(self):
        """Test small universe for quick testing"""
        small = STOCK_UNIVERSES['small']
        self.assertEqual(len(small), 3)
        self.assertIn('AAPL', small)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions"""
    
    def test_print_header(self):
        """Test header formatting"""
        output = io.StringIO()
        with redirect_stdout(output):
            print_header("Test Header")
        
        result = output.getvalue()
        self.assertIn("Test Header", result)
        self.assertIn("=", result)
    
    def test_print_section(self):
        """Test section formatting"""
        output = io.StringIO()
        with redirect_stdout(output):
            print_section("Test Section")
        
        result = output.getvalue()
        self.assertIn("Test Section", result)
        self.assertIn("-", result)


class TestScriptIntegration(unittest.TestCase):
    """Integration tests for the complete script"""
    
    def test_import_script(self):
        """Test that the script can be imported without errors"""
        try:
            import test_with_live_data
            self.assertTrue(hasattr(test_with_live_data, 'run_algorithm_with_live_data'))
            self.assertTrue(hasattr(test_with_live_data, 'main'))
        except ImportError as e:
            self.fail(f"Failed to import test_with_live_data: {e}")
    
    def test_all_sectors_covered(self):
        """Test that multiple market sectors are represented"""
        sectors = ['tech', 'finance', 'energy', 'healthcare', 'consumer']
        for sector in sectors:
            self.assertIn(sector, STOCK_UNIVERSES)
            self.assertGreater(len(STOCK_UNIVERSES[sector]), 5)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
