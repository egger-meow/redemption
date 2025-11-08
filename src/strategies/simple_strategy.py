"""Simple example strategy implementation."""
from typing import Optional, Dict
from .base_strategy import BaseStrategy


class SimpleStopLossStrategy(BaseStrategy):
    """
    Simple strategy that uses user-defined stop loss and target prices.
    Position size is automatically calculated based on max loss amount.
    """
    
    def __init__(
        self,
        data_provider,
        position_calculator,
        stop_loss_price: Optional[float] = None,
        target_price: Optional[float] = None,
        symbol: str = "BTC",
        currency: str = "USD"
    ):
        """
        Initialize simple strategy.
        
        Args:
            data_provider: Data provider instance
            position_calculator: Position calculator instance
            stop_loss_price: User-defined stop loss price (None = auto-calculate 2%)
            target_price: User-defined target price (None = auto-calculate 5%)
            symbol: Trading symbol
            currency: Quote currency
        """
        super().__init__(data_provider, position_calculator, symbol, currency)
        self.stop_loss_price = stop_loss_price
        self.target_price = target_price
    
    def set_levels(self, stop_loss_price: float, target_price: float):
        """
        Update stop loss and target price levels.
        
        Args:
            stop_loss_price: New stop loss price
            target_price: New target price
        """
        self.stop_loss_price = stop_loss_price
        self.target_price = target_price
    
    def generate_signal(self) -> Optional[Dict]:
        """
        Generate a signal with user-defined or auto-calculated price levels.
        
        Returns:
            Signal dictionary with action and price levels
        """
        current_price = self.get_current_price()
        if current_price is None:
            return None
        
        # Use user-defined prices or auto-calculate
        if self.stop_loss_price is not None and self.target_price is not None:
            stop_loss = self.stop_loss_price
            target = self.target_price
        else:
            # Auto-calculate with default percentages if not set
            stop_loss = current_price * 0.98  # 2% stop loss
            target = current_price * 1.05     # 5% target
        
        # Determine action based on stop loss position
        action = "BUY" if current_price > stop_loss else "SELL"
        
        return {
            "action": action,
            "current_price": current_price,
            "stop_loss": stop_loss,
            "target": target,
            "confidence": 0.7
        }
    
    def calculate_entry(self) -> Optional[Dict]:
        """
        Calculate position size based on user's max loss amount and price levels.
        
        Returns:
            Entry details with position sizing
        """
        signal = self.generate_signal()
        if signal is None:
            return None
        
        try:
            position_details = self.position_calculator.calculate_position_size(
                current_price=signal["current_price"],
                stop_loss=signal["stop_loss"],
                target_price=signal["target"]
            )
            
            return {
                **position_details,
                "action": signal["action"],
                "confidence": signal.get("confidence", 0.0)
            }
        except Exception as e:
            print(f"Error calculating entry: {e}")
            return None
