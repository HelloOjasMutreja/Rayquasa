# Quick Start Guide

This guide will help you quickly test the Rayquasa stock trading algorithm on your device.

## Prerequisites

1. **Python 3.8 or higher** installed
2. **Internet connection** (for fetching live market data)

## Installation

```bash
# Clone the repository
git clone https://github.com/HelloOjasMutreja/Rayquasa.git
cd Rayquasa

# Install dependencies
pip install -r requirements.txt
```

## Quick Testing

### 1. Test with Sample Data (No Internet Required)

```bash
python example_usage.py
```

This runs the algorithm with generated sample data to verify everything is working.

### 2. Test with Live Market Data

#### Option A: Use default stocks (recommended for first test)
```bash
python test_with_live_data.py
```

This will test with 8 major stocks: AAPL, GOOGL, MSFT, AMZN, TSLA, META, NVDA, JPM

#### Option B: Choose a specific sector
```bash
# Technology stocks
python test_with_live_data.py --universe tech

# Financial stocks
python test_with_live_data.py --universe finance

# Healthcare stocks
python test_with_live_data.py --universe healthcare
```

#### Option C: Test your own stocks
```bash
python test_with_live_data.py --custom AAPL MSFT NVDA TSLA
```

#### Option D: Use different time periods
```bash
# 3 months of data
python test_with_live_data.py --period 3mo

# 1 year of data
python test_with_live_data.py --period 1y
```

## Understanding the Output

The algorithm will show you:

1. **Data Summary**: How much historical data was fetched for each stock
2. **Trading Universe**: Which stocks passed the suitability filters
3. **Trade Signals**: 
   - 🔴 BUY signals (stock dropped ≥5%)
   - 🟢 SELL signals (stock rose ≥10%)
4. **Trading Summary**: Total buy/sell orders and net position
5. **Detailed Analysis**: Suitability scores and metrics for each stock

## Example Output

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
Trade Signals
----------------------------------------------------------------------

✓ 1 trade signal(s) generated:

🔴 AAPL:
   Action: BUY
   Amount: $5.00
   Shares: 0.0278
   Price: $180.00
   Weekly Change: -5.50%
```

## Exploring Different Options

```bash
# See all available stock universes
python test_with_live_data.py --list-universes

# See help and all options
python test_with_live_data.py --help
```

## Next Steps

Once you're comfortable with the basics:

1. **Customize Parameters**: Edit the algorithm configuration in your own Python script
2. **Add Your Own Logic**: Extend the `StockTradingAlgorithm` class
3. **Integrate with Trading Platform**: Use the signals for actual trading (at your own risk!)
4. **Backtest**: Test the algorithm with historical data using different periods

## Troubleshooting

### "Failed to fetch stock data"
- Check your internet connection
- Verify stock symbols are correct (use uppercase)
- Yahoo Finance may occasionally have rate limits

### "ModuleNotFoundError: No module named 'yfinance'"
```bash
pip install -r requirements.txt
```

### "Permission denied" on Linux/Mac
```bash
chmod +x test_with_live_data.py
```

## Support

For issues or questions, please open an issue on GitHub:
https://github.com/HelloOjasMutreja/Rayquasa/issues

---

**Disclaimer**: This algorithm is for educational purposes only. Always do your own research before making investment decisions. Past performance does not guarantee future results.
