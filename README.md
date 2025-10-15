# Rayquas - Stock Trading Algorithm

An intelligent stock trading algorithm that automates buy/sell decisions based on weekly price movements while filtering out unpredictable stocks.

## Features

### Trading Logic
- **Buy Signal**: Automatically buys $5 worth of a stock when it drops 5% or more in the last week
- **Sell Signal**: Automatically sells $10 worth of a stock when it rises 10% or more in the last week
- **Simultaneous Execution**: Processes all stocks in the trading universe at once

### Stock Selection (Predictability Filter)
The algorithm includes intelligent stock selection criteria to avoid highly unpredictable stocks:
- **Volatility Filter**: Excludes stocks with extreme volatility (too low = illiquid, too high = unpredictable)
- **Predictability Score**: Calculates a score based on price consistency and trend patterns
- **Minimum Data Requirements**: Requires sufficient historical data for reliable analysis

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Using Sample Data

```python
from stock_trading_algorithm import StockTradingAlgorithm, create_sample_data

# Initialize the algorithm
algorithm = StockTradingAlgorithm()

# Create sample stock data
stock_data = create_sample_data()

# Run the algorithm
results = algorithm.run(stock_data)

# View results
print(f"Suitable stocks: {results['suitable_stocks']}")
print(f"Trades: {results['trades']}")
print(f"Summary: {results['summary']}")
```

### Using Live Data

```python
from stock_trading_algorithm import StockTradingAlgorithm, fetch_live_data

# Initialize the algorithm
algorithm = StockTradingAlgorithm()

# Fetch live data for specific stocks
symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
stock_data = fetch_live_data(symbols, period='1mo')

# Run the algorithm
results = algorithm.run(stock_data)
```

## Usage Examples

Run the example script to see the algorithm in action:

```bash
python example_usage.py
```

## Architecture

The project consists of three main modules:

### 1. Stock Selector (`stock_selector.py`)
Filters stocks to create a suitable trading universe:
- Calculates volatility and predictability metrics
- Filters out highly unpredictable stocks
- Ensures minimum data quality requirements

### 2. Trading Engine (`trading_engine.py`)
Executes the core trading logic:
- Calculates weekly price changes
- Generates buy/sell signals based on thresholds
- Executes trades for all suitable stocks
- Provides trade summaries

### 3. Stock Trading Algorithm (`stock_trading_algorithm.py`)
Main orchestrator that combines selection and trading:
- Integrates stock selector and trading engine
- Provides easy-to-use interface
- Supports custom configurations

## Configuration

### Custom Trading Parameters

```python
from stock_trading_algorithm import StockTradingAlgorithm

# Customize stock selection criteria
selector_config = {
    'min_volatility': 0.02,  # Minimum acceptable volatility
    'max_volatility': 0.3,   # Maximum acceptable volatility
    'min_data_points': 30    # Minimum historical data points
}

# Customize trading parameters
trading_config = {
    'buy_threshold': -0.05,  # 5% drop triggers buy
    'sell_threshold': 0.10,  # 10% rise triggers sell
    'buy_amount': 5.0,       # Dollar amount to buy
    'sell_amount': 10.0      # Dollar amount to sell
}

# Initialize with custom config
algorithm = StockTradingAlgorithm(
    selector_config=selector_config,
    trading_config=trading_config
)
```

## Testing

Run the test suite:

```bash
python -m unittest test_trading_algorithm.py -v
```

## How It Works

1. **Stock Filtering**: The algorithm first analyzes all stocks and filters out those that are:
   - Too volatile (unpredictable)
   - Too stable (illiquid)
   - Lacking sufficient historical data

2. **Price Analysis**: For each suitable stock, it calculates the percentage change over the last 7 days

3. **Signal Generation**:
   - If price dropped ≥5%: Generate BUY signal for $5
   - If price rose ≥10%: Generate SELL signal for $10
   - Otherwise: HOLD (no action)

4. **Execution**: All buy and sell orders are generated simultaneously for the entire trading universe

## Example Output

```
SUITABLE STOCKS (Trading Universe)
------------------------------------------------------------
Number of suitable stocks: 3
Stocks: ['STOCK_A', 'STOCK_C', 'STOCK_E']

TRADE SIGNALS
------------------------------------------------------------
STOCK_A:
  Signal: BUY
  Amount: $5.00
  Shares: 0.0549
  Current Price: $91.06
  Weekly Change: -6.00%

SUMMARY
------------------------------------------------------------
Total Buy Orders: 2
Total Sell Orders: 0
Total Buy Value: $10.00
Total Sell Value: $0.00
Net Position: $-10.00
```

## Dependencies

- pandas >= 1.5.0
- numpy >= 1.23.0
- yfinance >= 0.2.0 (for live data)

## License

This project is open source and available for educational purposes.
