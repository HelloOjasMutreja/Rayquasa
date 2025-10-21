# Rayquasa

An algorithm for stock trading, where if a stock goes below 5% in the last week, we buy $5 of that stock, and if another stock goes up by 10% in the last week, we sell $10 worth of that stock simultaneously, and we do this for all the stocks in our trading universe.

## Features

- **Stock Selection**: Filters stocks based on predictability and volatility metrics to build a suitable trading universe
- **Trading Signals**: Generates BUY/SELL/HOLD signals based on weekly price movements
- **Live Market Data**: Integrates with Yahoo Finance API (yfinance) to fetch real-time market data
- **Pandas Integration**: Uses pandas for efficient data manipulation and analysis
- **Flexible Configuration**: Customizable thresholds and parameters for different trading strategies

## Installation

1. Clone the repository:
```bash
git clone https://github.com/HelloOjasMutreja/Rayquasa.git
cd Rayquasa
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

Required packages:
- pandas >= 1.5.0
- numpy >= 1.23.0
- yfinance >= 0.2.0

## Testing the Algorithm

### Test with Live Market Data

The easiest way to test the algorithm with real market data is using the `test_with_live_data.py` script:

```bash
# Test with default stock universe (AAPL, GOOGL, MSFT, AMZN, TSLA, META, NVDA, JPM)
python test_with_live_data.py

# Test with tech stocks
python test_with_live_data.py --universe tech

# Test with finance stocks
python test_with_live_data.py --universe finance

# Test with custom stocks
python test_with_live_data.py --custom AAPL MSFT TSLA NVDA

# Test with 3 months of historical data
python test_with_live_data.py --period 3mo

# List all available stock universes
python test_with_live_data.py --list-universes
```

Available stock universes:
- `default`: Major tech and finance stocks
- `tech`: Technology sector stocks
- `finance`: Financial sector stocks
- `energy`: Energy sector stocks
- `healthcare`: Healthcare sector stocks
- `consumer`: Consumer goods and retail stocks
- `small`: Small test set (3 stocks)

### Test with Sample Data

To test with generated sample data (no internet required):

```bash
python example_usage.py
```

## Usage in Your Own Code

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

## Algorithm Details

### Stock Selection Process

The algorithm uses a two-stage process:

1. **Filtering**: Filters stocks based on:
   - Volatility (must be within acceptable range)
   - Predictability score (based on price patterns and consistency)
   - Minimum data requirements

2. **Signal Generation**: For suitable stocks, generates signals based on:
   - **BUY**: Stock drops 5% or more in the last week
   - **SELL**: Stock rises 10% or more in the last week
   - **HOLD**: No significant movement

### Trading Rules

- Buy $5 worth of stock when it drops ≥5% in a week
- Sell $10 worth of stock when it rises ≥10% in a week
- Only trade stocks that pass suitability filters
- Trades are generated simultaneously for all qualifying stocks

## Project Structure

```
Rayquasa/
├── stock_trading_algorithm.py   # Main algorithm implementation
├── trading_engine.py             # Trading logic and signal generation
├── stock_selector.py             # Stock filtering and selection
├── test_with_live_data.py        # Live data testing script (NEW!)
├── example_usage.py              # Example with sample data
├── test_trading_algorithm.py     # Unit tests
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Running Tests

Run the unit tests to verify the algorithm:

```bash
python test_trading_algorithm.py
```

All tests should pass with output:
```
..................
----------------------------------------------------------------------
Ran 18 tests in 0.XXXs

OK
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.
