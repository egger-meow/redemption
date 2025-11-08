"""Configuration settings for the trading system."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for trading parameters."""
    
    # API Configuration
    CRYPTOCOMPARE_API_KEY = os.getenv("CRYPTOCOMPARE_API_KEY", None)
    
    # Trading Configuration
    DEFAULT_SYMBOL = os.getenv("DEFAULT_SYMBOL", "BTC")
    DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "USD")
    
    # Risk Management
    MAX_LOSS_AMOUNT = float(os.getenv("MAX_LOSS_AMOUNT", "300"))
    DEFAULT_STOP_LOSS_PCT = float(os.getenv("DEFAULT_STOP_LOSS_PCT", "0.02"))  # 2%
    DEFAULT_TARGET_PCT = float(os.getenv("DEFAULT_TARGET_PCT", "0.05"))  # 5%
    
    @classmethod
    def validate(cls):
        """Validate configuration settings."""
        if cls.MAX_LOSS_AMOUNT <= 0:
            raise ValueError("MAX_LOSS_AMOUNT must be positive")
        
        if not (0 < cls.DEFAULT_STOP_LOSS_PCT < 1):
            raise ValueError("DEFAULT_STOP_LOSS_PCT must be between 0 and 1")
        
        if not (0 < cls.DEFAULT_TARGET_PCT < 1):
            raise ValueError("DEFAULT_TARGET_PCT must be between 0 and 1")
        
        return True
