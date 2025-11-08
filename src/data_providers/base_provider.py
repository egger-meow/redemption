"""Base data provider interface for crypto price data."""
from abc import ABC, abstractmethod
from typing import Dict, Optional


class BaseDataProvider(ABC):
    """Abstract base class for data providers."""
    
    @abstractmethod
    def get_current_price(self, symbol: str, currency: str = "USD") -> Optional[float]:
        """
        Get current price for a symbol.
        
        Args:
            symbol: Trading symbol (e.g., 'BTC', 'ETH')
            currency: Quote currency (default: 'USD')
            
        Returns:
            Current price or None if unavailable
        """
        pass
    
    @abstractmethod
    def get_market_data(self, symbol: str, currency: str = "USD") -> Optional[Dict]:
        """
        Get comprehensive market data.
        
        Args:
            symbol: Trading symbol
            currency: Quote currency
            
        Returns:
            Dictionary with market data or None
        """
        pass
