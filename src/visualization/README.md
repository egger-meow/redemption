# Interactive Chart Visualization Module

This module provides interactive candlestick chart (K線圖) visualization with volume data for cryptocurrency trading analysis.

## Features

- 📊 **Interactive Candlestick Charts**: Full OHLCV (Open, High, Low, Close, Volume) data visualization
- 📈 **Volume Subplot**: Color-coded volume bars synchronized with price action
- ⏱️ **Multiple Timeframes**: Support for minute, hourly, and daily charts
- 🎨 **Customizable Themes**: Multiple color schemes (dark/light/custom)
- 🔍 **Interactive Controls**: 
  - Zoom and pan
  - Time range selectors (1h, 6h, 12h, 1d, 1w, 1m, All)
  - Hover tooltips with detailed data
- 📉 **Technical Indicators**: SMA, EMA support
- 💾 **Export Options**: Save as HTML, PNG, JPG, SVG, PDF

## Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

Required packages:
- `plotly>=5.18.0` - Interactive charting library
- `pandas>=2.1.0` - Data manipulation
- `kaleido>=0.2.1` - Static image export

## Quick Start

### Basic Usage

```python
from src.data_providers import CryptoCompareProvider
from src.visualization import ChartVisualizer

# Initialize
provider = CryptoCompareProvider()
visualizer = ChartVisualizer(theme="plotly_dark")

# Fetch data
df = provider.get_historical_ohlcv(
    symbol="BTC",
    currency="USD",
    timeframe="hour",
    limit=168  # 7 days
)

# Create chart
fig = visualizer.create_candlestick_chart(
    df=df,
    symbol="BTC",
    currency="USD",
    timeframe="hour",
    show_volume=True
)

# Display
visualizer.show_chart(fig)
```

### With Technical Indicators

```python
# Add moving averages
fig = visualizer.add_technical_indicators(
    fig=fig,
    df=df,
    indicators=['SMA_20', 'SMA_50', 'EMA_12']
)

visualizer.show_chart(fig)
```

### Save Chart

```python
# Save as HTML (interactive)
visualizer.save_chart(fig, "chart.html", format="html")

# Save as static image
visualizer.save_chart(fig, "chart.png", format="png")
```

## API Reference

### ChartVisualizer

Main class for creating interactive charts.

#### `__init__(theme: str = "plotly_dark")`

Initialize visualizer with a theme.

**Parameters:**
- `theme` (str): Plotly theme name
  - Options: `"plotly"`, `"plotly_white"`, `"plotly_dark"`, `"ggplot2"`, `"seaborn"`

#### `create_candlestick_chart()`

Create interactive candlestick chart with volume.

**Parameters:**
- `df` (pd.DataFrame): OHLCV data
- `symbol` (str): Trading symbol (e.g., "BTC")
- `currency` (str): Quote currency (default: "USD")
- `timeframe` (str): Time interval - "minute", "hour", "day"
- `title` (str, optional): Custom chart title
- `show_volume` (bool): Show volume subplot (default: True)
- `height` (int): Chart height in pixels (default: 800)
- `width` (int, optional): Chart width in pixels

**Returns:**
- `go.Figure`: Plotly figure object

#### `add_technical_indicators()`

Add technical indicators to existing chart.

**Parameters:**
- `fig` (go.Figure): Existing Plotly figure
- `df` (pd.DataFrame): OHLCV data
- `indicators` (List[str]): List of indicators
  - Format: `"SMA_20"`, `"SMA_50"`, `"EMA_12"`, etc.

**Returns:**
- `go.Figure`: Updated figure

#### `save_chart()`

Save chart to file.

**Parameters:**
- `fig` (go.Figure): Plotly figure
- `filename` (str): Output filename
- `format` (str): File format - "html", "png", "jpg", "svg", "pdf"

#### `show_chart()`

Display chart in browser.

**Parameters:**
- `fig` (go.Figure): Plotly figure to display

## Data Provider Integration

### CryptoCompareProvider Methods

#### `get_historical_ohlcv()`

Fetch historical OHLCV data.

```python
df = provider.get_historical_ohlcv(
    symbol="BTC",
    currency="USD",
    timeframe="hour",  # "minute", "hour", "day"
    limit=100
)
```

**Returns DataFrame with columns:**
- `timestamp` (datetime): Candle timestamp
- `open` (float): Opening price
- `high` (float): Highest price
- `low` (float): Lowest price
- `close` (float): Closing price
- `volume` (float): Trading volume
- `volume_from` (float): Volume in base currency
- `volume_to` (float): Volume in quote currency

#### `get_ohlcv_multi_timeframe()`

Fetch data for multiple timeframes.

```python
data = provider.get_ohlcv_multi_timeframe(
    symbol="BTC",
    currency="USD",
    timeframes=['hour', 'day']
)
# Returns: Dict[str, pd.DataFrame]
```

## Examples

See `example_chart.py` for complete examples:

```bash
python example_chart.py
```

### Example 1: Hourly Chart with Indicators

```python
from src.data_providers import CryptoCompareProvider
from src.visualization import ChartVisualizer

provider = CryptoCompareProvider()
visualizer = ChartVisualizer()

df = provider.get_historical_ohlcv("BTC", "USD", "hour", 168)
fig = visualizer.create_candlestick_chart(df, "BTC", "USD", "hour")
fig = visualizer.add_technical_indicators(fig, df, ['SMA_20', 'SMA_50'])

visualizer.save_chart(fig, "btc_hourly.html")
visualizer.show_chart(fig)
```

### Example 2: Daily Chart (3 months)

```python
df = provider.get_historical_ohlcv("ETH", "USD", "day", 90)
fig = visualizer.create_candlestick_chart(df, "ETH", "USD", "day")
visualizer.show_chart(fig)
```

### Example 3: Minute Chart for Day Trading

```python
df = provider.get_historical_ohlcv("BTC", "USD", "minute", 360)  # 6 hours
fig = visualizer.create_candlestick_chart(df, "BTC", "USD", "minute")
visualizer.show_chart(fig)
```

## Chart Interactions

### Mouse Controls
- **Drag**: Pan the chart
- **Scroll**: Zoom in/out
- **Double-click**: Reset zoom
- **Hover**: Show detailed OHLCV data

### Range Selector Buttons
- **1h**: Last 1 hour
- **6h**: Last 6 hours
- **12h**: Last 12 hours
- **1d**: Last 1 day
- **1w**: Last 1 week
- **1m**: Last 1 month
- **All**: Show all data

### Toolbar (Top Right)
- 🔍 Zoom
- ↔️ Pan
- 📦 Box select
- 🏠 Reset axes
- 📷 Download plot as PNG

## Customization

### Color Schemes

```python
visualizer = ChartVisualizer()
visualizer.default_colors = {
    'increasing': '#26a69a',  # Bullish candles (green)
    'decreasing': '#ef5350',  # Bearish candles (red)
    'volume_increasing': 'rgba(38, 166, 154, 0.5)',
    'volume_decreasing': 'rgba(239, 83, 80, 0.5)'
}
```

### Custom Chart Dimensions

```python
fig = visualizer.create_candlestick_chart(
    df=df,
    symbol="BTC",
    currency="USD",
    timeframe="hour",
    height=1000,  # Taller chart
    width=1600    # Wider chart
)
```

### Disable Volume Subplot

```python
fig = visualizer.create_candlestick_chart(
    df=df,
    symbol="BTC",
    currency="USD",
    timeframe="hour",
    show_volume=False  # Hide volume
)
```

## Technical Indicators

### Supported Indicators

- **SMA (Simple Moving Average)**: `"SMA_20"`, `"SMA_50"`, `"SMA_200"`
- **EMA (Exponential Moving Average)**: `"EMA_12"`, `"EMA_26"`, `"EMA_50"`

### Adding Custom Indicators

```python
# Calculate custom indicator
df['VWAP'] = (df['volume'] * df['close']).cumsum() / df['volume'].cumsum()

# Add to chart manually
import plotly.graph_objects as go

fig.add_trace(
    go.Scatter(
        x=df['timestamp'],
        y=df['VWAP'],
        name='VWAP',
        line=dict(color='yellow', width=2)
    ),
    row=1, col=1
)
```

## Troubleshooting

### Issue: No data returned

```python
# Check if data was fetched successfully
df = provider.get_historical_ohlcv("BTC", "USD", "hour", 100)
if df is None or df.empty:
    print("Failed to fetch data - check API connection")
else:
    print(f"Fetched {len(df)} candles")
```

### Issue: Chart not displaying

```python
# Ensure plotly is properly installed
pip install --upgrade plotly

# Try saving as HTML first
visualizer.save_chart(fig, "test_chart.html")
# Then open test_chart.html in your browser
```

### Issue: Image export not working

```python
# Install kaleido for static image export
pip install kaleido

# Then try exporting
visualizer.save_chart(fig, "chart.png", format="png")
```

## Performance Tips

1. **Limit data points**: Don't fetch excessive data
   ```python
   # Good: Reasonable data points
   df = provider.get_historical_ohlcv("BTC", "USD", "hour", 168)
   
   # Avoid: Too much data may slow down rendering
   # df = provider.get_historical_ohlcv("BTC", "USD", "minute", 10000)
   ```

2. **Use appropriate timeframes**: Match timeframe to analysis period
   - Minute charts: 1-24 hours of data
   - Hourly charts: 1-30 days of data
   - Daily charts: 1-12 months of data

3. **Limit indicators**: Too many indicators can clutter the chart
   ```python
   # Good: 2-3 key indicators
   indicators=['SMA_20', 'SMA_50']
   
   # Avoid: Too many indicators
   # indicators=['SMA_5', 'SMA_10', 'SMA_20', 'SMA_50', 'SMA_100', 'SMA_200']
   ```

## License

Part of the Redemption cryptocurrency trading framework.
