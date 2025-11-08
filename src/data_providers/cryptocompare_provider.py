"""CryptoCompare API data provider implementation."""
import cryptocompare
from typing import Dict, Optional, List
from datetime import datetime
import pandas as pd
from .base_provider import BaseDataProvider


class CryptoCompareProvider(BaseDataProvider):
    """Data provider using CryptoCompare library."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize CryptoCompare provider.
        
        Args:
            api_key: Optional API key for higher rate limits
        """
        if api_key:
            cryptocompare.cryptocompare._set_api_key_parameter(api_key)
    
    def get_current_price(self, symbol: str, currency: str = "USD") -> Optional[float]:
        """
        Get current price from CryptoCompare.
        
        Args:
            symbol: Crypto symbol (e.g., 'BTC', 'ETH')
            currency: Quote currency (default: 'USD')
            
        Returns:
            Current price or None if request fails
        """
        try:
            price_data = cryptocompare.get_price(symbol.upper(), currency=currency.upper())
            if price_data and symbol.upper() in price_data:
                return float(price_data[symbol.upper()][currency.upper()])
            return None
        except Exception as e:
            print(f"Error fetching price for {symbol}/{currency}: {e}")
            return None
    
    def get_market_data(self, symbol: str, currency: str = "USD") -> Optional[Dict]:
        """
        Get comprehensive market data from CryptoCompare.
        
        Args:
            symbol: Crypto symbol
            currency: Quote currency
            
        Returns:
            Dictionary with price, volume, change data or None
        """
        try:
            # Get current price
            price = self.get_current_price(symbol, currency)
            if price is None:
                return None
            
            # Get historical data for 24h stats
            hist_data = cryptocompare.get_historical_price_day(
                symbol.upper(), 
                currency.upper(), 
                limit=1
            )
            
            if not hist_data:
                return {
                    "symbol": symbol.upper(),
                    "currency": currency.upper(),
                    "price": price,
                    "volume_24h": None,
                    "change_24h": None,
                    "change_pct_24h": None,
                    "high_24h": None,
                    "low_24h": None,
                    "market_cap": None,
                }
            
            latest = hist_data[0] if hist_data else {}
            open_price = latest.get('open', price)
            change_24h = price - open_price if open_price else None
            change_pct_24h = ((price - open_price) / open_price * 100) if open_price else None
            
            return {
                "symbol": symbol.upper(),
                "currency": currency.upper(),
                "price": price,
                "volume_24h": latest.get('volumeto'),
                "change_24h": change_24h,
                "change_pct_24h": change_pct_24h,
                "high_24h": latest.get('high'),
                "low_24h": latest.get('low'),
                "market_cap": None,  # Not directly available in basic API
            }
        except Exception as e:
            print(f"Error fetching market data for {symbol}/{currency}: {e}")
            return None
    
    def get_historical_ohlcv(
        self, 
        symbol: str, 
        currency: str = "USD",
        timeframe: str = "hour",
        limit: int = 100
    ) -> Optional[pd.DataFrame]:
        """
        Get historical OHLCV (Open, High, Low, Close, Volume) data.
        
        Args:
            symbol: Crypto symbol (e.g., 'BTC', 'ETH')
            currency: Quote currency (default: 'USD')
            timeframe: Time interval - 'minute', 'hour', 'day' (default: 'hour')
            limit: Number of data points to fetch (default: 100, max varies by timeframe)
            
        Returns:
            DataFrame with columns: timestamp, open, high, low, close, volume
            or None if request fails
        """
        try:
            symbol_upper = symbol.upper()
            currency_upper = currency.upper()
            
            # Choose appropriate API method based on timeframe
            if timeframe == "minute":
                data = cryptocompare.get_historical_price_minute(
                    symbol_upper, currency_upper, limit=limit
                )
            elif timeframe == "hour":
                data = cryptocompare.get_historical_price_hour(
                    symbol_upper, currency_upper, limit=limit
                )
            elif timeframe == "day":
                data = cryptocompare.get_historical_price_day(
                    symbol_upper, currency_upper, limit=limit
                )
            else:
                print(f"Invalid timeframe: {timeframe}. Use 'minute', 'hour', or 'day'.")
                return None
            
            if not data:
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['time'], unit='s')
            
            # Select and rename relevant columns
            df = df[['timestamp', 'open', 'high', 'low', 'close', 'volumefrom', 'volumeto']]
            df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume_from', 'volume_to']
            
            # Add volume column (using volumeto which is in quote currency)
            df['volume'] = df['volume_to']
            
            return df
            
        except Exception as e:
            print(f"Error fetching historical data for {symbol}/{currency}: {e}")
            return None
    
    def get_ohlcv_multi_timeframe(
        self,
        symbol: str,
        currency: str = "USD",
        timeframes: Optional[List[str]] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Get OHLCV data for multiple timeframes.
        
        Args:
            symbol: Crypto symbol
            currency: Quote currency
            timeframes: List of timeframes (default: ['hour', 'day'])
            
        Returns:
            Dictionary mapping timeframe to DataFrame
        """
        if timeframes is None:
            timeframes = ['hour', 'day']
        
        result = {}
        for tf in timeframes:
            df = self.get_historical_ohlcv(symbol, currency, tf)
            if df is not None:
                result[tf] = df
        
        return result
