"""
Example usage of the Stock Trading Algorithm
"""

from stock_trading_algorithm import StockTradingAlgorithm, fetch_live_data
import pandas as pd
import numpy as np


def create_sample_data():
    """
    Create sample stock data for demonstration.
    Returns stock data with various scenarios.
    """
    # Create date range for last 30 days
    dates = pd.date_range(end=pd.Timestamp.now(), periods=30, freq='D')
    
    stock_data = {}
    
    # Stock 1: Dropped 6% in last week (should trigger BUY)
    prices1 = 100 + np.random.randn(30) * 2
    prices1[-7:] = prices1[-7] * np.linspace(1.0, 0.94, 7)  # 6% drop
    stock_data['STOCK_A'] = pd.Series(prices1, index=dates)
    
    # Stock 2: Rose 12% in last week (should trigger SELL)
    prices2 = 50 + np.random.randn(30) * 1.5
    prices2[-7:] = prices2[-7] * np.linspace(1.0, 1.12, 7)  # 12% rise
    stock_data['STOCK_B'] = pd.Series(prices2, index=dates)
    
    # Stock 3: Stable, no signal
    prices3 = 75 + np.random.randn(30) * 1
    stock_data['STOCK_C'] = pd.Series(prices3, index=dates)
    
    # Stock 4: Too volatile (should be filtered out)
    prices4 = 200 + np.random.randn(30) * 50
    stock_data['STOCK_D'] = pd.Series(prices4, index=dates)
    
    # Stock 5: Another buy signal
    prices5 = 30 + np.random.randn(30) * 0.8
    prices5[-7:] = prices5[-7] * np.linspace(1.0, 0.93, 7)  # 7% drop
    stock_data['STOCK_E'] = pd.Series(prices5, index=dates)
    
    return stock_data


def example_with_sample_data():
    """
    Run the algorithm with sample data.
    """
    print("=" * 60)
    print("Stock Trading Algorithm - Example with Sample Data")
    print("=" * 60)
    print()
    
    # Create sample data
    stock_data = create_sample_data()
    
    print(f"Total stocks in initial universe: {len(stock_data)}")
    print(f"Stock symbols: {list(stock_data.keys())}")
    print()
    
    # Initialize algorithm
    algorithm = StockTradingAlgorithm()
    
    # Run the algorithm
    results = algorithm.run(stock_data)
    
    # Display results
    print("-" * 60)
    print("SUITABLE STOCKS (Trading Universe)")
    print("-" * 60)
    print(f"Number of suitable stocks: {len(results['suitable_stocks'])}")
    print(f"Stocks: {results['suitable_stocks']}")
    print()
    
    print("-" * 60)
    print("TRADE SIGNALS")
    print("-" * 60)
    if results['trades']:
        for symbol, trade in results['trades'].items():
            print(f"\n{symbol}:")
            print(f"  Signal: {trade['signal']}")
            print(f"  Amount: ${trade['amount']:.2f}")
            print(f"  Shares: {trade['shares']:.4f}")
            print(f"  Current Price: ${trade['price']:.2f}")
            print(f"  Weekly Change: {trade['weekly_change']*100:.2f}%")
    else:
        print("No trades to execute")
    print()
    
    print("-" * 60)
    print("SUMMARY")
    print("-" * 60)
    summary = results['summary']
    print(f"Total Buy Orders: {summary['total_buys']}")
    print(f"Total Sell Orders: {summary['total_sells']}")
    print(f"Total Buy Value: ${summary['buy_value']:.2f}")
    print(f"Total Sell Value: ${summary['sell_value']:.2f}")
    print(f"Net Position: ${summary['net_position']:.2f}")
    print()
    
    # Analyze individual stocks
    print("-" * 60)
    print("INDIVIDUAL STOCK ANALYSIS")
    print("-" * 60)
    for symbol, prices in stock_data.items():
        analysis = algorithm.analyze_stock(symbol, prices)
        print(f"\n{symbol}:")
        print(f"  Suitable: {analysis['suitable']}")
        print(f"  Predictability Score: {analysis['predictability_score']:.3f}")
        print(f"  Volatility: {analysis['volatility']:.3f}")
        print(f"  Signal: {analysis['signal']}")
        if analysis['weekly_change'] is not None:
            print(f"  Weekly Change: {analysis['weekly_change']*100:.2f}%")
    print()


def example_with_live_data():
    """
    Run the algorithm with live data from Yahoo Finance.
    """
    print("=" * 60)
    print("Stock Trading Algorithm - Example with Live Data")
    print("=" * 60)
    print()
    
    # Define a list of stock symbols
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM']
    
    print(f"Fetching data for: {symbols}")
    print("This may take a moment...")
    print()
    
    try:
        # Fetch live data
        stock_data = fetch_live_data(symbols, period='1mo')
        
        if not stock_data:
            print("Failed to fetch stock data. Please check your internet connection.")
            return
        
        print(f"Successfully fetched data for {len(stock_data)} stocks")
        print()
        
        # Initialize algorithm
        algorithm = StockTradingAlgorithm()
        
        # Run the algorithm
        results = algorithm.run(stock_data)
        
        # Display results
        print("-" * 60)
        print("SUITABLE STOCKS (Trading Universe)")
        print("-" * 60)
        print(f"Number of suitable stocks: {len(results['suitable_stocks'])}")
        print(f"Stocks: {results['suitable_stocks']}")
        print()
        
        print("-" * 60)
        print("TRADE SIGNALS")
        print("-" * 60)
        if results['trades']:
            for symbol, trade in results['trades'].items():
                print(f"\n{symbol}:")
                print(f"  Signal: {trade['signal']}")
                print(f"  Amount: ${trade['amount']:.2f}")
                print(f"  Shares: {trade['shares']:.4f}")
                print(f"  Current Price: ${trade['price']:.2f}")
                print(f"  Weekly Change: {trade['weekly_change']*100:.2f}%")
        else:
            print("No trades to execute at this time")
        print()
        
        print("-" * 60)
        print("SUMMARY")
        print("-" * 60)
        summary = results['summary']
        print(f"Total Buy Orders: {summary['total_buys']}")
        print(f"Total Sell Orders: {summary['total_sells']}")
        print(f"Total Buy Value: ${summary['buy_value']:.2f}")
        print(f"Total Sell Value: ${summary['sell_value']:.2f}")
        print(f"Net Position: ${summary['net_position']:.2f}")
        print()
        
    except ImportError:
        print("yfinance not installed. Install with: pip install yfinance")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--live':
        # Run with live data
        example_with_live_data()
    else:
        # Run example with sample data
        example_with_sample_data()
        
        print("\n" + "=" * 60)
        print("TIP: To test with live market data, run:")
        print("  python example_usage.py --live")
        print("  OR use: python test_with_live_data.py")
        print("=" * 60)
        print()
