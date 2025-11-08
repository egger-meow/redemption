"""Interactive candlestick chart visualizer with volume subplot."""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Optional, Dict, List
from datetime import datetime


class ChartVisualizer:
    """Create interactive candlestick charts with volume data."""
    
    def __init__(self, theme: str = "plotly_dark"):
        """
        Initialize chart visualizer.
        
        Args:
            theme: Plotly theme ('plotly', 'plotly_white', 'plotly_dark', 'ggplot2', 'seaborn', etc.)
        """
        self.theme = theme
        self.default_colors = {
            'increasing': '#26a69a',  # Green for bullish candles
            'decreasing': '#ef5350',  # Red for bearish candles
            'volume_increasing': 'rgba(38, 166, 154, 0.5)',
            'volume_decreasing': 'rgba(239, 83, 80, 0.5)'
        }
    
    def create_candlestick_chart(
        self,
        df: pd.DataFrame,
        symbol: str,
        currency: str = "USD",
        timeframe: str = "hour",
        title: Optional[str] = None,
        show_volume: bool = True,
        height: int = 800,
        width: Optional[int] = None
    ) -> go.Figure:
        """
        Create an interactive candlestick chart with optional volume subplot.
        
        Args:
            df: DataFrame with columns: timestamp, open, high, low, close, volume
            symbol: Trading symbol (e.g., 'BTC')
            currency: Quote currency (e.g., 'USD')
            timeframe: Time interval ('minute', 'hour', 'day')
            title: Custom chart title (optional)
            show_volume: Whether to show volume subplot (default: True)
            height: Chart height in pixels (default: 800)
            width: Chart width in pixels (optional, auto if None)
            
        Returns:
            Plotly figure object
        """
        if df is None or df.empty:
            raise ValueError("DataFrame is empty or None")
        
        # Ensure required columns exist
        required_cols = ['timestamp', 'open', 'high', 'low', 'close']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"DataFrame must contain columns: {required_cols}")
        
        # Create subplots
        if show_volume and 'volume' in df.columns:
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.03,
                row_heights=[0.7, 0.3],
                subplot_titles=(f'{symbol}/{currency} Price', 'Volume')
            )
        else:
            fig = make_subplots(rows=1, cols=1)
        
        # Add candlestick chart
        candlestick = go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Price',
            increasing_line_color=self.default_colors['increasing'],
            decreasing_line_color=self.default_colors['decreasing'],
            increasing_fillcolor=self.default_colors['increasing'],
            decreasing_fillcolor=self.default_colors['decreasing']
        )
        
        fig.add_trace(candlestick, row=1, col=1)
        
        # Add volume bars if requested
        if show_volume and 'volume' in df.columns:
            # Color volume bars based on price change
            colors = []
            for i in range(len(df)):
                if df['close'].iloc[i] >= df['open'].iloc[i]:
                    colors.append(self.default_colors['volume_increasing'])
                else:
                    colors.append(self.default_colors['volume_decreasing'])
            
            volume_bars = go.Bar(
                x=df['timestamp'],
                y=df['volume'],
                name='Volume',
                marker_color=colors,
                showlegend=False
            )
            
            fig.add_trace(volume_bars, row=2, col=1)
        
        # Set title
        if title is None:
            title = f"{symbol}/{currency} - {timeframe.capitalize()} Chart"
        
        # Update layout
        layout_config = {
            'title': {
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            'xaxis': {
                'title': 'Time',
                'rangeslider': {'visible': False},
                'type': 'date'
            },
            'yaxis': {
                'title': f'Price ({currency})',
                'side': 'right'
            },
            'hovermode': 'x unified',
            'template': self.theme,
            'height': height,
            'showlegend': True,
            'legend': {
                'orientation': 'h',
                'yanchor': 'bottom',
                'y': 1.02,
                'xanchor': 'right',
                'x': 1
            }
        }
        
        if width:
            layout_config['width'] = width
        
        # Add volume y-axis if applicable
        if show_volume and 'volume' in df.columns:
            layout_config['yaxis2'] = {
                'title': f'Volume ({currency})',
                'side': 'right'
            }
            layout_config['xaxis2'] = {
                'title': 'Time'
            }
        
        fig.update_layout(**layout_config)
        
        # Add range selector buttons
        fig.update_xaxes(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1h", step="hour", stepmode="backward"),
                    dict(count=6, label="6h", step="hour", stepmode="backward"),
                    dict(count=12, label="12h", step="hour", stepmode="backward"),
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(step="all", label="All")
                ]),
                bgcolor="rgba(150, 150, 150, 0.1)",
                activecolor="rgba(100, 100, 100, 0.3)",
            ),
            row=1, col=1
        )
        
        return fig
    
    def create_multi_timeframe_chart(
        self,
        data_dict: Dict[str, pd.DataFrame],
        symbol: str,
        currency: str = "USD",
        default_timeframe: str = "hour"
    ) -> go.Figure:
        """
        Create a chart with dropdown to switch between timeframes.
        
        Args:
            data_dict: Dictionary mapping timeframe names to DataFrames
            symbol: Trading symbol
            currency: Quote currency
            default_timeframe: Initial timeframe to display
            
        Returns:
            Plotly figure with timeframe selector dropdown
        """
        if not data_dict:
            raise ValueError("data_dict is empty")
        
        # Use default timeframe or first available
        if default_timeframe not in data_dict:
            default_timeframe = list(data_dict.keys())[0]
        
        # Create initial chart
        fig = self.create_candlestick_chart(
            df=data_dict[default_timeframe],
            symbol=symbol,
            currency=currency,
            timeframe=default_timeframe,
            show_volume=True
        )
        
        # Create buttons for timeframe selection
        buttons = []
        for tf_name, df in data_dict.items():
            # Determine visibility for each trace
            visible_states = []
            for trace_tf in data_dict.keys():
                if trace_tf == tf_name:
                    visible_states.extend([True, True])  # candlestick + volume
                else:
                    visible_states.extend([False, False])
            
            button = dict(
                label=tf_name.upper(),
                method="update",
                args=[
                    {"visible": visible_states},
                    {"title": f"{symbol}/{currency} - {tf_name.capitalize()} Chart"}
                ]
            )
            buttons.append(button)
        
        # Add all timeframe data as traces (initially hidden)
        for i, (tf_name, df) in enumerate(data_dict.items()):
            if tf_name == default_timeframe:
                continue  # Already added
            
            temp_fig = self.create_candlestick_chart(
                df=df,
                symbol=symbol,
                currency=currency,
                timeframe=tf_name,
                show_volume=True
            )
            
            for trace in temp_fig.data:
                trace.visible = False
                fig.add_trace(trace)
        
        # Add dropdown menu
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=buttons,
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.11,
                    xanchor="left",
                    y=1.15,
                    yanchor="top",
                    bgcolor="rgba(150, 150, 150, 0.1)",
                    bordercolor="rgba(200, 200, 200, 0.5)",
                    font=dict(size=12)
                )
            ]
        )
        
        return fig
    
    def add_technical_indicators(
        self,
        fig: go.Figure,
        df: pd.DataFrame,
        indicators: Optional[List[str]] = None
    ) -> go.Figure:
        """
        Add technical indicators to an existing chart.
        
        Args:
            fig: Existing Plotly figure
            df: DataFrame with OHLCV data
            indicators: List of indicators to add (e.g., ['SMA_20', 'EMA_50'])
            
        Returns:
            Updated figure with indicators
        """
        if indicators is None:
            indicators = []
        
        for indicator in indicators:
            if indicator.startswith('SMA_'):
                period = int(indicator.split('_')[1])
                df[f'SMA_{period}'] = df['close'].rolling(window=period).mean()
                
                fig.add_trace(
                    go.Scatter(
                        x=df['timestamp'],
                        y=df[f'SMA_{period}'],
                        name=f'SMA {period}',
                        line=dict(width=1.5)
                    ),
                    row=1, col=1
                )
            
            elif indicator.startswith('EMA_'):
                period = int(indicator.split('_')[1])
                df[f'EMA_{period}'] = df['close'].ewm(span=period, adjust=False).mean()
                
                fig.add_trace(
                    go.Scatter(
                        x=df['timestamp'],
                        y=df[f'EMA_{period}'],
                        name=f'EMA {period}',
                        line=dict(width=1.5, dash='dash')
                    ),
                    row=1, col=1
                )
        
        return fig
    
    def save_chart(
        self,
        fig: go.Figure,
        filename: str,
        format: str = "html"
    ) -> None:
        """
        Save chart to file.
        
        Args:
            fig: Plotly figure to save
            filename: Output filename
            format: Output format ('html', 'png', 'jpg', 'svg', 'pdf')
        """
        if format == "html":
            fig.write_html(filename)
        else:
            fig.write_image(filename, format=format)
        
        print(f"Chart saved to: {filename}")
    
    def show_chart(self, fig: go.Figure) -> None:
        """
        Display chart in browser.
        
        Args:
            fig: Plotly figure to display
        """
        fig.show()
