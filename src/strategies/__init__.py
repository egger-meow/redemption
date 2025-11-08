"""Trading strategies for perpetual futures."""
from .base_strategy import BaseStrategy
from .simple_strategy import SimpleStopLossStrategy

__all__ = ["BaseStrategy", "SimpleStopLossStrategy"]
