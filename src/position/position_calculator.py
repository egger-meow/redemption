"""Position sizing calculator for perpetual trading."""
from enum import Enum
from typing import Optional


class PositionType(Enum):
    """Position direction types."""
    LONG = "LONG"
    SHORT = "SHORT"


class PositionCalculator:
    """Calculate position size based on risk parameters."""
    
    def __init__(self, max_loss_amount: float):
        """
        Initialize position calculator.
        
        Args:
            max_loss_amount: Maximum amount willing to lose per trade
        """
        self.max_loss_amount = max_loss_amount
    
    def determine_position_type(
        self, 
        current_price: float, 
        stop_loss: float
    ) -> PositionType:
        """
        Determine if position should be LONG or SHORT.
        
        Args:
            current_price: Current market price
            stop_loss: Stop loss price
            
        Returns:
            PositionType.LONG or PositionType.SHORT
        """
        return PositionType.LONG if current_price > stop_loss else PositionType.SHORT
    
    def calculate_position_size(
        self,
        current_price: float,
        stop_loss: float,
        target_price: float,
        position_type: Optional[PositionType] = None
    ) -> dict:
        """
        Calculate position size based on risk parameters.
        
        Args:
            current_price: Current market price
            stop_loss: Stop loss price
            target_price: Target profit price
            position_type: Optional position type (auto-determined if None)
            
        Returns:
            Dictionary with position details
        """
        if position_type is None:
            position_type = self.determine_position_type(current_price, stop_loss)
        
        # Calculate position size based on risk
        if position_type == PositionType.LONG:
            risk_per_unit = abs(current_price - stop_loss)
            potential_profit = abs(target_price - current_price)
        else:  # SHORT
            risk_per_unit = abs(stop_loss - current_price)
            potential_profit = abs(current_price - target_price)
        
        if risk_per_unit == 0:
            raise ValueError("Stop loss cannot equal current price")
        
        # Position size = max loss / risk per unit
        position_size = self.max_loss_amount / risk_per_unit
        
        # Calculate risk/reward ratio
        risk_reward_ratio = potential_profit / risk_per_unit if risk_per_unit > 0 else 0
        
        # Calculate potential profit/loss
        potential_loss = position_size * risk_per_unit
        potential_profit_amount = position_size * potential_profit
        
        return {
            "position_type": position_type.value,
            "position_size": position_size,
            "current_price": current_price,
            "stop_loss": stop_loss,
            "target_price": target_price,
            "risk_per_unit": risk_per_unit,
            "potential_loss": potential_loss,
            "potential_profit": potential_profit_amount,
            "risk_reward_ratio": risk_reward_ratio,
            "entry_cost": position_size * current_price
        }
    
    def update_max_loss(self, new_max_loss: float):
        """
        Update maximum loss amount.
        
        Args:
            new_max_loss: New maximum loss amount
        """
        if new_max_loss <= 0:
            raise ValueError("Max loss must be positive")
        self.max_loss_amount = new_max_loss
