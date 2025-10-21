# Backtesting Guide

This guide explains how to simulate the Rayquasa trading algorithm on historical data and visualize the results.

## What is Backtesting?

Backtesting runs the trading algorithm on past market data to see how it would have performed. This helps you:
- Understand the algorithm's behavior over time
- See potential returns and risks
- Evaluate trading frequency and patterns
- Visualize portfolio growth

## Quick Start

### Option 1: Demo with Sample Data (No Internet Required)

Run the demo script to see how backtesting works with generated sample data:

```bash
python demo_backtest.py
```

This will:
1. Generate 52 weeks of sample stock price data
2. Simulate the trading algorithm week by week
3. Show all trades that would have been executed
4. Display portfolio performance metrics
5. Create a visualization saved as `backtest_results.png`

**Example Output:**
```
Initial Portfolio Value: $10,000.00
Final Portfolio Value:   $10,001.58
Total Return:            +0.02%
Max Drawdown:            0.02%

Total Trades:  9
  Buy Trades:  7
  Sell Trades: 2
```

### Option 2: Backtest with Real Market Data

Test the algorithm with real historical data from Yahoo Finance:

```bash
# Backtest default stocks over 52 weeks
python backtest.py

# Backtest tech stocks over 26 weeks
python backtest.py --universe tech --weeks 26

# Backtest custom stocks
python backtest.py --custom AAPL MSFT GOOGL --weeks 12

# Start with custom initial cash
python backtest.py --cash 20000 --weeks 52
```

## Understanding the Results

### Key Metrics

**Initial Portfolio Value**
- The starting cash amount (default: $10,000)

**Final Portfolio Value**
- Total value at the end (cash + holdings)

**Total Return**
- Percentage gain or loss: `(Final - Initial) / Initial * 100`

**Max Drawdown**
- Largest peak-to-trough decline during the period
- Indicates risk/volatility
- Lower is better for risk management

**Total Trades**
- Number of buy and sell orders executed

### Trade Log

The backtest shows all trades executed with details:

```
🔴 2024-11-27: BUY 0.0502 STOCK_C @ $99.68 ($5.00) [-7.86%]
```

- **Date**: When the trade was executed
- **Action**: BUY (🔴) or SELL (🟢)
- **Shares**: Number of shares traded
- **Symbol**: Stock ticker
- **Price**: Price per share at execution
- **Amount**: Total dollar value of trade
- **Weekly Change**: Price movement that triggered the signal

### Portfolio Growth

Track how the portfolio value changed over time:

```
Portfolio Value Over Time:
  2024-10-23: $10,000.00 (+0.00%) [Cash: $10000.00, Holdings: $0.00]
  2025-01-22: $10,001.02 (+0.01%) [Cash: $9985.00, Holdings: $16.02]
  2025-04-23: $10,001.41 (+0.01%) [Cash: $9985.00, Holdings: $16.41]
  2025-07-23: $10,000.22 (+0.00%) [Cash: $9980.00, Holdings: $20.22]
  2025-10-15: $10,001.58 (+0.02%) [Cash: $9985.00, Holdings: $16.58]
```

## Visualization

The backtest creates a 4-panel visualization showing:

### 1. Portfolio Value Over Time
- Line chart showing total portfolio value
- Gray dashed line shows initial value for reference

### 2. Cash vs Holdings Over Time
- Green line: Available cash
- Red line: Value of stock holdings
- Shows how capital is deployed over time

### 3. Trade Distribution
- Bar chart showing number of BUY vs SELL trades
- Helps understand trading activity

### 4. Results Summary
- Text panel with key metrics
- Final holdings breakdown

The visualization is automatically saved as `backtest_results.png`.

## Command Line Options

### Basic Options

```bash
# Choose stock universe
python backtest.py --universe tech          # Tech stocks
python backtest.py --universe finance       # Financial stocks
python backtest.py --universe healthcare    # Healthcare stocks

# Custom stocks
python backtest.py --custom AAPL MSFT GOOGL NVDA

# Specify time period
python backtest.py --weeks 12               # 12 weeks (3 months)
python backtest.py --weeks 26               # 26 weeks (6 months)
python backtest.py --weeks 52               # 52 weeks (1 year)

# Adjust initial capital
python backtest.py --cash 5000              # Start with $5,000
python backtest.py --cash 50000             # Start with $50,000

# Skip visualization (faster)
python backtest.py --no-viz
```

### Available Stock Universes

- `default`: AAPL, GOOGL, MSFT, AMZN, TSLA, META, NVDA, JPM
- `tech`: Technology sector (10 stocks)
- `finance`: Financial sector (10 stocks)
- `energy`: Energy sector (10 stocks)
- `healthcare`: Healthcare sector (10 stocks)
- `consumer`: Consumer goods (10 stocks)
- `small`: Small test set (3 stocks)

## How the Backtest Works

1. **Fetch Historical Data**: Downloads stock prices for the specified period

2. **Week-by-Week Simulation**: 
   - Moves forward 7 days at a time
   - At each week, runs the algorithm on data available up to that point
   - Executes trades based on signals generated

3. **Portfolio Tracking**:
   - Starts with initial cash
   - Buys shares when BUY signals occur (if cash available)
   - Sells shares when SELL signals occur (if shares available)
   - Records portfolio state at each step

4. **Results Calculation**:
   - Computes total return
   - Calculates maximum drawdown
   - Generates trade statistics

5. **Visualization**:
   - Creates charts showing portfolio performance
   - Saves as PNG image

## Trading Rules Applied

The backtest follows the algorithm's trading rules:

- **BUY Signal**: When a stock drops ≥5% in a week
  - Buys $5 worth of shares
  - Only executes if cash is available

- **SELL Signal**: When a stock rises ≥10% in a week
  - Sells $10 worth of shares
  - Only executes if shares are owned

- **Stock Filtering**: Only trades stocks that pass suitability filters
  - Volatility within acceptable range
  - Minimum predictability score
  - Sufficient data points

## Example Scenarios

### Conservative Strategy
```bash
python backtest.py --cash 5000 --weeks 12 --universe finance
```
- Lower initial capital
- Shorter time period
- Stable sector (finance)

### Aggressive Strategy
```bash
python backtest.py --cash 20000 --weeks 52 --universe tech
```
- Higher initial capital
- Full year backtest
- Volatile sector (tech)

### Diversified Test
```bash
python backtest.py --custom AAPL JPM XOM JNJ WMT --weeks 26
```
- Mix of sectors
- Mid-term period
- 5 different stocks

## Tips for Interpreting Results

1. **Positive Returns Don't Guarantee Future Success**
   - Past performance ≠ future results
   - Market conditions change

2. **Consider Max Drawdown**
   - High drawdown = high risk
   - Can you tolerate the potential losses?

3. **Look at Trade Frequency**
   - Too many trades = high transaction costs in real trading
   - Too few trades = algorithm not active enough

4. **Analyze Different Time Periods**
   - Test multiple periods (bear markets, bull markets)
   - See how algorithm performs in different conditions

5. **Compare Portfolios**
   - Run multiple backtests with different settings
   - Compare against buy-and-hold strategy

## Limitations

- **No Transaction Costs**: Real trading has fees/commissions
- **Perfect Execution**: Assumes orders execute at exact prices
- **No Slippage**: Real prices may move between signal and execution
- **Limited Market Impact**: Assumes your trades don't affect prices
- **Historical Data Only**: Can't predict black swan events

## Next Steps

After backtesting:

1. **Analyze the Results**: Review metrics and trades
2. **Adjust Parameters**: Try different thresholds in the algorithm
3. **Test More Periods**: Backtest different time ranges
4. **Paper Trade**: Test in real-time without real money
5. **Start Small**: If going live, start with small amounts

## Troubleshooting

### "Failed to fetch stock data"
- Check internet connection
- Verify stock symbols are valid
- Try with fewer stocks or shorter period

### "Insufficient data for backtesting"
- Need at least 14 days of data
- Try shorter time period or different stocks

### Visualization not showing
- Use `--no-viz` to skip visualization
- Check matplotlib is installed: `pip install matplotlib`

## Support

For questions or issues:
- Open an issue on GitHub
- Check the README.md for general usage
- Review DEMO.md for more examples

---

**Disclaimer**: This is a simulation tool for educational purposes. Past performance does not guarantee future results. Always do your own research before making investment decisions.
