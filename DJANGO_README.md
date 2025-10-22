# Trading Algorithm Platform - Django Web Application

A Django-based web platform for creating, testing, and visualizing custom trading algorithms on historical stock data.

## Features

### 1. Algorithm Management
- **Create Custom Algorithms**: Define your own trading strategies with customizable parameters
  - Buy/Sell thresholds (percentage changes that trigger trades)
  - Buy/Sell amounts (dollar amounts per trade)
  - Stock selection criteria (volatility ranges, minimum data points)
- **Edit Algorithms**: Modify existing algorithms to refine strategies
- **View Algorithm Details**: See complete configuration and backtest history

### 2. Backtesting
- **Run Backtests**: Test algorithms on historical market data from Yahoo Finance
- **Flexible Configuration**:
  - Choose from predefined stock universes (tech, finance, energy, healthcare, etc.)
  - Or specify custom stock symbols
  - Configure test period (1-260 weeks)
  - Set initial portfolio cash
- **Historical Simulation**: Week-by-week trading simulation respecting cash and holdings constraints

### 3. Results Visualization
- **Performance Metrics**:
  - Total return percentage
  - Maximum drawdown
  - Trade statistics (buy/sell counts)
- **Interactive Charts**:
  - Portfolio value over time
  - Cash vs holdings breakdown
  - Trade distribution
  - Performance summary
- **Trade History**: Detailed log of all executed trades

## Quick Start

### 1. Database Setup
```bash
# Run migrations to create database tables
python manage.py migrate

# Create sample algorithms
python manage.py create_sample_algorithms
```

### 2. Create a Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 3. Start the Development Server
```bash
python manage.py runserver
```

### 4. Access the Platform
- **Main Platform**: http://localhost:8000/
- **Admin Interface**: http://localhost:8000/admin/

## Usage Guide

### Creating an Algorithm

1. Navigate to "Create Algorithm" in the navigation menu
2. Fill in the basic information:
   - **Name**: Unique identifier for your algorithm
   - **Description**: Brief explanation of the strategy

3. Set trading parameters:
   - **Buy Threshold**: Percentage drop to trigger buy (e.g., -0.05 for 5% drop)
   - **Sell Threshold**: Percentage rise to trigger sell (e.g., 0.10 for 10% rise)
   - **Buy Amount**: Dollar amount to invest per buy signal
   - **Sell Amount**: Dollar amount to sell per sell signal

4. Configure stock selection:
   - **Min/Max Volatility**: Acceptable volatility range for stocks
   - **Min Data Points**: Minimum historical data required

5. Click "Create Algorithm"

### Running a Backtest

1. Select an algorithm from the algorithms list
2. Click "Run Backtest"
3. Configure the backtest:
   - **Stock Universe**: Choose a predefined set or enter custom symbols
   - **Weeks**: How many weeks of historical data to test (1-260)
   - **Initial Cash**: Starting portfolio value

4. Click "Run Backtest" and wait for completion
5. View detailed results and visualizations

### Predefined Stock Universes

- **Default**: AAPL, GOOGL, MSFT, AMZN, TSLA, META, NVDA, JPM
- **Tech**: Technology sector stocks
- **Finance**: Financial sector stocks
- **Energy**: Energy sector stocks
- **Healthcare**: Healthcare sector stocks
- **Consumer**: Consumer goods and retail stocks
- **Small**: Quick test set (3 stocks)

## Sample Algorithms

The platform includes three pre-configured algorithms:

1. **Default Strategy**: Original Rayquasa algorithm (5% drop buy, 10% rise sell)
2. **Aggressive Trader**: Lower thresholds for more frequent trading (3% drop, 7% rise)
3. **Conservative Strategy**: Higher thresholds for fewer, larger trades (7% drop, 15% rise)

## Project Structure

```
algorithms/
├── admin.py              # Admin interface configuration
├── forms.py              # Form definitions
├── models.py             # Database models (TradingAlgorithm, BacktestResult)
├── views.py              # View logic
├── urls.py               # URL routing
├── backtest_runner.py    # Backtest execution engine
├── templates/            # HTML templates
│   └── algorithms/
│       ├── base.html
│       ├── home.html
│       ├── algorithm_list.html
│       ├── algorithm_detail.html
│       ├── algorithm_form.html
│       ├── backtest_list.html
│       ├── backtest_detail.html
│       └── backtest_form.html
└── management/           # Management commands
    └── commands/
        └── create_sample_algorithms.py
```

## Models

### TradingAlgorithm
Stores algorithm configuration:
- Trading parameters (buy/sell thresholds and amounts)
- Stock selection parameters (volatility, data points)
- Metadata (created/updated timestamps)

### BacktestResult
Stores backtest results:
- Configuration (symbols, weeks, initial cash)
- Performance metrics (return, drawdown, trades)
- Detailed data (trade log, portfolio history, chart path)

## Technical Details

### Backtest Execution
The backtest runner:
1. Fetches historical data from Yahoo Finance
2. Simulates week-by-week trading
3. Applies algorithm rules to generate trade signals
4. Tracks portfolio value, cash, and holdings
5. Calculates performance metrics
6. Generates visualization charts

### Data Storage
- SQLite database (development)
- Media files stored in `media/charts/` directory
- JSON-encoded trade logs and portfolio history

### Integration
The Django app integrates with the existing Rayquasa components:
- `stock_trading_algorithm.py`: Core algorithm logic
- `trading_engine.py`: Trade signal generation
- `stock_selector.py`: Stock filtering
- `backtest.py`: Portfolio management

## Screenshots

### Home Page
![Home Page](https://github.com/user-attachments/assets/ca5cec9b-58b4-4a32-921c-9cd3735b8551)

### Algorithms List
![Algorithms List](https://github.com/user-attachments/assets/fdff56e9-39f0-4bce-a081-5522f6c8f7a2)

### Algorithm Detail
![Algorithm Detail](https://github.com/user-attachments/assets/ecf13232-24e4-4eca-af97-6f8680304e4e)

### Create Algorithm
![Create Algorithm](https://github.com/user-attachments/assets/713796bd-4e5a-4182-947b-a13d3590b908)

### Run Backtest
![Run Backtest](https://github.com/user-attachments/assets/f7de575c-3495-4491-aaf6-6710703bc112)

## Notes

- Backtests may take 1-2 minutes depending on the number of stocks and weeks
- Historical data is fetched from Yahoo Finance (internet connection required)
- Charts are automatically generated and saved for each backtest
- The platform is for educational purposes only

## Future Enhancements

Potential improvements:
- Real-time data streaming
- More advanced visualization options
- Strategy comparison tools
- Risk metrics (Sharpe ratio, etc.)
- Export results to CSV/PDF
- User authentication and multi-user support
