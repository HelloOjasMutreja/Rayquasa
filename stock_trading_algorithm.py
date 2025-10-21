"""
Main Stock Trading Algorithm
Combines stock selection and trading logic.
"""

from stock_selector import StockSelector
from trading_engine import TradingEngine
import pandas as pd


class StockTradingAlgorithm:
    """
    Main algorithm that orchestrates stock selection and trading execution.
    """
    
    def __init__(self, selector_config=None, trading_config=None):
        """
        Initialize the stock trading algorithm.
        
        Args:
            selector_config (dict): Configuration for StockSelector
            trading_config (dict): Configuration for TradingEngine
        """
        # Initialize stock selector with default or custom config
        if selector_config is None:
            self.selector = StockSelector()
        else:
            self.selector = StockSelector(**selector_config)
        
        # Initialize trading engine with default or custom config
        if trading_config is None:
            self.engine = TradingEngine()
        else:
            self.engine = TradingEngine(**trading_config)
    
    def run(self, stock_data):
        """
        Run the complete trading algorithm:
        1. Filter stocks to create trading universe
        2. Execute trades for suitable stocks
        
        Args:
            stock_data (dict): Dictionary with stock symbols as keys and price series as values
            
        Returns:
            dict: Contains 'suitable_stocks', 'trades', and 'summary'
        """
        # Step 1: Filter stocks to create trading universe
        suitable_stocks = self.selector.filter_stocks(stock_data)
        
        # Step 2: Create filtered stock data for suitable stocks only
        filtered_stock_data = {
            symbol: stock_data[symbol] 
            for symbol in suitable_stocks 
            if symbol in stock_data
        }
        
        # Step 3: Execute trades for suitable stocks
        trades = self.engine.execute_trades(filtered_stock_data)
        
        # Step 4: Generate summary
        summary = self.engine.get_trade_summary(trades)
        
        return {
            'suitable_stocks': suitable_stocks,
            'trades': trades,
            'summary': summary
        }
    
    def analyze_stock(self, symbol, prices):
        """
        Analyze a single stock for suitability and trading signals.
        
        Args:
            symbol (str): Stock symbol
            prices (pd.Series): Historical prices
            
        Returns:
            dict: Analysis results
        """
        is_suitable = self.selector.is_suitable(prices)
        predictability = self.selector.calculate_predictability_score(prices)
        volatility = self.selector.calculate_volatility(prices)
        
        signal, amount, pct_change = self.engine.generate_signal(prices)
        
        return {
            'symbol': symbol,
            'suitable': is_suitable,
            'predictability_score': predictability,
            'volatility': volatility,
            'signal': signal,
            'amount': amount,
            'weekly_change': pct_change
        }


def load_stock_data_from_csv(file_path):
    """
    Helper function to load stock data from a CSV file.
    Expected format: Date, Symbol, Close
    
    Args:
        file_path (str): Path to CSV file
        
    Returns:
        dict: Dictionary with stock symbols as keys and price series as values
    """
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    
    stock_data = {}
    for symbol in df['Symbol'].unique():
        symbol_data = df[df['Symbol'] == symbol].set_index('Date')
        stock_data[symbol] = symbol_data['Close']
    
    return stock_data


def fetch_live_data(symbols, period='1mo'):
    """
    Fetch live stock data using yfinance.
    
    Args:
        symbols (list): List of stock symbols
        period (str): Time period (e.g., '1mo', '3mo', '1y')
        
    Returns:
        dict: Dictionary with stock symbols as keys and price series as values
    """
    try:
        import yfinance as yf
    except ImportError:
        raise ImportError("yfinance is required for fetching live data. Install with: pip install yfinance")
    
    stock_data = {}
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            if not hist.empty:
                stock_data[symbol] = hist['Close']
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
    
    return stock_data
