"""Quick Demo: Generate a Bitcoin K線圖 (Candlestick Chart) in 5 lines."""
from src import CryptoCompareProvider, ChartVisualizer

# 1. Initialize
provider = CryptoCompareProvider()
visualizer = ChartVisualizer(theme="plotly_dark")

# 2. Fetch data (last 7 days, hourly)
print("Fetching BTC/USD data...")
df = provider.get_historical_ohlcv(symbol="BTC", currency="USD", timeframe="hour", limit=168)

if df is not None and not df.empty:
    print(f"✓ Fetched {len(df)} candles")
    
    # 3. Create chart with volume
    print("Creating interactive chart...")
    fig = visualizer.create_candlestick_chart(
        df=df, 
        symbol="BTC", 
        currency="USD", 
        timeframe="hour",
        show_volume=True
    )
    
    # 4. Add moving averages
    print("Adding technical indicators...")
    fig = visualizer.add_technical_indicators(
        fig=fig,
        df=df,
        indicators=['SMA_20', 'SMA_50']
    )
    
    # 5. Save and display
    print("Saving chart...")
    visualizer.save_chart(fig, "btc_quick_demo.html")
    
    print("\n" + "="*60)
    print("✓ Chart created: btc_quick_demo.html")
    print("  Opening in browser...")
    print("="*60)
    print("\nChart Features:")
    print("  • Zoom: Scroll or use zoom button")
    print("  • Pan: Click and drag")
    print("  • Hover: See detailed OHLCV data")
    print("  • Time ranges: Use buttons (1h, 6h, 12h, etc.)")
    print("  • Export: Download button in top-right")
    print("="*60 + "\n")
    
    visualizer.show_chart(fig)
else:
    print("✗ Failed to fetch data. Check your internet connection.")
