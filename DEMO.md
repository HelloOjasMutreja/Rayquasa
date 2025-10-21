# Rayquasa Algorithm Demo

This document shows various examples of testing the Rayquasa stock trading algorithm.

## Example 1: Testing with Sample Data

Running with sample data (no internet required):

```bash
$ python example_usage.py
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

## Example 2: Testing with Live Market Data

### Command:
```bash
python test_with_live_data.py --universe small
```

### What it does:
- Fetches real-time data from Yahoo Finance for AAPL, MSFT, GOOGL
- Analyzes each stock for trading opportunities
- Generates BUY/SELL signals based on weekly price movements
- Shows detailed metrics for each stock

### Sample Output Structure:
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
```

## Example 3: Testing Different Sectors

### Technology Stocks:
```bash
python test_with_live_data.py --universe tech
```
Tests: AAPL, GOOGL, MSFT, META, NVDA, AMD, INTC, CSCO, ORCL, IBM

### Financial Stocks:
```bash
python test_with_live_data.py --universe finance
```
Tests: JPM, BAC, WFC, GS, MS, C, USB, PNC, TFC, COF

### Healthcare Stocks:
```bash
python test_with_live_data.py --universe healthcare
```
Tests: JNJ, UNH, PFE, MRK, ABBV, TMO, DHR, ABT, LLY, BMY

## Example 4: Custom Stock Selection

Test your favorite stocks:
```bash
python test_with_live_data.py --custom AAPL TSLA NVDA AMD
```

## Example 5: Different Time Periods

### 3 Months of Data:
```bash
python test_with_live_data.py --period 3mo
```

### 1 Year of Data:
```bash
python test_with_live_data.py --period 1y
```

Longer periods give more data points for better analysis.

## Example 6: Viewing All Options

List all available stock universes:
```bash
python test_with_live_data.py --list-universes
```

Output:
```
Available Stock Universes:
--------------------------------------------------

default:
  Stocks: AAPL, GOOGL, MSFT, AMZN, TSLA, META, NVDA, JPM
  Count: 8

tech:
  Stocks: AAPL, GOOGL, MSFT, META, NVDA, AMD, INTC, CSCO, ORCL, IBM
  Count: 10

finance:
  Stocks: JPM, BAC, WFC, GS, MS, C, USB, PNC, TFC, COF
  Count: 10
...
```

## Understanding the Signals

### 🔴 BUY Signal
- Stock dropped ≥5% in the last week
- Algorithm recommends buying $5 worth
- Example: Stock went from $100 → $94 (-6%)

### 🟢 SELL Signal
- Stock rose ≥10% in the last week
- Algorithm recommends selling $10 worth
- Example: Stock went from $100 → $112 (+12%)

### ⚪ HOLD Signal (not shown in trades)
- Stock moved less than thresholds
- No action recommended
- Example: Stock went from $100 → $103 (+3%)

## Key Metrics Explained

### Predictability Score (0-1)
- Measures how predictable a stock's price movements are
- Higher = more predictable patterns
- Stocks below 0.3 are filtered out

### Volatility
- Annualized standard deviation of returns
- Too low = illiquid, too high = unpredictable
- Acceptable range: 0.01 - 0.5

### Weekly Change
- Percentage change in price over last 7 trading days
- Used to generate BUY/SELL signals
- Example: -6% triggers BUY, +12% triggers SELL

## Integration with Your Code

```python
from stock_trading_algorithm import StockTradingAlgorithm, fetch_live_data

# Fetch data
symbols = ['AAPL', 'MSFT', 'GOOGL']
stock_data = fetch_live_data(symbols, period='1mo')

# Run algorithm
algorithm = StockTradingAlgorithm()
results = algorithm.run(stock_data)

# Get trades
for symbol, trade in results['trades'].items():
    print(f"{symbol}: {trade['signal']} ${trade['amount']}")
```

## Tips for Testing

1. **Start Small**: Use `--universe small` for quick tests
2. **Test Sectors**: Try different sectors to see how the algorithm performs
3. **Vary Time Periods**: Longer periods may give different signals
4. **Custom Stocks**: Test stocks you're interested in
5. **Check Regularly**: Market conditions change, run tests periodically

## Disclaimer

This is an educational trading algorithm. Do not use it for actual trading without thorough testing and understanding of the risks. Past performance does not guarantee future results.
