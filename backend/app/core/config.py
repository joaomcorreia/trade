import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    alpha_vantage_api_key: Optional[str] = None
    news_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    
    # Database
    database_url: str = "sqlite:///./trading.db"
    
    # Trading Configuration
    trading_mode: str = "paper"  # paper or live
    default_position_size: float = 1000.0
    max_risk_per_trade: float = 0.02
    stop_loss_percentage: float = 0.05
    
    # Technical Indicators
    rsi_period: int = 14
    rsi_overbought: int = 70
    rsi_oversold: int = 30
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9
    
    # News Analysis
    news_sentiment_threshold: float = 0.1
    news_update_interval: int = 300  # seconds
    
    # AI Configuration
    ai_confidence_threshold: float = 0.75
    ai_trading_enabled: bool = False
    ai_max_trades_per_day: int = 10
    
    class Config:
        env_file = ".env"

settings = Settings()