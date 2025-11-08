"""Base strategy class for trading strategies."""
from abc import ABC, abstractmethod
from typing import Optional, Dict
from ..data_providers.base_provider import BaseDataProvider
from ..position.position_calculator import PositionCalculator


class BaseStrategy(ABC):
    """Abstract base class for trading strategies."""
    
    def __init__(
        self,
        data_provider: BaseDataProvider,
        position_calculator: PositionCalculator,
        symbol: str = "BTC",
        currency: str = "USD"
    ):
        """
        Initialize base strategy.
        
        Args:
            data_provider: Data provider instance
            position_calculator: Position calculator instance
            symbol: Trading symbol
            currency: Quote currency
        """
        self.data_provider = data_provider
        self.position_calculator = position_calculator
        self.symbol = symbol
        self.currency = currency
    
    def get_current_price(self) -> Optional[float]:
        """
        Get current market price.
        
        Returns:
            Current price or None
        """
        return self.data_provider.get_current_price(self.symbol, self.currency)
    
    def get_market_data(self) -> Optional[Dict]:
        """
        Get comprehensive market data.
        
        Returns:
            Market data dictionary or None
        """
        return self.data_provider.get_market_data(self.symbol, self.currency)
    
    @abstractmethod
    def generate_signal(self) -> Optional[Dict]:
        """
        Generate trading signal based on strategy logic.
        
        Returns:
            Dictionary with signal details or None
            Expected keys: 'action' (BUY/SELL/HOLD), 'stop_loss', 'target'
        """
        pass
    
    @abstractmethod
    def calculate_entry(self) -> Optional[Dict]:
        """
        Calculate entry parameters for a trade.
        
        Returns:
            Dictionary with entry details or None
        """
        pass
    
    def execute_strategy(self) -> Optional[Dict]:
        """
        Execute full strategy workflow.
        
        Returns:
            Complete trade setup or None
        """
        signal = self.generate_signal()
        if signal is None:
            return None
        
        entry = self.calculate_entry()
        if entry is None:
            return None
        
        return {
            "signal": signal,
            "entry": entry,
            "timestamp": self._get_timestamp()
        }
    
    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat()
