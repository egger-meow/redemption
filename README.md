# Crypto Perpetual Trading Framework

A clean, OOP-based framework for developing and testing crypto perpetual trading strategies with built-in position sizing and risk management.

## Why "Redemption"?

After losing significant money in crypto last year by holding altcoins and meme coins without proper analysis or strategy, I decided it was time for a **redemption arc**. No more holding shit coins hoping they'll moon. No more buying into hype without doing the real work.

This framework represents a commitment to:
- **Real technical analysis** instead of gambling
- **Disciplined risk management** instead of emotional trading
- **Data-driven decisions** instead of following Twitter shills
- **Calculated position sizing** instead of YOLO trades
- **Systematic strategies** instead of hope and prayers

If you've been burned by crypto like I have, this is your tool to fight back with discipline and analysis.

## Features

- **Real-time Price Data**: Integration with CryptoCompare API
- **Interactive K線圖 Visualization**: Beautiful candlestick charts with volume analysis and technical indicators
- **Position Sizing Calculator**: Automatically calculate position sizes based on risk parameters
- **Extensible Strategy Framework**: Easy-to-extend base classes for custom strategies
- **Risk Management**: Built-in stop loss and target calculations
- **Technical Analysis Tools**: SMA, EMA, and expandable indicator system
- **Clean Architecture**: Modular, OOP design for easy maintenance and expansion

## Project Structure

```
redemption/
├── src/
│   ├── data_providers/       # Price data providers
│   │   ├── base_provider.py
│   │   └── cryptocompare_provider.py
│   ├── position/             # Position sizing logic
│   │   └── position_calculator.py
│   ├── strategies/           # Trading strategies
│   │   ├── base_strategy.py
│   │   └── simple_strategy.py
│   └── visualization/        # Interactive charts (K線圖)
│       ├── chart_visualizer.py
│       └── README.md
├── main.py                   # Main example
├── example_chart.py          # Chart visualization examples
├── quick_chart_demo.py       # Quick chart demo
├── CHART_QUICKSTART.md       # Chart quick start guide
├── requirements.txt          # Python dependencies
└── .env.example             # Environment variables template
```

## Installation

1. **Clone the repository**
   ```bash
   cd e:\IDEA\redemption
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment** (optional)
   ```bash
   copy .env.example .env
   # Edit .env with your settings
   ```

## Quick Start

**Trading Strategy Example:**

```bash
python main.py
```

**Interactive K線圖 Visualization:**

```bash
python quick_chart_demo.py
```

**Full example with market data:**

```bash
python example.py
```

## Usage

### Set Your Own Stop Loss and Target Prices

```python
from src.data_providers import CryptoCompareProvider
from src.position import PositionCalculator
from src.strategies import SimpleStopLossStrategy

# 1. Set your max loss amount
calculator = PositionCalculator(max_loss_amount=300)

# 2. Initialize strategy
data_provider = CryptoCompareProvider()
strategy = SimpleStopLossStrategy(
    data_provider=data_provider,
    position_calculator=calculator,
    symbol="BTC"
)

# 3. Set YOUR stop loss and target prices
strategy.set_levels(
    stop_loss_price=99000.0,   # Your stop loss
    target_price=108000.0       # Your target
)

# 4. Get position size automatically calculated
result = strategy.execute_strategy()
print(f"Position Size: {result['entry']['position_size']:.6f} BTC")
print(f"Max Loss: ${result['entry']['potential_loss']:.2f}")
print(f"Potential Profit: ${result['entry']['potential_profit']:.2f}")
```

### Direct Position Calculation

```python
from src.position import PositionCalculator

calculator = PositionCalculator(max_loss_amount=300)

position = calculator.calculate_position_size(
    current_price=101000.0,
    stop_loss=99000.0,      # Your stop loss price
    target_price=108000.0   # Your target price
)

print(f"Position Size: {position['position_size']}")
print(f"Max Loss: ${position['potential_loss']}")
```

### Creating Custom Strategies

Extend `BaseStrategy` to create your own trading strategies:

```python
from src.strategies import BaseStrategy

class MyCustomStrategy(BaseStrategy):
    def generate_signal(self):
        # Your signal logic here
        current_price = self.get_current_price()
        
        # Example: Simple moving average crossover, etc.
        # Add your indicators and logic
        
        return {
            "action": "BUY",
            "current_price": current_price,
            "stop_loss": current_price * 0.98,
            "target": current_price * 1.05
        }
    
    def calculate_entry(self):
        signal = self.generate_signal()
        return self.position_calculator.calculate_position_size(
            current_price=signal["current_price"],
            stop_loss=signal["stop_loss"],
            target_price=signal["target"]
        )
```

## Configuration

Edit `config.py` or use environment variables:

- `CRYPTOCOMPARE_API_KEY`: API key for CryptoCompare (optional, for higher limits)
- `MAX_LOSS_AMOUNT`: Maximum amount you're willing to lose per trade (default: 300)
- `DEFAULT_SYMBOL`: Trading symbol (default: BTC)
- `DEFAULT_CURRENCY`: Quote currency (default: USD)
- `DEFAULT_STOP_LOSS_PCT`: Default stop loss percentage (default: 0.02 = 2%)
- `DEFAULT_TARGET_PCT`: Default target percentage (default: 0.05 = 5%)

## Extending the Framework

### Adding New Data Providers

1. Create a new provider class inheriting from `BaseDataProvider`
2. Implement `get_current_price()` and `get_market_data()` methods
3. Add to `src/data_providers/__init__.py`

### Adding New Strategies

1. Create a new strategy class inheriting from `BaseStrategy`
2. Implement `generate_signal()` and `calculate_entry()` methods
3. Add your custom indicators and logic
4. Add to `src/strategies/__init__.py`

## Risk Warning

⚠️ **This is a development framework for educational purposes.**

- Always test strategies thoroughly before using real funds
- Past performance does not guarantee future results
- Crypto trading involves significant risk
- Never risk more than you can afford to lose

## License

MIT License - Feel free to use and modify for your needs.

## Next Steps

- Add technical indicators (RSI, MACD, Bollinger Bands, etc.)
- Implement backtesting functionality
- Add multiple timeframe analysis
- Create paper trading mode
- Add trade logging and performance tracking
- Integrate with exchange APIs for live trading
