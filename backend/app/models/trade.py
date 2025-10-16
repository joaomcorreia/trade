from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.sql import func
from app.core.database import Base

class Trade(Base):
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), nullable=False, index=True)
    action = Column(String(4), nullable=False)  # "buy" or "sell"
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    order_type = Column(String(10), default="market")  # "market" or "limit"
    status = Column(String(20), default="executed")  # "pending", "executed", "cancelled"
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    pnl = Column(Float, default=0.0)  # Profit and Loss
    fees = Column(Float, default=0.0)
    notes = Column(Text)
    ai_decision = Column(Boolean, default=False)  # True if trade was made by AI
    confidence_score = Column(Float)  # AI confidence in the trade
    
    def __repr__(self):
        return f"<Trade(symbol={self.symbol}, action={self.action}, quantity={self.quantity}, price={self.price})>"