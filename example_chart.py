"""Example: Interactive Candlestick Chart with Volume - K線圖示例."""
from src.data_providers import CryptoCompareProvider
from src.visualization import ChartVisualizer


def main():
    """Create interactive candlestick charts with different timeframes."""
    
    # Initialize data provider and visualizer
    print("Initializing data provider and chart visualizer...")
    data_provider = CryptoCompareProvider()
    visualizer = ChartVisualizer(theme="plotly_dark")  # Options: plotly, plotly_white, plotly_dark
    
    # Configuration
    symbol = "BTC"
    currency = "USD"
    
    print(f"\nFetching data for {symbol}/{currency}...")
    
    # Example 1: Single timeframe chart (hourly)
    print("\n" + "="*60)
    print("Example 1: Hourly Candlestick Chart with Volume")
    print("="*60)
    
    df_hourly = data_provider.get_historical_ohlcv(
        symbol=symbol,
        currency=currency,
        timeframe="hour",
        limit=168  # Last 7 days of hourly data
    )
    
    if df_hourly is not None and not df_hourly.empty:
        print(f"✓ Fetched {len(df_hourly)} hourly candles")
        
        # Create candlestick chart with volume
        fig_hourly = visualizer.create_candlestick_chart(
            df=df_hourly,
            symbol=symbol,
            currency=currency,
            timeframe="hour",
            show_volume=True,
            height=800
        )
        
        # Add technical indicators (optional)
        fig_hourly = visualizer.add_technical_indicators(
            fig=fig_hourly,
            df=df_hourly,
            indicators=['SMA_20', 'SMA_50', 'EMA_12']
        )
        
        # Save and display
        visualizer.save_chart(fig_hourly, "btc_hourly_chart.html")
        print("✓ Chart saved as 'btc_hourly_chart.html'")
        print("  Opening in browser...")
        visualizer.show_chart(fig_hourly)
    else:
        print("✗ Failed to fetch hourly data")
    
    # Example 2: Multi-timeframe chart with dropdown selector
    print("\n" + "="*60)
    print("Example 2: Multi-Timeframe Chart (Hour/Day)")
    print("="*60)
    
    # Fetch multiple timeframes
    timeframes_data = data_provider.get_ohlcv_multi_timeframe(
        symbol=symbol,
        currency=currency,
        timeframes=['hour', 'day']
    )
    
    if timeframes_data:
        print(f"✓ Fetched data for timeframes: {list(timeframes_data.keys())}")
        
        # Note: For multi-timeframe with dropdown, we create separate charts
        # as plotly's dropdown works better with single-timeframe views
        for tf, df in timeframes_data.items():
            print(f"  - {tf}: {len(df)} candles")
    else:
        print("✗ Failed to fetch multi-timeframe data")
    
    # Example 3: Daily chart for longer period
    print("\n" + "="*60)
    print("Example 3: Daily Candlestick Chart (3 months)")
    print("="*60)
    
    df_daily = data_provider.get_historical_ohlcv(
        symbol=symbol,
        currency=currency,
        timeframe="day",
        limit=90  # Last 3 months
    )
    
    if df_daily is not None and not df_daily.empty:
        print(f"✓ Fetched {len(df_daily)} daily candles")
        
        fig_daily = visualizer.create_candlestick_chart(
            df=df_daily,
            symbol=symbol,
            currency=currency,
            timeframe="day",
            show_volume=True,
            height=800
        )
        
        # Add moving averages
        fig_daily = visualizer.add_technical_indicators(
            fig=fig_daily,
            df=df_daily,
            indicators=['SMA_20', 'SMA_50', 'EMA_20']
        )
        
        visualizer.save_chart(fig_daily, "btc_daily_chart.html")
        print("✓ Chart saved as 'btc_daily_chart.html'")
        print("  Opening in browser...")
        visualizer.show_chart(fig_daily)
    else:
        print("✗ Failed to fetch daily data")
    
    # Example 4: Minute chart for short-term trading
    print("\n" + "="*60)
    print("Example 4: Minute Candlestick Chart (Last 6 hours)")
    print("="*60)
    
    df_minute = data_provider.get_historical_ohlcv(
        symbol=symbol,
        currency=currency,
        timeframe="minute",
        limit=360  # Last 6 hours of minute data
    )
    
    if df_minute is not None and not df_minute.empty:
        print(f"✓ Fetched {len(df_minute)} minute candles")
        
        fig_minute = visualizer.create_candlestick_chart(
            df=df_minute,
            symbol=symbol,
            currency=currency,
            timeframe="minute",
            show_volume=True,
            height=800
        )
        
        visualizer.save_chart(fig_minute, "btc_minute_chart.html")
        print("✓ Chart saved as 'btc_minute_chart.html'")
        print("  Opening in browser...")
        visualizer.show_chart(fig_minute)
    else:
        print("✗ Failed to fetch minute data")
    
    print("\n" + "="*60)
    print("Chart Features:")
    print("="*60)
    print("✓ Interactive zoom and pan")
    print("✓ Hover for detailed OHLCV data")
    print("✓ Time range selector buttons (1h, 6h, 12h, 1d, 1w, 1m, All)")
    print("✓ Volume subplot with color-coded bars")
    print("✓ Technical indicators (SMA, EMA)")
    print("✓ Responsive design")
    print("="*60)


if __name__ == "__main__":
    main()
