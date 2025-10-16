from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class Portfolio(Base):
    __tablename__ = "portfolio"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), nullable=False, unique=True, index=True)
    quantity = Column(Integer, nullable=False)
    avg_price = Column(Float, nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Portfolio(symbol={self.symbol}, quantity={self.quantity}, avg_price={self.avg_price})>"

class MarketData(Base):
    __tablename__ = "market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    open_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    timeframe = Column(String(5), nullable=False)  # "1m", "5m", "1h", "1d", etc.
    
    def __repr__(self):
        return f"<MarketData(symbol={self.symbol}, timestamp={self.timestamp}, close={self.close_price})>"

class TechnicalIndicators(Base):
    __tablename__ = "technical_indicators"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    rsi = Column(Float)
    macd = Column(Float)
    macd_signal = Column(Float)
    macd_histogram = Column(Float)
    sma_20 = Column(Float)
    sma_50 = Column(Float)
    ema_12 = Column(Float)
    ema_26 = Column(Float)
    bb_upper = Column(Float)
    bb_middle = Column(Float)
    bb_lower = Column(Float)
    volume_sma = Column(Float)
    
    def __repr__(self):
        return f"<TechnicalIndicators(symbol={self.symbol}, timestamp={self.timestamp})>"

class News(Base):
    __tablename__ = "news"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    url = Column(String(1000))
    source = Column(String(100))
    published_at = Column(DateTime(timezone=True))
    sentiment = Column(String(20))  # "positive", "negative", "neutral"
    sentiment_score = Column(Float)  # -1 to 1
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<News(symbol={self.symbol}, title={self.title[:50]}...)>"

class AIDecision(Base):
    __tablename__ = "ai_decisions"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), nullable=False, index=True)
    decision = Column(String(10), nullable=False)  # "buy", "sell", "hold"
    confidence = Column(Float, nullable=False)  # 0 to 1
    reasoning = Column(Text)
    market_data = Column(JSON)  # Store the market data used for decision
    indicators = Column(JSON)  # Store the indicators used
    news_sentiment = Column(Float)  # Overall news sentiment
    executed = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<AIDecision(symbol={self.symbol}, decision={self.decision}, confidence={self.confidence})>"