#!/usr/bin/env python
"""
Test script for running the Stock Trading Algorithm with live market data from Yahoo Finance.
This script allows users to test the algorithm on their own devices with real market data.

Usage:
    python test_with_live_data.py                    # Test with default stocks
    python test_with_live_data.py --tech              # Test with tech stocks
    python test_with_live_data.py --custom AAPL MSFT # Test with custom stocks
"""

import argparse
import sys
from stock_trading_algorithm import StockTradingAlgorithm, fetch_live_data


# Predefined stock universes for easy testing
STOCK_UNIVERSES = {
    'default': ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM'],
    'tech': ['AAPL', 'GOOGL', 'MSFT', 'META', 'NVDA', 'AMD', 'INTC', 'CSCO', 'ORCL', 'IBM'],
    'finance': ['JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'USB', 'PNC', 'TFC', 'COF'],
    'energy': ['XOM', 'CVX', 'COP', 'SLB', 'EOG', 'MPC', 'PSX', 'VLO', 'OXY', 'HAL'],
    'healthcare': ['JNJ', 'UNH', 'PFE', 'MRK', 'ABBV', 'TMO', 'DHR', 'ABT', 'LLY', 'BMY'],
    'consumer': ['AMZN', 'WMT', 'HD', 'MCD', 'NKE', 'SBUX', 'TGT', 'LOW', 'TJX', 'COST'],
    'small': ['AAPL', 'MSFT', 'GOOGL'],  # Small test set
}


def print_header(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70)


def print_section(title):
    """Print a formatted subsection header"""
    print("\n" + "-" * 70)
    print(title)
    print("-" * 70)


def run_algorithm_with_live_data(symbols, period='1mo', custom_config=None):
    """
    Run the trading algorithm with live data from Yahoo Finance.
    
    Args:
        symbols (list): List of stock symbols to analyze
        period (str): Time period for historical data ('1mo', '3mo', '6mo', '1y')
        custom_config (dict): Optional custom configuration for the algorithm
        
    Returns:
        dict: Results from the algorithm
    """
    print_header("Stock Trading Algorithm - Live Market Data Test")
    
    print(f"\nConfiguration:")
    print(f"  Stock Symbols: {', '.join(symbols)}")
    print(f"  Time Period: {period}")
    print(f"  Number of Stocks: {len(symbols)}")
    
    # Fetch live data
    print_section("Fetching Live Data from Yahoo Finance")
    print("Please wait, downloading market data...")
    
    try:
        stock_data = fetch_live_data(symbols, period=period)
        
        if not stock_data:
            print("\n❌ ERROR: Failed to fetch any stock data!")
            print("   This could be due to:")
            print("   - Network connectivity issues")
            print("   - Invalid stock symbols")
            print("   - Yahoo Finance API issues")
            print("\nPlease check your internet connection and try again.")
            return None
        
        print(f"\n✓ Successfully fetched data for {len(stock_data)}/{len(symbols)} stocks")
        
        # Show failed symbols if any
        failed_symbols = set(symbols) - set(stock_data.keys())
        if failed_symbols:
            print(f"\n⚠ Warning: Failed to fetch data for: {', '.join(failed_symbols)}")
        
        # Display data summary
        print_section("Data Summary")
        for symbol, prices in stock_data.items():
            print(f"{symbol}:")
            print(f"  Data points: {len(prices)}")
            print(f"  Date range: {prices.index[0].strftime('%Y-%m-%d')} to {prices.index[-1].strftime('%Y-%m-%d')}")
            print(f"  Latest price: ${prices.iloc[-1]:.2f}")
            print(f"  Price range: ${prices.min():.2f} - ${prices.max():.2f}")
        
        # Initialize and run algorithm
        print_section("Running Trading Algorithm")
        
        if custom_config:
            algorithm = StockTradingAlgorithm(**custom_config)
            print("Using custom configuration")
        else:
            algorithm = StockTradingAlgorithm()
            print("Using default configuration:")
            print(f"  Buy threshold: {algorithm.engine.buy_threshold*100:.1f}% drop")
            print(f"  Sell threshold: {algorithm.engine.sell_threshold*100:.1f}% rise")
            print(f"  Buy amount: ${algorithm.engine.buy_amount:.2f}")
            print(f"  Sell amount: ${algorithm.engine.sell_amount:.2f}")
        
        results = algorithm.run(stock_data)
        
        # Display results
        print_section("Trading Universe (Suitable Stocks)")
        print(f"✓ {len(results['suitable_stocks'])}/{len(stock_data)} stocks passed filters")
        
        if results['suitable_stocks']:
            print(f"\nSuitable stocks: {', '.join(results['suitable_stocks'])}")
        else:
            print("\n⚠ No stocks passed the suitability filters")
            print("   Try adjusting the selector configuration or using a different stock universe")
        
        # Display trades
        print_section("Trade Signals")
        
        if results['trades']:
            print(f"\n✓ {len(results['trades'])} trade signal(s) generated:\n")
            
            for symbol, trade in results['trades'].items():
                signal_emoji = "🔴" if trade['signal'] == 'BUY' else "🟢"
                print(f"{signal_emoji} {symbol}:")
                print(f"   Action: {trade['signal']}")
                print(f"   Amount: ${trade['amount']:.2f}")
                print(f"   Shares: {trade['shares']:.4f}")
                print(f"   Price: ${trade['price']:.2f}")
                print(f"   Weekly Change: {trade['weekly_change']*100:+.2f}%")
                print()
        else:
            print("\n⚠ No trade signals generated")
            print("   Market conditions don't meet buy/sell thresholds")
        
        # Display summary
        print_section("Trading Summary")
        summary = results['summary']
        print(f"Total Buy Orders: {summary['total_buys']}")
        print(f"Total Sell Orders: {summary['total_sells']}")
        print(f"Buy Value: ${summary['buy_value']:.2f}")
        print(f"Sell Value: ${summary['sell_value']:.2f}")
        print(f"Net Position: ${summary['net_position']:.2f}")
        
        # Display detailed analysis
        print_section("Detailed Stock Analysis")
        
        for symbol, prices in stock_data.items():
            analysis = algorithm.analyze_stock(symbol, prices)
            status_emoji = "✓" if analysis['suitable'] else "✗"
            
            print(f"\n{status_emoji} {symbol}:")
            print(f"   Suitable: {analysis['suitable']}")
            print(f"   Predictability Score: {analysis['predictability_score']:.3f}")
            print(f"   Volatility: {analysis['volatility']:.3f}")
            print(f"   Signal: {analysis['signal']}")
            if analysis['weekly_change'] is not None:
                print(f"   Weekly Change: {analysis['weekly_change']*100:+.2f}%")
        
        print("\n" + "=" * 70)
        print("Test Complete!")
        print("=" * 70 + "\n")
        
        return results
        
    except ImportError as e:
        print(f"\n❌ ERROR: Missing required package - {e}")
        print("Please install required packages: pip install -r requirements.txt")
        return None
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main entry point for the test script"""
    parser = argparse.ArgumentParser(
        description='Test the Stock Trading Algorithm with live market data from Yahoo Finance',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_with_live_data.py                         # Default stock universe
  python test_with_live_data.py --universe tech         # Tech stocks
  python test_with_live_data.py --universe finance      # Finance stocks
  python test_with_live_data.py --period 3mo            # 3 months of data
  python test_with_live_data.py --custom AAPL MSFT TSLA # Custom stocks
  python test_with_live_data.py --list-universes        # List available universes
        """
    )
    
    parser.add_argument(
        '--universe', '-u',
        choices=list(STOCK_UNIVERSES.keys()),
        default='default',
        help='Predefined stock universe to test (default: default)'
    )
    
    parser.add_argument(
        '--custom', '-c',
        nargs='+',
        metavar='SYMBOL',
        help='Custom list of stock symbols to test'
    )
    
    parser.add_argument(
        '--period', '-p',
        default='1mo',
        choices=['1mo', '3mo', '6mo', '1y', '2y', '5y'],
        help='Time period for historical data (default: 1mo)'
    )
    
    parser.add_argument(
        '--list-universes', '-l',
        action='store_true',
        help='List all available predefined stock universes'
    )
    
    args = parser.parse_args()
    
    # Handle list universes
    if args.list_universes:
        print("\nAvailable Stock Universes:")
        print("-" * 50)
        for name, stocks in STOCK_UNIVERSES.items():
            print(f"\n{name}:")
            print(f"  Stocks: {', '.join(stocks)}")
            print(f"  Count: {len(stocks)}")
        print()
        return 0
    
    # Determine which symbols to use
    if args.custom:
        symbols = [s.upper() for s in args.custom]
        print(f"\nUsing custom stock symbols: {symbols}")
    else:
        symbols = STOCK_UNIVERSES[args.universe]
        print(f"\nUsing '{args.universe}' stock universe: {symbols}")
    
    # Run the algorithm
    results = run_algorithm_with_live_data(symbols, period=args.period)
    
    if results is None:
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
