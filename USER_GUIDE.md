# Rayquasa User Guide

Complete guide to using the Rayquasa stock trading algorithm with practical examples and detailed explanations.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Testing Options](#testing-options)
3. [Understanding Output](#understanding-output)
4. [Usage Examples](#usage-examples)
5. [Advanced Configuration](#advanced-configuration)
6. [Integration in Your Code](#integration-in-your-code)
7. [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites

- **Python 3.8 or higher** installed on your system
- **Internet connection** (for fetching live market data)
- **pip** package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/HelloOjasMutreja/Rayquasa.git
cd Rayquasa

# Install dependencies
pip install -r requirements.txt
```

This installs:
- `pandas >= 1.5.0` - Data manipulation
- `numpy >= 1.23.0` - Numerical operations
- `yfinance >= 0.2.0` - Yahoo Finance API
- `matplotlib >= 3.5.0` - Visualization (for backtesting)

### Verify Installation

```bash
# Quick test with sample data (no internet required)
python example_usage.py
```

If successful, you'll see trading signals and portfolio analysis.

## Testing Options

### Option 1: Sample Data (Offline)

Perfect for:
- Verifying installation
- Understanding output format
- Testing without internet

```bash
python example_usage.py
```

**Output:**
```
============================================================
Stock Trading Algorithm - Example with Sample Data
============================================================

Total stocks in initial universe: 5
Stock symbols: ['STOCK_A', 'STOCK_B', 'STOCK_C', 'STOCK_D', 'STOCK_E']

------------------------------------------------------------
SUITABLE STOCKS (Trading Universe)
------------------------------------------------------------
Number of suitable stocks: 2
Stocks: ['STOCK_A', 'STOCK_C']

------------------------------------------------------------
TRADE SIGNALS
------------------------------------------------------------

STOCK_A:
  Signal: BUY
  Amount: $5.00
  Shares: 0.0535
  Current Price: $93.42
  Weekly Change: -6.00%

------------------------------------------------------------
SUMMARY
------------------------------------------------------------
Total Buy Orders: 1
Total Sell Orders: 0
Total Buy Value: $5.00
Total Sell Value: $0.00
Net Position: $-5.00
```

### Option 2: Live Market Data

Perfect for:
- Real-world testing
- Current market analysis
- Actual trading decisions

#### Basic Usage

```bash
# Test with default stocks (recommended for first test)
python test_with_live_data.py
```

This tests 8 major stocks: AAPL, GOOGL, MSFT, AMZN, TSLA, META, NVDA, JPM

#### Test Specific Sectors

```bash
# Technology stocks (AAPL, GOOGL, MSFT, META, NVDA, AMD, INTC, CSCO, ORCL, IBM)
python test_with_live_data.py --universe tech

# Financial stocks (JPM, BAC, WFC, GS, MS, C, USB, PNC, TFC, COF)
python test_with_live_data.py --universe finance

# Healthcare stocks (JNJ, UNH, PFE, MRK, ABBV, TMO, DHR, ABT, LLY, BMY)
python test_with_live_data.py --universe healthcare

# Energy stocks
python test_with_live_data.py --universe energy

# Consumer goods stocks
python test_with_live_data.py --universe consumer

# Small test set (AAPL, MSFT, GOOGL) - fastest for testing
python test_with_live_data.py --universe small
```

#### Test Custom Stocks

```bash
# Your favorite stocks
python test_with_live_data.py --custom AAPL TSLA NVDA AMD

# Mix of sectors
python test_with_live_data.py --custom AAPL JPM XOM JNJ WMT
```

#### Different Time Periods

```bash
# 1 month of data (default)
python test_with_live_data.py --period 1mo

# 3 months of data
python test_with_live_data.py --period 3mo

# 6 months of data
python test_with_live_data.py --period 6mo

# 1 year of data
python test_with_live_data.py --period 1y

# 2 years of data
python test_with_live_data.py --period 2y
```

**Note**: Longer periods provide more data points for better analysis.

#### List All Options

```bash
# See all available stock universes
python test_with_live_data.py --list-universes

# See help and all options
python test_with_live_data.py --help
```

### Option 3: Backtesting

Perfect for:
- Evaluating historical performance
- Understanding algorithm behavior
- Risk assessment

```bash
# Demo with sample data (offline)
python demo_backtest.py

# Backtest with real data
python backtest.py

# See BACKTEST.md for comprehensive backtesting guide
```

## Understanding Output

### Live Data Test Output

When you run `test_with_live_data.py`, you'll see:

```
======================================================================
              Stock Trading Algorithm - Live Market Data Test
======================================================================

Configuration:
  Stock Symbols: AAPL, MSFT, GOOGL
  Time Period: 1mo
  Number of Stocks: 3

----------------------------------------------------------------------
Fetching Live Data from Yahoo Finance
----------------------------------------------------------------------
Please wait, downloading market data...

✓ Successfully fetched data for 3/3 stocks

----------------------------------------------------------------------
Data Summary
----------------------------------------------------------------------
AAPL:
  Data points: 22
  Date range: 2024-09-21 to 2024-10-21
  Latest price: $180.00
  Price range: $170.00 - $185.00

----------------------------------------------------------------------
Suitable Stocks
----------------------------------------------------------------------
✓ 2 out of 3 stocks passed suitability filters

Trading Universe: AAPL, MSFT

Filtered out (1 stocks):
  GOOGL: Below minimum predictability threshold

----------------------------------------------------------------------
Trade Signals
----------------------------------------------------------------------

✓ 1 trade signal(s) generated:

🔴 AAPL:
   Action: BUY
   Amount: $5.00
   Shares: 0.0278
   Price: $180.00
   Weekly Change: -5.50%

----------------------------------------------------------------------
Trading Summary
----------------------------------------------------------------------
Total Buy Orders: 1
Total Sell Orders: 0
Buy Value: $5.00
Sell Value: $0.00
Net Position: $-5.00

----------------------------------------------------------------------
Detailed Analysis
----------------------------------------------------------------------

AAPL:
  ✓ Suitable for trading
  Latest Price: $180.00
  Weekly Change: -5.50%
  Signal: BUY $5.00
  Predictability: 0.67 (High)
  Volatility: 0.15 (Moderate)

MSFT:
  ✓ Suitable for trading
  Latest Price: $350.00
  Weekly Change: +2.30%
  Signal: HOLD (no action)
  Predictability: 0.58 (Medium)
  Volatility: 0.12 (Low)
```

### Understanding Trade Signals

#### 🔴 BUY Signal
- **Trigger**: Stock dropped ≥5% in the last week
- **Action**: Algorithm recommends buying $5 worth
- **Example**: Stock went from $100 → $94 (-6% change)
- **Calculation**: Shares = $5 / Current Price

#### 🟢 SELL Signal
- **Trigger**: Stock rose ≥10% in the last week
- **Action**: Algorithm recommends selling $10 worth
- **Example**: Stock went from $100 → $112 (+12% change)
- **Calculation**: Shares = $10 / Current Price

#### ⚪ HOLD Signal
- **Trigger**: Stock moved less than thresholds
- **Action**: No action recommended
- **Example**: Stock went from $100 → $103 (+3% change)
- **Note**: HOLD signals are not shown in trade output

### Understanding Metrics

#### Predictability Score (0-1)
- **What it measures**: How predictable a stock's price movements are
- **Scale**:
  - 0.0-0.3: Low predictability (filtered out)
  - 0.3-0.5: Medium predictability
  - 0.5-0.7: Good predictability
  - 0.7-1.0: High predictability
- **Impact**: Stocks below 0.3 are filtered out

#### Volatility
- **What it measures**: Annualized standard deviation of returns
- **Scale**:
  - <0.01: Too low (illiquid, filtered out)
  - 0.01-0.1: Low volatility
  - 0.1-0.3: Moderate volatility
  - 0.3-0.5: High volatility
  - >0.5: Too high (unpredictable, filtered out)
- **Impact**: Stocks outside 0.01-0.5 range are filtered out

#### Weekly Change
- **What it measures**: Percentage price change over last 7 trading days
- **Calculation**: (Current Price - Price 7 days ago) / Price 7 days ago × 100
- **Impact**: Determines BUY/SELL signals
  - ≤-5%: BUY signal
  - ≥+10%: SELL signal
  - Between: HOLD (no signal)

## Usage Examples

### Example 1: Quick Test with Default Settings

**Command:**
```bash
python test_with_live_data.py
```

**What it does:**
- Tests 8 major stocks (AAPL, GOOGL, MSFT, AMZN, TSLA, META, NVDA, JPM)
- Uses 1 month of historical data
- Shows all suitable stocks and trade signals

**Use case:** First-time users, quick market overview

### Example 2: Technology Sector Analysis

**Command:**
```bash
python test_with_live_data.py --universe tech --period 3mo
```

**What it does:**
- Tests 10 technology stocks
- Uses 3 months of historical data
- Provides more data points for better analysis

**Use case:** Tech sector investors, longer-term trends

### Example 3: Custom Stock Portfolio

**Command:**
```bash
python test_with_live_data.py --custom AAPL MSFT NVDA AMD --period 6mo
```

**What it does:**
- Tests your selected 4 stocks
- Uses 6 months of historical data
- Focuses analysis on your portfolio

**Use case:** Personal portfolio analysis, specific stock interests

### Example 4: Financial Sector with Short Period

**Command:**
```bash
python test_with_live_data.py --universe finance --period 1mo
```

**What it does:**
- Tests 10 financial stocks
- Uses recent 1 month data
- Captures current market conditions

**Use case:** Short-term trading, recent trend analysis

### Example 5: Mixed Sector Diversification

**Command:**
```bash
python test_with_live_data.py --custom AAPL JPM XOM JNJ WMT PG --period 3mo
```

**What it does:**
- Tests stocks from 6 different sectors (Tech, Finance, Energy, Healthcare, Retail, Consumer)
- Uses 3 months of data
- Evaluates diversified portfolio

**Use case:** Diversification analysis, sector comparison

### Example 6: High-Frequency Testing

**Command:**
```bash
python test_with_live_data.py --universe small
```

**What it does:**
- Tests only 3 stocks (AAPL, MSFT, GOOGL)
- Fast execution for quick tests
- Perfect for iterative testing

**Use case:** Algorithm testing, development, quick checks

## Advanced Configuration

### Customizing Algorithm Parameters

Create a Python script to customize thresholds:

```python
from stock_trading_algorithm import StockTradingAlgorithm, fetch_live_data

# Custom stock selector configuration
selector_config = {
    'min_volatility': 0.02,      # Higher minimum = less volatile stocks
    'max_volatility': 0.3,       # Lower maximum = avoid very volatile stocks
    'min_data_points': 30        # More data = better analysis
}

# Custom trading engine configuration
trading_config = {
    'buy_threshold': -0.03,      # Buy at 3% drop instead of 5%
    'sell_threshold': 0.15,      # Sell at 15% rise instead of 10%
    'buy_amount': 10.0,          # Buy $10 instead of $5
    'sell_amount': 20.0          # Sell $20 instead of $10
}

# Fetch data
symbols = ['AAPL', 'MSFT', 'GOOGL']
stock_data = fetch_live_data(symbols, period='1mo')

# Run with custom config
algorithm = StockTradingAlgorithm(
    selector_config=selector_config,
    trading_config=trading_config
)
results = algorithm.run(stock_data)

# Process results
for symbol, trade in results['trades'].items():
    print(f"{symbol}: {trade['signal']} ${trade['amount']}")
```

### Parameter Tuning Guide

#### Buy/Sell Thresholds
- **Conservative**: buy_threshold=-0.03 (3%), sell_threshold=0.15 (15%)
- **Default**: buy_threshold=-0.05 (5%), sell_threshold=0.10 (10%)
- **Aggressive**: buy_threshold=-0.07 (7%), sell_threshold=0.08 (8%)

#### Trade Amounts
- **Small**: buy=$5, sell=$10 (default)
- **Medium**: buy=$10, sell=$20
- **Large**: buy=$50, sell=$100

#### Volatility Filters
- **Conservative**: min=0.02, max=0.2 (stable stocks only)
- **Default**: min=0.01, max=0.5 (balanced)
- **Aggressive**: min=0.01, max=0.8 (allow volatile stocks)

## Integration in Your Code

### Basic Integration

```python
from stock_trading_algorithm import StockTradingAlgorithm, fetch_live_data

def run_daily_analysis():
    # Define your stock universe
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    
    # Fetch latest data
    stock_data = fetch_live_data(symbols, period='1mo')
    
    # Run algorithm
    algorithm = StockTradingAlgorithm()
    results = algorithm.run(stock_data)
    
    # Process buy signals
    for symbol, trade in results['trades'].items():
        if trade['signal'] == 'BUY':
            print(f"BUY ALERT: {symbol} at ${trade['price']:.2f}")
            print(f"  Recommended: {trade['shares']:.4f} shares (${trade['amount']:.2f})")
        elif trade['signal'] == 'SELL':
            print(f"SELL ALERT: {symbol} at ${trade['price']:.2f}")
            print(f"  Recommended: {trade['shares']:.4f} shares (${trade['amount']:.2f})")
    
    return results

if __name__ == '__main__':
    run_daily_analysis()
```

### Automated Trading Integration

```python
from stock_trading_algorithm import StockTradingAlgorithm, fetch_live_data
import schedule
import time

def check_and_trade():
    """Run algorithm and execute trades (example)"""
    symbols = ['AAPL', 'MSFT', 'GOOGL']
    stock_data = fetch_live_data(symbols, period='1mo')
    
    algorithm = StockTradingAlgorithm()
    results = algorithm.run(stock_data)
    
    for symbol, trade in results['trades'].items():
        if trade['signal'] in ['BUY', 'SELL']:
            # Here you would integrate with your brokerage API
            print(f"Execute: {trade['signal']} {trade['shares']:.4f} shares of {symbol}")
            # execute_trade(symbol, trade['signal'], trade['shares'])

# Run every day at market open (example: 9:30 AM)
schedule.every().day.at("09:30").do(check_and_trade)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Portfolio Monitoring

```python
from stock_trading_algorithm import StockTradingAlgorithm, fetch_live_data
import pandas as pd

def monitor_portfolio(portfolio_symbols):
    """Monitor portfolio and get recommendations"""
    stock_data = fetch_live_data(portfolio_symbols, period='1mo')
    
    algorithm = StockTradingAlgorithm()
    results = algorithm.run(stock_data)
    
    # Create summary DataFrame
    summary = []
    for symbol in portfolio_symbols:
        if symbol in results['suitable_stocks']:
            trade = results['trades'].get(symbol, {})
            summary.append({
                'Symbol': symbol,
                'Signal': trade.get('signal', 'HOLD'),
                'Price': trade.get('price', 0),
                'Weekly Change': trade.get('weekly_change', 0),
                'Recommendation': f"{trade.get('signal', 'HOLD')} ${trade.get('amount', 0):.2f}"
            })
    
    df = pd.DataFrame(summary)
    print(df.to_string(index=False))
    return df

# Example usage
my_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
monitor_portfolio(my_stocks)
```

## Troubleshooting

### Common Issues and Solutions

#### Issue: "Failed to fetch stock data"

**Possible Causes:**
- No internet connection
- Invalid stock symbols
- Yahoo Finance API rate limiting

**Solutions:**
```bash
# 1. Check internet connection
ping google.com

# 2. Verify stock symbols (must be uppercase)
python test_with_live_data.py --custom AAPL MSFT  # Correct
# Not: python test_with_live_data.py --custom aapl msft

# 3. If rate limited, wait a few minutes and try again
# Or reduce number of stocks:
python test_with_live_data.py --universe small
```

#### Issue: "ModuleNotFoundError: No module named 'yfinance'"

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install individually
pip install yfinance pandas numpy matplotlib
```

#### Issue: No trade signals generated

**Possible Causes:**
- Stocks didn't meet volatility/predictability filters
- Weekly price changes didn't reach thresholds
- Insufficient data

**Solutions:**
```bash
# 1. Try longer time period for more data
python test_with_live_data.py --period 3mo

# 2. Try different stocks
python test_with_live_data.py --universe tech

# 3. Check what stocks were filtered out in the output
# Look for "Filtered out" section

# 4. Use custom config with lower thresholds (in Python)
```

#### Issue: "Insufficient data for analysis"

**Cause:** Stock has less than minimum required data points (default: 30)

**Solutions:**
```bash
# Use longer time period
python test_with_live_data.py --period 3mo

# Or reduce minimum data points in custom config (Python)
```

#### Issue: "Permission denied" on Linux/Mac

**Solution:**
```bash
# Make script executable
chmod +x test_with_live_data.py

# Or run with python explicitly
python test_with_live_data.py
```

#### Issue: Visualization not created (backtesting)

**Solutions:**
```bash
# Check matplotlib is installed
pip install matplotlib

# Or skip visualization
python backtest.py --no-viz
```

### Getting Help

If you encounter issues not covered here:

1. **Check existing issues**: Visit [GitHub Issues](https://github.com/HelloOjasMutreja/Rayquasa/issues)
2. **Open new issue**: Provide:
   - Command you ran
   - Error message (full output)
   - Python version: `python --version`
   - OS: Windows/Mac/Linux
3. **Enable debug output** (when available in future versions)

## Tips for Best Results

### For Testing
1. **Start small**: Use `--universe small` for quick tests
2. **Test sectors**: Try different sectors to see varied signals
3. **Vary time periods**: Longer periods may give different signals
4. **Custom stocks**: Test stocks you're interested in
5. **Check regularly**: Market conditions change, run tests periodically

### For Live Trading (If Applicable)
1. **Paper trade first**: Test without real money
2. **Start with small amounts**: Use default $5/$10 values
3. **Monitor results**: Track performance over time
4. **Adjust parameters**: Fine-tune based on results
5. **Diversify**: Don't rely on single stock or sector
6. **Set limits**: Know your risk tolerance
7. **Stay informed**: Algorithm is a tool, not a replacement for research

### For Analysis
1. **Compare metrics**: Look at predictability and volatility together
2. **Context matters**: Consider broader market conditions
3. **Multiple runs**: Test same stocks over different periods
4. **Benchmark**: Compare against buy-and-hold strategy
5. **Document**: Keep track of what configurations work best

## Best Practices

### Data Quality
- Use at least 1 month of data for reliable signals
- 3-6 months provides better predictability scores
- Longer periods smooth out short-term noise

### Stock Selection
- Mix sectors for diversification
- Include both high and low volatility stocks
- Test both large-cap and mid-cap stocks

### Signal Interpretation
- HOLD is not a failure - it's prudent risk management
- Multiple consecutive BUY signals may indicate downtrend
- Check broader market context before acting

### Risk Management
- Never invest more than you can afford to lose
- Diversify across multiple stocks and sectors
- Set stop-loss limits for protection
- Regular rebalancing based on new signals

## Next Steps

After mastering the basics:

1. **Explore Backtesting**: See [BACKTEST.md](BACKTEST.md) for historical simulation
2. **Customize Parameters**: Adjust thresholds to match your strategy
3. **Integrate with Tools**: Connect to your trading platform
4. **Contribute**: Help improve the algorithm on GitHub
5. **Stay Updated**: Check for new features and improvements

## Disclaimer

⚠️ **Important**: This algorithm is for **educational purposes only**. 

- Do not use for actual trading without thorough testing
- Past performance does not guarantee future results
- Always do your own research before making investment decisions
- Consider consulting with a financial advisor
- Understand the risks involved in trading
- The developers are not responsible for any financial losses

---

**Happy Trading! 📈**

For more information:
- Main documentation: [README.md](README.md)
- Backtesting guide: [BACKTEST.md](BACKTEST.md)
- GitHub repository: https://github.com/HelloOjasMutreja/Rayquasa
