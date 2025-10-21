# Backtesting Guide

Comprehensive guide to backtesting the Rayquasa trading algorithm on historical data.

## Table of Contents

1. [What is Backtesting?](#what-is-backtesting)
2. [Quick Start](#quick-start)
3. [Understanding Results](#understanding-results)
4. [Command Line Options](#command-line-options)
5. [How Backtesting Works](#how-backtesting-works)
6. [Visualization](#visualization)
7. [Example Scenarios](#example-scenarios)
8. [Technical Implementation](#technical-implementation)
9. [Limitations and Best Practices](#limitations-and-best-practices)
10. [Troubleshooting](#troubleshooting)

## What is Backtesting?

Backtesting simulates how the trading algorithm would have performed using historical market data. This helps you:

- **Evaluate Performance**: See potential returns and losses
- **Understand Behavior**: Learn how the algorithm trades over time
- **Assess Risk**: Measure maximum drawdown and volatility
- **Compare Strategies**: Test different configurations
- **Build Confidence**: Validate the algorithm before live use

**Important**: Past performance does not guarantee future results.

## Quick Start

### Option 1: Demo with Sample Data (No Internet)

Perfect for learning how backtesting works without needing market data.

```bash
python demo_backtest.py
```

**What it does:**
1. Generates 52 weeks of realistic sample stock price data
2. Simulates the trading algorithm week by week
3. Shows all trades executed
4. Displays performance metrics
5. Creates visualization saved as `backtest_results.png`

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

Test with actual historical data from Yahoo Finance.

```bash
# Backtest default stocks over 52 weeks (1 year)
python backtest.py

# Backtest tech stocks over 26 weeks (6 months)
python backtest.py --universe tech --weeks 26

# Backtest custom stocks over 12 weeks (3 months)
python backtest.py --custom AAPL MSFT GOOGL --weeks 12

# Start with $20,000 initial capital
python backtest.py --cash 20000 --weeks 52

# Skip visualization for faster results
python backtest.py --no-viz
```

## Understanding Results

### Key Metrics

#### Initial Portfolio Value
- Starting cash amount (default: $10,000)
- All available for trading at the beginning

#### Final Portfolio Value
- Total value at end = Cash + Holdings value
- Includes unsold shares at final market prices

#### Total Return
- Percentage gain or loss
- Formula: `(Final - Initial) / Initial × 100`
- Example: $10,000 → $10,500 = +5.00% return

#### Max Drawdown
- Largest peak-to-trough decline during the period
- Measures risk and volatility
- Lower is better for risk management
- Example: Portfolio goes $11,000 → $10,000 = 9.09% drawdown

#### Total Trades
- Number of buy and sell orders executed
- Shows algorithm activity level
- High frequency = more active trading

### Trade Log

Each trade shows complete details:

```
🔴 2024-11-27: BUY 0.0502 STOCK_C @ $99.68 ($5.00) [-7.86%]
```

**Breakdown:**
- **🔴/🟢**: BUY (red) or SELL (green) indicator
- **Date**: When the trade was executed
- **Shares**: Number of shares traded (0.0502)
- **Symbol**: Stock ticker (STOCK_C)
- **Price**: Price per share at execution ($99.68)
- **Amount**: Total dollar value ($5.00)
- **Weekly Change**: Price movement that triggered signal (-7.86%)

### Portfolio Tracking

View portfolio evolution over time:

```
Portfolio Value Over Time:
  2024-10-23: $10,000.00 (+0.00%) [Cash: $10000.00, Holdings: $0.00]
  2025-01-22: $10,001.02 (+0.01%) [Cash: $9985.00, Holdings: $16.02]
  2025-04-23: $10,001.41 (+0.01%) [Cash: $9985.00, Holdings: $16.41]
  2025-07-23: $10,000.22 (+0.00%) [Cash: $9980.00, Holdings: $20.22]
  2025-10-15: $10,001.58 (+0.02%) [Cash: $9985.00, Holdings: $16.58]
```

**Each line shows:**
- **Date**: Snapshot date
- **Total Value**: Cash + Holdings
- **Return**: % gain/loss from initial value
- **Cash**: Available cash for buying
- **Holdings**: Value of owned shares

### Final Holdings

See what stocks you own at the end:

```
Final Holdings:
  STOCK_C: 0.0502 shares @ $104.26 = $5.23
  STOCK_D: 0.0032 shares @ $141.28 = $0.45
  STOCK_E: 0.0677 shares @ $163.42 = $11.06
```

## Command Line Options

### Stock Universe Selection

```bash
# Predefined universes
python backtest.py --universe tech          # Technology (10 stocks)
python backtest.py --universe finance       # Financial (10 stocks)
python backtest.py --universe healthcare    # Healthcare (10 stocks)
python backtest.py --universe energy        # Energy (10 stocks)
python backtest.py --universe consumer      # Consumer goods (10 stocks)
python backtest.py --universe small         # Small set (3 stocks)
python backtest.py --universe default       # Mixed set (8 stocks)

# Custom stocks
python backtest.py --custom AAPL MSFT GOOGL NVDA
```

**Available Universes:**
- **default**: AAPL, GOOGL, MSFT, AMZN, TSLA, META, NVDA, JPM
- **tech**: AAPL, GOOGL, MSFT, META, NVDA, AMD, INTC, CSCO, ORCL, IBM
- **finance**: JPM, BAC, WFC, GS, MS, C, USB, PNC, TFC, COF
- **energy**: XOM, CVX, COP, SLB, EOG, MPC, PSX, VLO, OXY, HAL
- **healthcare**: JNJ, UNH, PFE, MRK, ABBV, TMO, DHR, ABT, LLY, BMY
- **consumer**: WMT, PG, KO, PEP, COST, HD, MCD, NKE, SBUX, TGT
- **small**: AAPL, MSFT, GOOGL

### Time Period Configuration

```bash
# Specify number of weeks to backtest
python backtest.py --weeks 12    # 12 weeks (3 months)
python backtest.py --weeks 26    # 26 weeks (6 months)
python backtest.py --weeks 52    # 52 weeks (1 year) - default
python backtest.py --weeks 104   # 104 weeks (2 years)
```

**Recommendations:**
- **12 weeks**: Quick tests, recent trends
- **26 weeks**: Medium-term analysis
- **52 weeks**: Standard full year backtest
- **104+ weeks**: Long-term strategy evaluation

### Initial Capital

```bash
# Adjust starting cash
python backtest.py --cash 5000      # Conservative: $5,000
python backtest.py --cash 10000     # Default: $10,000
python backtest.py --cash 50000     # Aggressive: $50,000
```

**Impact:** Higher capital allows more simultaneous trades but doesn't change percentage returns.

### Visualization Control

```bash
# Skip visualization for faster execution
python backtest.py --no-viz

# Include visualization (default)
python backtest.py
```

**Note:** Visualization saved as `backtest_results.png` in current directory.

### Combining Options

```bash
# Full customization
python backtest.py \
  --custom AAPL MSFT GOOGL AMZN TSLA \
  --weeks 26 \
  --cash 20000 \
  --no-viz
```

## How Backtesting Works

### Process Overview

```
1. Fetch Historical Data
   ↓
2. Initialize Portfolio (cash + empty holdings)
   ↓
3. For each week:
   ├── Get data up to current date
   ├── Run trading algorithm
   ├── Generate BUY/SELL signals
   ├── Execute trades (if cash/shares available)
   ├── Update portfolio state
   └── Record portfolio value
   ↓
4. Calculate performance metrics
   ↓
5. Generate visualization
   ↓
6. Display results
```

### Step-by-Step Explanation

#### Step 1: Data Fetching
```python
# Downloads historical stock prices
# For 52 weeks, gets ~365 days of data
# Ensures enough history for weekly calculations
```

#### Step 2: Portfolio Initialization
```python
Portfolio:
  Cash: $10,000 (or custom amount)
  Holdings: {} (empty, no shares owned)
  History: [] (will record each week)
```

#### Step 3: Week-by-Week Simulation

For each 7-day period:

**A. Get Current Data**
- Use only data available up to current simulation date
- Ensures realistic "look-forward bias" free simulation

**B. Run Algorithm**
- Apply stock filters (volatility, predictability)
- Calculate weekly price changes
- Generate signals (BUY/SELL/HOLD)

**C. Execute Trades**

BUY Signal:
```python
if signal == 'BUY' and cash >= buy_amount:
    shares = buy_amount / current_price
    holdings[symbol] += shares
    cash -= buy_amount
```

SELL Signal:
```python
if signal == 'SELL' and holdings[symbol] >= sell_shares:
    sell_value = sell_shares * current_price
    holdings[symbol] -= sell_shares
    cash += sell_value
```

**D. Record State**
```python
portfolio_value = cash + sum(holdings[s] * prices[s] for s in holdings)
history.append({
    'date': current_date,
    'value': portfolio_value,
    'cash': cash,
    'holdings_value': portfolio_value - cash
})
```

#### Step 4: Performance Calculation

```python
# Total Return
total_return = (final_value - initial_value) / initial_value * 100

# Max Drawdown
peak = initial_value
max_drawdown = 0
for value in portfolio_values:
    if value > peak:
        peak = value
    drawdown = (peak - value) / peak
    if drawdown > max_drawdown:
        max_drawdown = drawdown
max_drawdown_pct = max_drawdown * 100
```

### Trading Rules Applied

#### Stock Filtering
Only trades stocks that pass:
- **Volatility**: Between 0.01 and 0.5 (annualized)
- **Predictability**: Score ≥ 0.3
- **Data Points**: Minimum 30 points available

#### Buy Signal
**Trigger:** Stock drops ≥5% in last week
```
Conditions:
  - weekly_change <= -5%
  - stock passes suitability filters
  - cash >= $5 (buy amount)

Action:
  - Buy $5 worth of shares
  - Deduct $5 from cash
  - Add shares to holdings
```

#### Sell Signal
**Trigger:** Stock rises ≥10% in last week
```
Conditions:
  - weekly_change >= +10%
  - stock passes suitability filters
  - own shares of that stock
  - holdings >= $10 worth (sell amount)

Action:
  - Sell $10 worth of shares
  - Add proceeds to cash
  - Reduce shares in holdings
```

## Visualization

The backtest creates a comprehensive 4-panel visualization:

### Panel 1: Portfolio Value Over Time
- **Type**: Line chart
- **Shows**: Total portfolio value progression
- **Reference**: Gray dashed line at initial value
- **Insights**: Overall performance trend, growth/decline

### Panel 2: Cash vs Holdings
- **Type**: Line chart (dual)
- **Green Line**: Available cash
- **Red Line**: Value of stock holdings
- **Insights**: Capital deployment, cash management

### Panel 3: Trade Distribution
- **Type**: Bar chart
- **Shows**: Count of BUY vs SELL trades
- **Insights**: Trading activity, signal balance

### Panel 4: Results Summary
- **Type**: Text panel
- **Shows**: 
  - Initial and final values
  - Total return percentage
  - Max drawdown
  - Trade counts
  - Final holdings breakdown
- **Insights**: Complete performance summary

**File:** Saved as `backtest_results.png` in current directory

## Example Scenarios

### Scenario 1: Conservative Strategy
```bash
python backtest.py --cash 5000 --weeks 12 --universe finance
```

**Profile:**
- Lower initial capital ($5,000)
- Shorter time period (3 months)
- Stable sector (finance)

**Best for:** Risk-averse investors, testing waters

### Scenario 2: Aggressive Growth
```bash
python backtest.py --cash 20000 --weeks 52 --universe tech
```

**Profile:**
- Higher initial capital ($20,000)
- Full year backtest
- Volatile sector (tech)

**Best for:** Growth-focused investors, higher risk tolerance

### Scenario 3: Diversified Portfolio
```bash
python backtest.py --custom AAPL JPM XOM JNJ WMT --weeks 26
```

**Profile:**
- Mix of 5 sectors (tech, finance, energy, healthcare, consumer)
- Medium-term (6 months)
- Balanced approach

**Best for:** Diversification seekers, sector comparison

### Scenario 4: Quick Test
```bash
python backtest.py --universe small --weeks 12 --no-viz
```

**Profile:**
- Only 3 stocks
- Short period
- No visualization

**Best for:** Quick validation, development testing

### Scenario 5: Long-Term Analysis
```bash
python backtest.py --universe default --weeks 104 --cash 15000
```

**Profile:**
- 2 years of data
- Mixed stock universe
- Medium capital

**Best for:** Long-term strategy evaluation, trend analysis

## Technical Implementation

### Architecture Overview

The backtesting system consists of three main components:

#### 1. Portfolio Class
Manages portfolio state and operations.

**Attributes:**
```python
class Portfolio:
    cash: float              # Available cash
    holdings: dict           # {symbol: shares_owned}
    history: list            # Portfolio states over time
    trades: list             # All executed trades
```

**Methods:**
- `buy(symbol, shares, price)`: Purchase shares
- `sell(symbol, shares, price)`: Sell shares
- `get_value(prices)`: Calculate total portfolio value
- `record_state(date, prices)`: Save current state
- `can_buy(amount)`: Check if sufficient cash
- `can_sell(symbol, shares)`: Check if sufficient shares

#### 2. Backtester Class
Orchestrates the simulation.

**Workflow:**
```python
class Backtester:
    def run(symbols, weeks, initial_cash):
        # 1. Fetch historical data
        data = fetch_historical_data(symbols, weeks)
        
        # 2. Initialize portfolio
        portfolio = Portfolio(initial_cash)
        
        # 3. Simulate week by week
        for week in range(weeks):
            current_date = start_date + week * 7
            available_data = data[data.index <= current_date]
            
            # Run algorithm
            results = algorithm.run(available_data)
            
            # Execute trades
            for symbol, trade in results['trades'].items():
                if trade['signal'] == 'BUY':
                    portfolio.buy(symbol, trade['shares'], trade['price'])
                elif trade['signal'] == 'SELL':
                    portfolio.sell(symbol, trade['shares'], trade['price'])
            
            # Record state
            portfolio.record_state(current_date, current_prices)
        
        # 4. Calculate metrics
        metrics = calculate_performance(portfolio)
        
        return metrics, portfolio
```

#### 3. Visualization Function
Creates multi-panel charts.

**Process:**
```python
def visualize_results(portfolio, metrics):
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Panel 1: Portfolio value
    plot_portfolio_value(axes[0, 0], portfolio.history)
    
    # Panel 2: Cash vs holdings
    plot_cash_holdings(axes[0, 1], portfolio.history)
    
    # Panel 3: Trade distribution
    plot_trade_distribution(axes[1, 0], portfolio.trades)
    
    # Panel 4: Summary text
    plot_summary(axes[1, 1], metrics, portfolio)
    
    plt.savefig('backtest_results.png')
```

### Design Decisions

#### Week-by-Week Granularity
**Why:** Algorithm signals based on weekly price changes
**Benefit:** Natural simulation unit, matches trading logic

#### Portfolio Class Separation
**Why:** Separates portfolio management from backtesting logic
**Benefit:** Modular, testable, reusable

#### Trade Constraints
**Why:** Realistic simulation requires respecting limits
**Benefit:** Can't buy without cash, can't sell without shares

#### Look-Forward Bias Prevention
**Why:** Only use data available at each simulation date
**Benefit:** Realistic simulation, no "cheating" with future data

#### Demo with Sample Data
**Why:** Allow testing without internet/API access
**Benefit:** Learning tool, development aid, reproducible

### Performance Characteristics

**Execution Time:**
- 52-week backtest, 5 stocks: ~5-10 seconds
- 104-week backtest, 10 stocks: ~15-20 seconds

**Memory Usage:**
- Efficient week-by-week streaming
- Stores only necessary history
- ~50-100 MB for typical backtest

**Scalability:**
- Linear with number of weeks
- Linear with number of stocks
- Visualization adds ~1-2 seconds

## Limitations and Best Practices

### Limitations

#### 1. No Transaction Costs
**Reality:** Brokerages charge commissions/fees
**Impact:** Real returns will be lower
**Mitigation:** Factor in ~$0.50-$5 per trade mentally

#### 2. Perfect Execution
**Reality:** Orders may not fill at exact prices
**Impact:** Actual prices may differ slightly
**Mitigation:** Understand results are optimistic

#### 3. No Slippage
**Reality:** Price moves between signal and execution
**Impact:** Buy higher, sell lower than simulated
**Mitigation:** Add 0.1-0.5% buffer in expectations

#### 4. Limited Market Impact
**Reality:** Large orders can move prices
**Impact:** Small trades assumed, won't scale to millions
**Mitigation:** Only use with portfolio sizes < $100k

#### 5. Historical Data Only
**Reality:** Can't predict black swan events
**Impact:** Future may differ dramatically from past
**Mitigation:** Don't rely solely on backtest results

### Best Practices

#### For Backtesting

**1. Test Multiple Periods**
```bash
# Don't just test one period
python backtest.py --weeks 26
python backtest.py --weeks 52
python backtest.py --weeks 104
```

**2. Try Different Markets**
```bash
# Test various sectors
python backtest.py --universe tech
python backtest.py --universe finance
python backtest.py --universe healthcare
```

**3. Include Bear and Bull Markets**
- Test periods with market downturns
- Test periods with market rallies
- See how algorithm performs in each

**4. Compare Strategies**
- Run with different thresholds
- Compare against buy-and-hold
- Evaluate risk-adjusted returns

**5. Document Results**
- Keep log of backtests
- Note configurations used
- Track what works best

#### For Interpretation

**1. Consider Max Drawdown**
- High return with high drawdown = risky
- Moderate return with low drawdown = safer
- Can you tolerate the potential losses?

**2. Look at Trade Frequency**
- Too many trades = high costs in reality
- Too few trades = underutilized capital
- Sweet spot: 10-30 trades per year

**3. Analyze Portfolio Composition**
- Are you concentrated in one stock?
- Is cash sitting idle?
- Are you properly diversified?

**4. Context Matters**
- What was market doing overall?
- Were there major events?
- Would you have actually held through volatility?

**5. Be Conservative**
- Subtract 1-2% from returns for costs
- Add 0.5% to drawdown for safety
- Don't expect to match backtest exactly

#### For Risk Management

**1. Position Sizing**
- Don't exceed 20% in single stock
- Maintain 30%+ cash reserve
- Diversify across sectors

**2. Stop Losses**
- Set maximum loss per stock (e.g., 15%)
- Have overall portfolio stop (e.g., 20%)
- Stick to limits even if algorithm says hold

**3. Regular Rebalancing**
- Review portfolio monthly
- Sell winners that become too large
- Add to losers if still suitable

**4. Gradual Entry**
- Don't deploy all capital immediately
- Start with 25-50% of intended amount
- Increase as you gain confidence

## Troubleshooting

### Common Issues

#### Issue: "Failed to fetch stock data"

**Symptoms:**
```
Error: Failed to fetch historical data for AAPL
```

**Causes:**
- No internet connection
- Invalid stock symbols
- Yahoo Finance API unavailable

**Solutions:**
```bash
# 1. Check internet
ping google.com

# 2. Verify symbols (must be valid and uppercase)
python backtest.py --custom AAPL MSFT  # Correct
# Not: python backtest.py --custom aapl invalid_symbol

# 3. Try demo instead
python demo_backtest.py

# 4. Reduce number of stocks
python backtest.py --universe small
```

#### Issue: "Insufficient data for backtesting"

**Symptoms:**
```
Error: Need at least 14 days of data for analysis
```

**Causes:**
- Stock too new/recently IPO'd
- Requested period too long
- Data not available

**Solutions:**
```bash
# 1. Use shorter period
python backtest.py --weeks 12

# 2. Use different stocks
python backtest.py --universe tech

# 3. Check if stock is valid
# Visit finance.yahoo.com and search for symbol
```

#### Issue: Visualization not created

**Symptoms:**
- Backtest completes but no `backtest_results.png`

**Causes:**
- Matplotlib not installed
- Permission issues
- `--no-viz` flag used

**Solutions:**
```bash
# 1. Install matplotlib
pip install matplotlib

# 2. Check permissions
ls -la backtest_results.png
chmod 644 backtest_results.png

# 3. Ensure not skipping viz
python backtest.py  # Without --no-viz

# 4. Try demo
python demo_backtest.py
```

#### Issue: Poor/negative returns

**Symptoms:**
- Backtest shows losses
- Negative total return

**This is NOT a bug!**

**Understanding:**
- Algorithm may not perform well in all conditions
- Some periods naturally have poor results
- Market conditions matter

**Actions:**
```bash
# 1. Try different time period
python backtest.py --weeks 26

# 2. Test different stocks
python backtest.py --universe finance

# 3. Check if market was down overall
# Compare to S&P 500 for same period

# 4. Consider this a learning opportunity
# Not all strategies work in all conditions
```

#### Issue: Very high returns (>50%)

**Symptoms:**
- Unrealistically high returns in backtest

**Causes:**
- Short period with lucky timing
- Very volatile stocks
- Small number of trades

**Reality Check:**
```bash
# 1. Extend time period
python backtest.py --weeks 104  # 2 years

# 2. Test more stocks
python backtest.py --universe tech

# 3. Remember: past ≠ future
# Don't expect to replicate results
```

### Getting Help

If issues persist:

1. **Check Configuration**
   - Print current settings
   - Verify all parameters

2. **Review Documentation**
   - README.md for basics
   - USER_GUIDE.md for detailed usage
   - This file for backtesting

3. **Check GitHub Issues**
   - https://github.com/HelloOjasMutreja/Rayquasa/issues
   - Search for similar problems

4. **Open New Issue**
   - Provide full command run
   - Include error message
   - Share Python version
   - Mention operating system

## Summary

Backtesting is a powerful tool for:
- ✅ Evaluating algorithm performance
- ✅ Understanding trading behavior
- ✅ Assessing risk and returns
- ✅ Building confidence in strategy

Remember:
- ⚠️ Past performance ≠ future results
- ⚠️ Backtest is optimistic (no costs/slippage)
- ⚠️ Test multiple periods and conditions
- ⚠️ Use as one tool among many
- ⚠️ Always do your own research

**Next Steps:**
1. Run demo: `python demo_backtest.py`
2. Try real data: `python backtest.py`
3. Experiment with configurations
4. Analyze results critically
5. Paper trade before live trading

---

**Happy Backtesting! 📊**

For more information:
- Main documentation: [README.md](README.md)
- User guide: [USER_GUIDE.md](USER_GUIDE.md)
- GitHub: https://github.com/HelloOjasMutreja/Rayquasa
