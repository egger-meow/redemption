"""Crypto perpetual trading strategy framework."""
__version__ = "0.1.0"

from .data_providers import BaseDataProvider, CryptoCompareProvider
from .position import PositionCalculator, PositionType
from .strategies import BaseStrategy, SimpleStopLossStrategy
from .visualization import ChartVisualizer

__all__ = [
    "BaseDataProvider",
    "CryptoCompareProvider",
    "PositionCalculator",
    "PositionType",
    "BaseStrategy",
    "SimpleStopLossStrategy",
    "ChartVisualizer",
]
