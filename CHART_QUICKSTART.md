# K線圖 (Candlestick Chart) Quick Start Guide

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `plotly` - Interactive charting
- `pandas` - Data manipulation
- `kaleido` - Image export
- `cryptocompare` - Market data

### 2. Run Example

```bash
python example_chart.py
```

This will create and open interactive charts in your browser!

## 📊 Basic Usage

```python
from src.data_providers import CryptoCompareProvider
from src.visualization import ChartVisualizer

# Initialize
provider = CryptoCompareProvider()
visualizer = ChartVisualizer(theme="plotly_dark")

# Fetch data (K線數據)
df = provider.get_historical_ohlcv(
    symbol="BTC",
    currency="USD",
    timeframe="hour",  # "minute", "hour", "day"
    limit=168          # Number of candles
)

# Create interactive chart with volume
fig = visualizer.create_candlestick_chart(
    df=df,
    symbol="BTC",
    currency="USD",
    timeframe="hour",
    show_volume=True  # Shows volume subplot
)

# Add technical indicators (optional)
fig = visualizer.add_technical_indicators(
    fig=fig,
    df=df,
    indicators=['SMA_20', 'SMA_50', 'EMA_12']
)

# Display in browser
visualizer.show_chart(fig)

# Or save as HTML
visualizer.save_chart(fig, "my_chart.html")
```

## 🎯 Available Timeframes

| Timeframe | Use Case | Example |
|-----------|----------|---------|
| `"minute"` | Day trading, scalping | Last 6 hours (360 candles) |
| `"hour"` | Swing trading | Last 7 days (168 candles) |
| `"day"` | Position trading | Last 3 months (90 candles) |

## 🎨 Chart Features

### Interactive Controls
- **Zoom**: Scroll or click zoom button
- **Pan**: Drag the chart
- **Hover**: See detailed OHLCV data
- **Time Range**: Click buttons (1h, 6h, 12h, 1d, 1w, 1m, All)
- **Export**: Download as PNG from toolbar

### Volume Subplot
- Color-coded volume bars
- Green: Price closed higher than open
- Red: Price closed lower than open
- Synchronized with candlestick chart

### Technical Indicators
- **SMA** (Simple Moving Average): `'SMA_20'`, `'SMA_50'`, `'SMA_200'`
- **EMA** (Exponential Moving Average): `'EMA_12'`, `'EMA_26'`, `'EMA_50'`

## 📝 Quick Examples

### Example 1: Bitcoin Hourly Chart (7 Days)

```python
from src import CryptoCompareProvider, ChartVisualizer

provider = CryptoCompareProvider()
visualizer = ChartVisualizer()

df = provider.get_historical_ohlcv("BTC", "USD", "hour", 168)
fig = visualizer.create_candlestick_chart(df, "BTC", "USD", "hour")
visualizer.show_chart(fig)
```

### Example 2: Ethereum Daily Chart with Moving Averages

```python
df = provider.get_historical_ohlcv("ETH", "USD", "day", 90)
fig = visualizer.create_candlestick_chart(df, "ETH", "USD", "day")
fig = visualizer.add_technical_indicators(fig, df, ['SMA_20', 'SMA_50'])
visualizer.show_chart(fig)
```

### Example 3: Multiple Timeframes

```python
# Fetch multiple timeframes
data = provider.get_ohlcv_multi_timeframe(
    symbol="BTC",
    currency="USD",
    timeframes=['hour', 'day']
)

# Create separate charts for each
for timeframe, df in data.items():
    fig = visualizer.create_candlestick_chart(df, "BTC", "USD", timeframe)
    visualizer.save_chart(fig, f"btc_{timeframe}_chart.html")
```

### Example 4: Minute Chart for Day Trading

```python
# Last 6 hours of minute data
df = provider.get_historical_ohlcv("BTC", "USD", "minute", 360)
fig = visualizer.create_candlestick_chart(df, "BTC", "USD", "minute")
visualizer.show_chart(fig)
```

## 💾 Saving Charts

```python
# Save as interactive HTML
visualizer.save_chart(fig, "chart.html", format="html")

# Save as static image
visualizer.save_chart(fig, "chart.png", format="png")
visualizer.save_chart(fig, "chart.jpg", format="jpg")
visualizer.save_chart(fig, "chart.svg", format="svg")
visualizer.save_chart(fig, "chart.pdf", format="pdf")
```

## 🎨 Themes

```python
# Dark theme (default)
visualizer = ChartVisualizer(theme="plotly_dark")

# Light theme
visualizer = ChartVisualizer(theme="plotly_white")

# Default plotly theme
visualizer = ChartVisualizer(theme="plotly")

# Other themes
visualizer = ChartVisualizer(theme="ggplot2")
visualizer = ChartVisualizer(theme="seaborn")
```

## 🔧 Customization

### Custom Chart Size

```python
fig = visualizer.create_candlestick_chart(
    df=df,
    symbol="BTC",
    currency="USD",
    timeframe="hour",
    height=1000,  # Height in pixels
    width=1600    # Width in pixels
)
```

### Without Volume

```python
fig = visualizer.create_candlestick_chart(
    df=df,
    symbol="BTC",
    currency="USD",
    timeframe="hour",
    show_volume=False  # Hide volume subplot
)
```

### Custom Title

```python
fig = visualizer.create_candlestick_chart(
    df=df,
    symbol="BTC",
    currency="USD",
    timeframe="hour",
    title="My Custom Bitcoin Chart 📈"
)
```

## 📚 More Information

- Full documentation: `src/visualization/README.md`
- Example script: `example_chart.py`
- Data provider docs: `src/data_providers/cryptocompare_provider.py`

## ⚡ Tips

1. **Start with hourly data** for general analysis
2. **Use minute data** only for short periods (avoid fetching thousands of candles)
3. **Add 2-3 indicators max** to avoid cluttering the chart
4. **Save as HTML** to keep interactivity
5. **Use time range selectors** to zoom into specific periods

## 🐛 Troubleshooting

### Charts not showing?
- Make sure you have internet connection (fetches data from CryptoCompare API)
- Check if browser opened automatically
- Try saving as HTML first: `visualizer.save_chart(fig, "test.html")`

### No data returned?
```python
df = provider.get_historical_ohlcv("BTC", "USD", "hour", 100)
if df is None or df.empty:
    print("API request failed - check connection")
else:
    print(f"Success! Got {len(df)} candles")
```

### Image export not working?
```bash
# Reinstall kaleido
pip install --upgrade kaleido
```

## 🎓 Learning Path

1. ✅ Run `example_chart.py` to see charts in action
2. ✅ Try modifying the example with different symbols (ETH, SOL, etc.)
3. ✅ Experiment with different timeframes
4. ✅ Add your favorite technical indicators
5. ✅ Customize colors and themes
6. ✅ Integrate with your trading strategies

Happy charting! 📊📈
