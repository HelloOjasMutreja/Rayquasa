#!/usr/bin/env python
"""
Backtesting script for simulating the Stock Trading Algorithm on historical data.
Simulates trading over the past 52 weeks and visualizes the results.

Usage:
    python backtest.py                              # Backtest default stocks
    python backtest.py --universe tech              # Backtest tech stocks
    python backtest.py --custom AAPL MSFT GOOGL     # Backtest custom stocks
    python backtest.py --weeks 26                   # Backtest over 26 weeks
"""

import argparse
import sys
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from stock_trading_algorithm import StockTradingAlgorithm, fetch_live_data
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


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


class Portfolio:
    """Tracks portfolio holdings and cash over time"""
    
    def __init__(self, initial_cash=10000.0):
        """
        Initialize portfolio with cash
        
        Args:
            initial_cash (float): Starting cash amount
        """
        self.cash = initial_cash
        self.holdings = {}  # {symbol: shares}
        self.history = []  # List of portfolio states
        
    def buy(self, symbol, shares, price):
        """
        Buy shares of a stock
        
        Args:
            symbol (str): Stock symbol
            shares (float): Number of shares to buy
            price (float): Price per share
        """
        cost = shares * price
        if cost <= self.cash:
            self.cash -= cost
            self.holdings[symbol] = self.holdings.get(symbol, 0) + shares
            return True
        return False
    
    def sell(self, symbol, shares, price):
        """
        Sell shares of a stock
        
        Args:
            symbol (str): Stock symbol
            shares (float): Number of shares to sell
            price (float): Price per share
        """
        if symbol in self.holdings and self.holdings[symbol] >= shares:
            proceeds = shares * price
            self.cash += proceeds
            self.holdings[symbol] -= shares
            if self.holdings[symbol] < 1e-10:
                del self.holdings[symbol]
            return True
        return False
    
    def get_value(self, current_prices):
        """
        Calculate total portfolio value
        
        Args:
            current_prices (dict): Current prices for all stocks {symbol: price}
            
        Returns:
            float: Total portfolio value (cash + holdings)
        """
        holdings_value = sum(
            shares * current_prices.get(symbol, 0)
            for symbol, shares in self.holdings.items()
        )
        return self.cash + holdings_value
    
    def record_state(self, date, current_prices):
        """
        Record current portfolio state
        
        Args:
            date: Current date
            current_prices (dict): Current prices for all stocks
        """
        total_value = self.get_value(current_prices)
        holdings_value = total_value - self.cash
        
        self.history.append({
            'date': date,
            'cash': self.cash,
            'holdings_value': holdings_value,
            'total_value': total_value,
            'holdings': dict(self.holdings)  # Copy current holdings
        })


class Backtester:
    """Backtests the trading algorithm over historical data"""
    
    def __init__(self, symbols, weeks=52, initial_cash=10000.0):
        """
        Initialize backtester
        
        Args:
            symbols (list): Stock symbols to trade
            weeks (int): Number of weeks to backtest
            initial_cash (float): Starting portfolio cash
        """
        self.symbols = symbols
        self.weeks = weeks
        self.initial_cash = initial_cash
        self.portfolio = Portfolio(initial_cash)
        self.algorithm = StockTradingAlgorithm()
        self.trade_log = []
        
    def fetch_data(self):
        """
        Fetch historical data for backtesting
        
        Returns:
            dict: Stock data for each symbol
        """
        print(f"Fetching {self.weeks} weeks of historical data...")
        
        # Fetch data with some buffer to ensure we have enough
        period = f"{self.weeks + 8}w"
        
        try:
            stock_data = fetch_live_data(self.symbols, period=period)
            
            if not stock_data:
                print("❌ Failed to fetch stock data!")
                return None
            
            print(f"✓ Successfully fetched data for {len(stock_data)}/{len(self.symbols)} stocks")
            
            # Show failed symbols if any
            failed_symbols = set(self.symbols) - set(stock_data.keys())
            if failed_symbols:
                print(f"⚠ Warning: Failed to fetch data for: {', '.join(failed_symbols)}")
            
            return stock_data
            
        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            return None
    
    def run(self, stock_data):
        """
        Run backtest simulation
        
        Args:
            stock_data (dict): Historical stock data
            
        Returns:
            dict: Backtest results
        """
        if not stock_data:
            return None
        
        print(f"\nRunning backtest simulation over {self.weeks} weeks...")
        
        # Get the date range
        all_dates = sorted(set(
            date for prices in stock_data.values() 
            for date in prices.index
        ))
        
        if len(all_dates) < 14:
            print("❌ Insufficient data for backtesting (need at least 14 days)")
            return None
        
        # Initialize portfolio at start
        start_date = all_dates[0]
        current_prices = {
            symbol: prices.loc[start_date] if start_date in prices.index else None
            for symbol, prices in stock_data.items()
        }
        current_prices = {k: v for k, v in current_prices.items() if v is not None}
        self.portfolio.record_state(start_date, current_prices)
        
        # Simulate week by week (7 trading days)
        weeks_processed = 0
        i = 7  # Start from day 7 to have a week of history
        
        while i < len(all_dates) and weeks_processed < self.weeks:
            current_date = all_dates[i]
            
            # Get data up to current date for each stock
            window_data = {}
            for symbol, prices in stock_data.items():
                # Get prices up to current date
                mask = prices.index <= current_date
                if mask.sum() > 0:
                    window_data[symbol] = prices[mask]
            
            # Run algorithm on current window
            if window_data:
                results = self.algorithm.run(window_data)
                
                # Execute trades
                current_prices = {}
                for symbol, prices in window_data.items():
                    if len(prices) > 0:
                        current_prices[symbol] = prices.iloc[-1]
                
                # Process each trade
                for symbol, trade in results['trades'].items():
                    if symbol in current_prices:
                        price = current_prices[symbol]
                        
                        if trade['signal'] == 'BUY':
                            # Buy with specified dollar amount
                            shares = trade['amount'] / price
                            if self.portfolio.buy(symbol, shares, price):
                                self.trade_log.append({
                                    'date': current_date,
                                    'symbol': symbol,
                                    'action': 'BUY',
                                    'shares': shares,
                                    'price': price,
                                    'amount': trade['amount'],
                                    'weekly_change': trade['weekly_change']
                                })
                        
                        elif trade['signal'] == 'SELL':
                            # Sell with specified dollar amount
                            shares_to_sell = trade['amount'] / price
                            # Only sell if we have shares
                            if symbol in self.portfolio.holdings:
                                actual_shares = min(shares_to_sell, self.portfolio.holdings[symbol])
                                if self.portfolio.sell(symbol, actual_shares, price):
                                    self.trade_log.append({
                                        'date': current_date,
                                        'symbol': symbol,
                                        'action': 'SELL',
                                        'shares': actual_shares,
                                        'price': price,
                                        'amount': actual_shares * price,
                                        'weekly_change': trade['weekly_change']
                                    })
                
                # Record portfolio state
                self.portfolio.record_state(current_date, current_prices)
            
            # Move to next week
            i += 7
            weeks_processed += 1
            
            if weeks_processed % 10 == 0:
                print(f"  Processed {weeks_processed}/{self.weeks} weeks...")
        
        print(f"✓ Backtest complete! Processed {weeks_processed} weeks")
        
        # Calculate results
        return self._calculate_results()
    
    def _calculate_results(self):
        """Calculate backtest results"""
        if not self.portfolio.history:
            return None
        
        initial_value = self.portfolio.history[0]['total_value']
        final_value = self.portfolio.history[-1]['total_value']
        
        total_return = (final_value - initial_value) / initial_value
        total_return_pct = total_return * 100
        
        # Calculate max drawdown
        max_value = initial_value
        max_drawdown = 0
        for state in self.portfolio.history:
            max_value = max(max_value, state['total_value'])
            drawdown = (max_value - state['total_value']) / max_value
            max_drawdown = max(max_drawdown, drawdown)
        
        # Count trades
        buy_trades = [t for t in self.trade_log if t['action'] == 'BUY']
        sell_trades = [t for t in self.trade_log if t['action'] == 'SELL']
        
        return {
            'initial_value': initial_value,
            'final_value': final_value,
            'total_return': total_return,
            'total_return_pct': total_return_pct,
            'max_drawdown': max_drawdown,
            'total_trades': len(self.trade_log),
            'buy_trades': len(buy_trades),
            'sell_trades': len(sell_trades),
            'portfolio_history': self.portfolio.history,
            'trade_log': self.trade_log,
            'final_holdings': self.portfolio.holdings
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


def visualize_results(results, symbols):
    """
    Create visualizations of backtest results
    
    Args:
        results (dict): Backtest results
        symbols (list): Stock symbols traded
    """
    if not results or not results['portfolio_history']:
        print("No data to visualize")
        return
    
    # Extract data from portfolio history
    dates = [state['date'] for state in results['portfolio_history']]
    total_values = [state['total_value'] for state in results['portfolio_history']]
    cash_values = [state['cash'] for state in results['portfolio_history']]
    holdings_values = [state['holdings_value'] for state in results['portfolio_history']]
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Trading Algorithm Backtest Results', fontsize=16, fontweight='bold')
    
    # Plot 1: Portfolio Value Over Time
    ax1 = axes[0, 0]
    ax1.plot(dates, total_values, 'b-', linewidth=2, label='Total Value')
    ax1.axhline(y=results['initial_value'], color='gray', linestyle='--', alpha=0.5, label='Initial Value')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Portfolio Value ($)')
    ax1.set_title('Portfolio Value Over Time')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.tick_params(axis='x', rotation=45)
    
    # Plot 2: Cash vs Holdings Value
    ax2 = axes[0, 1]
    ax2.plot(dates, cash_values, 'g-', linewidth=2, label='Cash')
    ax2.plot(dates, holdings_values, 'r-', linewidth=2, label='Holdings')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Value ($)')
    ax2.set_title('Cash vs Holdings Over Time')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax2.tick_params(axis='x', rotation=45)
    
    # Plot 3: Trade Distribution
    ax3 = axes[1, 0]
    trade_counts = {'BUY': results['buy_trades'], 'SELL': results['sell_trades']}
    colors = ['green', 'red']
    ax3.bar(trade_counts.keys(), trade_counts.values(), color=colors, alpha=0.7)
    ax3.set_ylabel('Number of Trades')
    ax3.set_title('Trade Distribution')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Add count labels on bars
    for i, (action, count) in enumerate(trade_counts.items()):
        ax3.text(i, count, str(count), ha='center', va='bottom')
    
    # Plot 4: Returns Summary
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    # Create text summary
    summary_text = f"""
    BACKTEST SUMMARY
    
    Initial Value:     ${results['initial_value']:,.2f}
    Final Value:       ${results['final_value']:,.2f}
    Total Return:      {results['total_return_pct']:+.2f}%
    Max Drawdown:      {results['max_drawdown']*100:.2f}%
    
    Total Trades:      {results['total_trades']}
    Buy Trades:        {results['buy_trades']}
    Sell Trades:       {results['sell_trades']}
    
    Final Holdings:
    """
    
    if results['final_holdings']:
        for symbol, shares in sorted(results['final_holdings'].items()):
            summary_text += f"    {symbol}: {shares:.4f} shares\n"
    else:
        summary_text += "    (None)\n"
    
    ax4.text(0.1, 0.5, summary_text, fontsize=11, family='monospace',
             verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.tight_layout()
    
    # Save the plot
    filename = 'backtest_results.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\n✓ Visualization saved to: {filename}")
    
    # Show the plot
    plt.show()


def main():
    """Main entry point for the backtest script"""
    parser = argparse.ArgumentParser(
        description='Backtest the Stock Trading Algorithm on historical data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python backtest.py                              # Backtest default stocks over 52 weeks
  python backtest.py --universe tech              # Backtest tech stocks
  python backtest.py --weeks 26                   # Backtest over 26 weeks
  python backtest.py --custom AAPL MSFT GOOGL     # Backtest custom stocks
  python backtest.py --cash 20000                 # Start with $20,000
        """
    )
    
    parser.add_argument(
        '--universe', '-u',
        choices=list(STOCK_UNIVERSES.keys()),
        default='default',
        help='Predefined stock universe to backtest (default: default)'
    )
    
    parser.add_argument(
        '--custom', '-c',
        nargs='+',
        metavar='SYMBOL',
        help='Custom list of stock symbols to backtest'
    )
    
    parser.add_argument(
        '--weeks', '-w',
        type=int,
        default=52,
        help='Number of weeks to backtest (default: 52)'
    )
    
    parser.add_argument(
        '--cash',
        type=float,
        default=10000.0,
        help='Initial portfolio cash (default: 10000.0)'
    )
    
    parser.add_argument(
        '--no-viz', '--no-visualization',
        action='store_true',
        help='Skip visualization'
    )
    
    args = parser.parse_args()
    
    # Determine which symbols to use
    if args.custom:
        symbols = [s.upper() for s in args.custom]
        print(f"\nUsing custom stock symbols: {symbols}")
    else:
        symbols = STOCK_UNIVERSES[args.universe]
        print(f"\nUsing '{args.universe}' stock universe: {symbols}")
    
    print_header("Stock Trading Algorithm - Backtest Simulation")
    
    print(f"\nConfiguration:")
    print(f"  Symbols: {', '.join(symbols)}")
    print(f"  Weeks: {args.weeks}")
    print(f"  Initial Cash: ${args.cash:,.2f}")
    
    # Initialize backtester
    backtester = Backtester(symbols, weeks=args.weeks, initial_cash=args.cash)
    
    # Fetch data
    stock_data = backtester.fetch_data()
    if stock_data is None:
        return 1
    
    # Run backtest
    results = backtester.run(stock_data)
    if results is None:
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
            print(f"  {symbol}: {shares:.4f} shares")
    else:
        print(f"\nFinal Holdings: None (all cash)")
    
    # Show recent trades
    if results['trade_log']:
        print_section("Recent Trades (Last 10)")
        recent_trades = results['trade_log'][-10:]
        for trade in recent_trades:
            action_symbol = "🔴" if trade['action'] == 'BUY' else "🟢"
            print(f"{action_symbol} {trade['date'].strftime('%Y-%m-%d')}: "
                  f"{trade['action']:4s} {trade['shares']:.4f} {trade['symbol']:6s} @ "
                  f"${trade['price']:.2f} (${trade['amount']:.2f}) "
                  f"[{trade['weekly_change']*100:+.2f}%]")
    
    # Visualize results
    if not args.no_viz:
        print_section("Generating Visualization")
        try:
            visualize_results(results, symbols)
        except Exception as e:
            print(f"⚠ Warning: Could not create visualization: {e}")
            print("  You can still view the numeric results above.")
    
    print("\n" + "=" * 70)
    print("Backtest Complete!")
    print("=" * 70 + "\n")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
