#!/usr/bin/env python
"""
Demo script for backtesting with sample data (no internet required).
This demonstrates the backtesting functionality with generated sample data.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from backtest import Backtester, visualize_results, print_header, print_section


def create_realistic_stock_data(symbols, weeks=52):
    """
    Create realistic-looking stock data for demonstration
    
    Args:
        symbols (list): Stock symbols to generate data for
        weeks (int): Number of weeks of data to generate
        
    Returns:
        dict: Stock data for each symbol
    """
    print(f"Generating {weeks} weeks of sample stock data...")
    
    days = weeks * 7
    dates = pd.date_range(end=pd.Timestamp.now(), periods=days, freq='D')
    
    stock_data = {}
    
    for i, symbol in enumerate(symbols):
        # Each stock starts at a different base price
        base_price = 50 + i * 30
        
        # Create realistic price movements
        # 1. Overall trend (some up, some down, some sideways)
        if i % 3 == 0:
            trend = np.linspace(0, 20, days)  # Upward trend
        elif i % 3 == 1:
            trend = np.linspace(0, -10, days)  # Downward trend
        else:
            trend = np.zeros(days)  # Sideways
        
        # 2. Random walk component
        random_walk = np.cumsum(np.random.randn(days) * 0.5)
        
        # 3. Weekly volatility
        volatility = np.random.randn(days) * 2
        
        # Combine components
        prices = base_price + trend + random_walk + volatility
        
        # Ensure no negative prices
        prices = np.maximum(prices, 10)
        
        # Add some deliberate buy signals (5%+ drops over a week)
        # Add 3-5 buy signals throughout the period
        num_buy_signals = np.random.randint(3, 6)
        for j in range(num_buy_signals):
            start_idx = np.random.randint(7, days - 7)
            drop_pct = 0.06 + np.random.rand() * 0.04  # 6-10% drop
            prices[start_idx:start_idx+7] = prices[start_idx] * np.linspace(1.0, 1.0 - drop_pct, 7)
        
        # Add some deliberate sell signals (10%+ rises over a week)
        # Add 2-4 sell signals throughout the period
        num_sell_signals = np.random.randint(2, 5)
        for j in range(num_sell_signals):
            start_idx = np.random.randint(7, days - 7)
            rise_pct = 0.11 + np.random.rand() * 0.05  # 11-16% rise
            prices[start_idx:start_idx+7] = prices[start_idx] * np.linspace(1.0, 1.0 + rise_pct, 7)
        
        stock_data[symbol] = pd.Series(prices, index=dates)
    
    print(f"✓ Generated data for {len(stock_data)} stocks")
    
    return stock_data


def main():
    """Run backtest demo with sample data"""
    
    print_header("Stock Trading Algorithm - Backtest Demo (Sample Data)")
    
    # Configuration
    symbols = ['STOCK_A', 'STOCK_B', 'STOCK_C', 'STOCK_D', 'STOCK_E']
    weeks = 52
    initial_cash = 10000.0
    
    print(f"\nConfiguration:")
    print(f"  Symbols: {', '.join(symbols)}")
    print(f"  Weeks: {weeks}")
    print(f"  Initial Cash: ${initial_cash:,.2f}")
    print(f"  Data: Sample/Generated (no internet required)")
    
    # Generate sample data
    print_section("Generating Sample Data")
    stock_data = create_realistic_stock_data(symbols, weeks=weeks)
    
    # Show data summary
    print("\nData Summary:")
    for symbol, prices in stock_data.items():
        print(f"  {symbol}:")
        print(f"    Data points: {len(prices)}")
        print(f"    Start price: ${prices.iloc[0]:.2f}")
        print(f"    End price: ${prices.iloc[-1]:.2f}")
        print(f"    Change: {((prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0] * 100):+.2f}%")
        print(f"    Range: ${prices.min():.2f} - ${prices.max():.2f}")
    
    # Initialize backtester
    print_section("Running Backtest Simulation")
    backtester = Backtester(symbols, weeks=weeks, initial_cash=initial_cash)
    
    # Run backtest
    results = backtester.run(stock_data)
    
    if results is None:
        print("❌ Backtest failed!")
        return 1
    
    # Display results
    print_section("Backtest Results")
    
    print(f"\nInitial Portfolio Value: ${results['initial_value']:,.2f}")
    print(f"Final Portfolio Value:   ${results['final_value']:,.2f}")
    print(f"Total Return:            {results['total_return_pct']:+.2f}%")
    print(f"Max Drawdown:            {results['max_drawdown']*100:.2f}%")
    
    print(f"\nTotal Trades:  {results['total_trades']}")
    print(f"  Buy Trades:  {results['buy_trades']}")
    print(f"  Sell Trades: {results['sell_trades']}")
    
    if results['final_holdings']:
        print(f"\nFinal Holdings:")
        for symbol, shares in sorted(results['final_holdings'].items()):
            current_price = stock_data[symbol].iloc[-1]
            value = shares * current_price
            print(f"  {symbol}: {shares:.4f} shares @ ${current_price:.2f} = ${value:.2f}")
    else:
        print(f"\nFinal Holdings: None (all cash)")
    
    # Show all trades
    if results['trade_log']:
        print_section(f"Trade History ({len(results['trade_log'])} trades)")
        
        # Group by action
        buy_trades = [t for t in results['trade_log'] if t['action'] == 'BUY']
        sell_trades = [t for t in results['trade_log'] if t['action'] == 'SELL']
        
        if buy_trades:
            print(f"\nBUY Trades ({len(buy_trades)}):")
            for trade in buy_trades[:10]:  # Show first 10
                print(f"  {trade['date'].strftime('%Y-%m-%d')}: "
                      f"BUY {trade['shares']:.4f} {trade['symbol']:8s} @ "
                      f"${trade['price']:.2f} (${trade['amount']:.2f}) "
                      f"[{trade['weekly_change']*100:+.2f}%]")
            if len(buy_trades) > 10:
                print(f"  ... and {len(buy_trades) - 10} more")
        
        if sell_trades:
            print(f"\nSELL Trades ({len(sell_trades)}):")
            for trade in sell_trades[:10]:  # Show first 10
                print(f"  {trade['date'].strftime('%Y-%m-%d')}: "
                      f"SELL {trade['shares']:.4f} {trade['symbol']:8s} @ "
                      f"${trade['price']:.2f} (${trade['amount']:.2f}) "
                      f"[{trade['weekly_change']*100:+.2f}%]")
            if len(sell_trades) > 10:
                print(f"  ... and {len(sell_trades) - 10} more")
    
    # Portfolio value over time
    print_section("Portfolio Growth")
    
    # Show portfolio value at key intervals
    history = results['portfolio_history']
    intervals = [0, len(history)//4, len(history)//2, 3*len(history)//4, -1]
    
    print("\nPortfolio Value Over Time:")
    for i in intervals:
        state = history[i]
        pct_change = ((state['total_value'] - results['initial_value']) / 
                     results['initial_value'] * 100)
        print(f"  {state['date'].strftime('%Y-%m-%d')}: "
              f"${state['total_value']:,.2f} ({pct_change:+.2f}%) "
              f"[Cash: ${state['cash']:.2f}, Holdings: ${state['holdings_value']:.2f}]")
    
    # Visualize results
    print_section("Generating Visualization")
    try:
        visualize_results(results, symbols)
        print("\n✓ Visualization complete! Check 'backtest_results.png'")
    except Exception as e:
        print(f"⚠ Warning: Could not create visualization: {e}")
        print("  You can still view the numeric results above.")
    
    print("\n" + "=" * 70)
    print("Demo Complete!")
    print("=" * 70)
    print("\nTo run backtest with live data, use:")
    print("  python backtest.py --universe small --weeks 12")
    print("\n")
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
