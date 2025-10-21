# Rayquasa

A stock trading algorithm that buys stocks when they drop ≥5% in a week and sells when they rise ≥10%, applying intelligent stock filtering and portfolio management.

## Overview

Rayquasa is an automated trading algorithm that:
- 🔍 **Filters stocks** based on volatility and predictability metrics
- 📉 **Buys $5** worth when a stock drops ≥5% in the last week
- 📈 **Sells $10** worth when a stock rises ≥10% in the last week
- 📊 **Backtests** on historical data to evaluate performance
- 🔴 **Integrates** with Yahoo Finance for real-time market data

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/HelloOjasMutreja/Rayquasa.git
cd Rayquasa

# Install dependencies
pip install -r requirements.txt
```

**Requirements:** Python 3.8+, pandas ≥1.5.0, numpy ≥1.23.0, yfinance ≥0.2.0

### Test the Algorithm (30 seconds)

```bash
# Option 1: Test with sample data (no internet required)
python example_usage.py

# Option 2: Test with live market data
python test_with_live_data.py

# Option 3: Run backtest simulation
python demo_backtest.py
```

## Testing with Live Data

The `test_with_live_data.py` script makes it easy to test with real market data:

```bash
# Test default stocks (AAPL, GOOGL, MSFT, AMZN, TSLA, META, NVDA, JPM)
python test_with_live_data.py

# Test specific sectors
python test_with_live_data.py --universe tech        # Technology stocks
python test_with_live_data.py --universe finance     # Financial stocks
python test_with_live_data.py --universe healthcare  # Healthcare stocks

# Test your own stocks
python test_with_live_data.py --custom AAPL MSFT NVDA TSLA

# Use different time periods
python test_with_live_data.py --period 3mo   # 3 months
python test_with_live_data.py --period 1y    # 1 year

# See all options
python test_with_live_data.py --list-universes
```

### Available Stock Universes
- **default**: Major tech and finance stocks (8 stocks)
- **tech**: Technology sector (10 stocks)
- **finance**: Financial sector (10 stocks)
- **energy**: Energy sector (10 stocks)
- **healthcare**: Healthcare sector (10 stocks)
- **consumer**: Consumer goods and retail (10 stocks)
- **small**: Quick test set (3 stocks)

## Backtesting

Simulate the algorithm on historical data to see how it would have performed:

```bash
# Run demo backtest (no internet required)
python demo_backtest.py

# Backtest with real market data over 52 weeks
python backtest.py

# Backtest specific sectors
python backtest.py --universe tech --weeks 26

# Backtest custom stocks with custom initial cash
python backtest.py --custom AAPL MSFT GOOGL --cash 20000 --weeks 52

# Skip visualization for faster results
python backtest.py --no-viz
```

### Backtest Output
- **Performance Metrics**: Total return, max drawdown
- **Trade History**: Complete log of all buy/sell trades
- **Portfolio Tracking**: Cash, holdings, and total value over time
- **Visualization**: 4-panel chart saved as `backtest_results.png`

For comprehensive backtesting documentation, see [BACKTEST.md](BACKTEST.md).

## Using in Your Code

### Basic Usage

```python
from stock_trading_algorithm import StockTradingAlgorithm, fetch_live_data

# Fetch live data from Yahoo Finance
symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
stock_data = fetch_live_data(symbols, period='1mo')

# Initialize and run the algorithm
algorithm = StockTradingAlgorithm()
results = algorithm.run(stock_data)

# Access results
print(f"Suitable stocks: {results['suitable_stocks']}")
print(f"Trades: {results['trades']}")
print(f"Summary: {results['summary']}")
```

### Custom Configuration

```python
# Configure stock selector
selector_config = {
    'min_volatility': 0.02,      # Minimum acceptable volatility
    'max_volatility': 0.3,       # Maximum acceptable volatility
    'min_data_points': 30        # Minimum data points required
}

# Configure trading engine
trading_config = {
    'buy_threshold': -0.05,      # Buy if stock drops 5%
    'sell_threshold': 0.10,      # Sell if stock rises 10%
    'buy_amount': 5.0,           # Dollar amount to buy
    'sell_amount': 10.0          # Dollar amount to sell
}

# Initialize with custom config
algorithm = StockTradingAlgorithm(
    selector_config=selector_config,
    trading_config=trading_config
)
```

## How It Works

### 1. Stock Selection
Filters stocks based on:
- **Volatility**: Must be within acceptable range (0.01-0.5)
- **Predictability**: Pattern consistency score must be ≥0.3
- **Data Requirements**: Minimum 30 data points

### 2. Signal Generation
For suitable stocks, generates trading signals:
- **🔴 BUY**: Stock drops ≥5% in the last week → Buy $5 worth
- **🟢 SELL**: Stock rises ≥10% in the last week → Sell $10 worth
- **⚪ HOLD**: No significant movement → No action

### 3. Trade Execution
- Trades are generated simultaneously for all qualifying stocks
- Respects cash and holdings constraints in backtesting mode
- Uses current market prices for valuation

## Understanding the Output

When you run the algorithm, you'll see:

```
======================================================================
              Stock Trading Algorithm - Live Market Data Test              
======================================================================

✓ Successfully fetched data for 3/3 stocks

----------------------------------------------------------------------
Trade Signals
----------------------------------------------------------------------

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

### Key Metrics
- **Predictability Score** (0-1): How predictable price movements are
- **Volatility**: Annualized standard deviation of returns
- **Weekly Change**: Percentage price change over last 7 trading days

## Project Structure

```
Rayquasa/
├── stock_trading_algorithm.py   # Main algorithm implementation
├── trading_engine.py             # Trading logic and signal generation
├── stock_selector.py             # Stock filtering and selection
├── backtest.py                   # Backtesting with historical data
├── demo_backtest.py              # Backtest demo (sample data)
├── test_with_live_data.py        # Live data testing script
├── example_usage.py              # Basic usage example
├── test_trading_algorithm.py     # Unit tests
├── test_backtest.py              # Backtest tests
├── test_integration.py           # Integration tests
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── USER_GUIDE.md                 # Comprehensive user guide
└── BACKTEST.md                   # Backtesting documentation
```

## Django Web Application

A new Django-based web platform for creating, testing, and visualizing custom trading algorithms!

### Quick Start

```bash
# Run database migrations
python manage.py migrate

# Create sample algorithms
python manage.py create_sample_algorithms

# Start the web server
python manage.py runserver
```

Then open http://localhost:8000/ in your browser to:
- Create custom trading algorithms with your own parameters
- Run backtests on historical data
- View detailed performance metrics and visualizations
- Compare different algorithm strategies

For detailed documentation, see [DJANGO_README.md](DJANGO_README.md).

## Testing

```bash
# Run all unit tests
python test_trading_algorithm.py

# Run backtest tests
python test_backtest.py

# Run integration tests
python test_integration.py
```

Expected output: All tests should pass (26 total tests).

## Documentation

- **README.md** (this file): Overview and quick start
- **[USER_GUIDE.md](USER_GUIDE.md)**: Comprehensive usage guide with examples
- **[BACKTEST.md](BACKTEST.md)**: Complete backtesting documentation

## Troubleshooting

### "Failed to fetch stock data"
- Check your internet connection
- Verify stock symbols are correct (use uppercase)
- Yahoo Finance may have rate limits - try again later

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### No trade signals generated
- Stock may not pass volatility/predictability filters
- Weekly price change may not meet thresholds (5% drop or 10% rise)
- Try different stocks or longer time periods

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Disclaimer

⚠️ **Educational Purpose Only**: This algorithm is for educational purposes. Do not use it for actual trading without thorough testing and understanding of the risks involved. Past performance does not guarantee future results. Always do your own research before making investment decisions.
