"""
Backtest runner for executing algorithm backtests
"""
import os
import sys
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server use
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Add parent directory to path to import trading modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stock_trading_algorithm import StockTradingAlgorithm, fetch_live_data
from backtest import Portfolio


def run_backtest(backtest_result):
    """
    Run a backtest for the given BacktestResult object
    
    Args:
        backtest_result: BacktestResult instance
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get algorithm configuration
        algorithm_model = backtest_result.algorithm
        selector_config = algorithm_model.get_selector_config()
        trading_config = algorithm_model.get_trading_config()
        
        # Initialize algorithm
        algorithm = StockTradingAlgorithm(
            selector_config=selector_config,
            trading_config=trading_config
        )
        
        # Get symbols
        symbols = backtest_result.get_symbols_list()
        
        # Fetch historical data
        weeks = backtest_result.weeks
        period = f"{weeks + 8}w"  # Add buffer
        
        stock_data = fetch_live_data(symbols, period=period)
        
        if not stock_data:
            return False
        
        # Initialize portfolio
        portfolio = Portfolio(backtest_result.initial_cash)
        trade_log = []
        
        # Get date range
        all_dates = sorted(set(
            date for prices in stock_data.values() 
            for date in prices.index
        ))
        
        if len(all_dates) < 14:
            return False
        
        # Initialize portfolio
        start_date = all_dates[0]
        current_prices = {
            symbol: prices.loc[start_date] if start_date in prices.index else None
            for symbol, prices in stock_data.items()
        }
        current_prices = {k: v for k, v in current_prices.items() if v is not None}
        portfolio.record_state(start_date, current_prices)
        
        # Simulate week by week
        weeks_processed = 0
        i = 7
        
        while i < len(all_dates) and weeks_processed < weeks:
            current_date = all_dates[i]
            
            # Get data up to current date
            window_data = {}
            for symbol, prices in stock_data.items():
                mask = prices.index <= current_date
                if mask.sum() > 0:
                    window_data[symbol] = prices[mask]
            
            # Run algorithm
            if window_data:
                results = algorithm.run(window_data)
                
                # Get current prices
                current_prices = {}
                for symbol, prices in window_data.items():
                    if len(prices) > 0:
                        current_prices[symbol] = prices.iloc[-1]
                
                # Execute trades
                for symbol, trade in results['trades'].items():
                    if symbol in current_prices:
                        price = current_prices[symbol]
                        
                        if trade['signal'] == 'BUY':
                            shares = trade['amount'] / price
                            if portfolio.buy(symbol, shares, price):
                                trade_log.append({
                                    'date': current_date.isoformat(),
                                    'symbol': symbol,
                                    'action': 'BUY',
                                    'shares': shares,
                                    'price': float(price),
                                    'amount': trade['amount'],
                                    'weekly_change': float(trade['weekly_change']) if trade['weekly_change'] is not None else None
                                })
                        
                        elif trade['signal'] == 'SELL':
                            shares_to_sell = trade['amount'] / price
                            if symbol in portfolio.holdings:
                                actual_shares = min(shares_to_sell, portfolio.holdings[symbol])
                                if portfolio.sell(symbol, actual_shares, price):
                                    trade_log.append({
                                        'date': current_date.isoformat(),
                                        'symbol': symbol,
                                        'action': 'SELL',
                                        'shares': actual_shares,
                                        'price': float(price),
                                        'amount': actual_shares * price,
                                        'weekly_change': float(trade['weekly_change']) if trade['weekly_change'] is not None else None
                                    })
                
                # Record portfolio state
                portfolio.record_state(current_date, current_prices)
            
            i += 7
            weeks_processed += 1
        
        # Calculate results
        if not portfolio.history:
            return False
        
        initial_value = portfolio.history[0]['total_value']
        final_value = portfolio.history[-1]['total_value']
        
        total_return = (final_value - initial_value) / initial_value
        total_return_pct = total_return * 100
        
        # Calculate max drawdown
        max_value = initial_value
        max_drawdown = 0
        for state in portfolio.history:
            max_value = max(max_value, state['total_value'])
            drawdown = (max_value - state['total_value']) / max_value
            max_drawdown = max(max_drawdown, drawdown)
        
        # Count trades
        buy_trades = len([t for t in trade_log if t['action'] == 'BUY'])
        sell_trades = len([t for t in trade_log if t['action'] == 'SELL'])
        
        # Save results to model
        backtest_result.final_value = final_value
        backtest_result.total_return_pct = total_return_pct
        backtest_result.max_drawdown_pct = max_drawdown * 100
        backtest_result.total_trades = len(trade_log)
        backtest_result.buy_trades = buy_trades
        backtest_result.sell_trades = sell_trades
        
        backtest_result.set_trade_log(trade_log)
        backtest_result.set_portfolio_history(portfolio.history)
        backtest_result.set_final_holdings(portfolio.holdings)
        
        # Generate visualization
        chart_path = generate_chart(backtest_result, portfolio.history, initial_value)
        if chart_path:
            backtest_result.chart_path = chart_path
        
        backtest_result.save()
        
        return True
        
    except Exception as e:
        print(f"Error running backtest: {e}")
        import traceback
        traceback.print_exc()
        return False


def generate_chart(backtest_result, portfolio_history, initial_value):
    """
    Generate visualization chart for backtest results
    
    Args:
        backtest_result: BacktestResult instance
        portfolio_history: List of portfolio states
        initial_value: Initial portfolio value
        
    Returns:
        str: Path to generated chart
    """
    try:
        # Extract data from portfolio history
        dates = [state['date'] for state in portfolio_history]
        total_values = [state['total_value'] for state in portfolio_history]
        cash_values = [state['cash'] for state in portfolio_history]
        holdings_values = [state['holdings_value'] for state in portfolio_history]
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f'Backtest Results: {backtest_result.algorithm.name}', fontsize=16, fontweight='bold')
        
        # Plot 1: Portfolio Value Over Time
        ax1 = axes[0, 0]
        ax1.plot(dates, total_values, 'b-', linewidth=2, label='Total Value')
        ax1.axhline(y=initial_value, color='gray', linestyle='--', alpha=0.5, label='Initial Value')
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
        trade_counts = {'BUY': backtest_result.buy_trades, 'SELL': backtest_result.sell_trades}
        colors = ['green', 'red']
        ax3.bar(trade_counts.keys(), trade_counts.values(), color=colors, alpha=0.7)
        ax3.set_ylabel('Number of Trades')
        ax3.set_title('Trade Distribution')
        ax3.grid(True, alpha=0.3, axis='y')
        
        for i, (action, count) in enumerate(trade_counts.items()):
            ax3.text(i, count, str(count), ha='center', va='bottom')
        
        # Plot 4: Summary
        ax4 = axes[1, 1]
        ax4.axis('off')
        
        summary_text = f"""
    BACKTEST SUMMARY
    
    Initial Value:     ${backtest_result.initial_cash:,.2f}
    Final Value:       ${backtest_result.final_value:,.2f}
    Total Return:      {backtest_result.total_return_pct:+.2f}%
    Max Drawdown:      {backtest_result.max_drawdown_pct:.2f}%
    
    Total Trades:      {backtest_result.total_trades}
    Buy Trades:        {backtest_result.buy_trades}
    Sell Trades:       {backtest_result.sell_trades}
    
    Stocks: {backtest_result.symbols}
    Period: {backtest_result.weeks} weeks
        """
        
        ax4.text(0.1, 0.5, summary_text, fontsize=11, family='monospace',
                verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
        
        plt.tight_layout()
        
        # Save the plot
        media_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media', 'charts')
        os.makedirs(media_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'backtest_{backtest_result.id}_{timestamp}.png'
        filepath = os.path.join(media_dir, filename)
        
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        return filepath
        
    except Exception as e:
        print(f"Error generating chart: {e}")
        import traceback
        traceback.print_exc()
        return None
