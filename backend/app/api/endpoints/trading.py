from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.trade import Trade
from app.services.trading import TradingService
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

class TradeRequest(BaseModel):
    symbol: str
    action: str  # "buy" or "sell"
    quantity: int
    order_type: str = "market"  # "market" or "limit"
    limit_price: Optional[float] = None

class PositionResponse(BaseModel):
    symbol: str
    quantity: int
    avg_price: float
    current_price: float
    unrealized_pnl: float
    market_value: float

@router.post("/execute")
async def execute_trade(trade_request: TradeRequest, db: Session = Depends(get_db)):
    """Execute a trade"""
    try:
        trading_service = TradingService(db)
        result = await trading_service.execute_trade(
            symbol=trade_request.symbol,
            action=trade_request.action,
            quantity=trade_request.quantity,
            order_type=trade_request.order_type,
            limit_price=trade_request.limit_price
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/positions")
async def get_positions(db: Session = Depends(get_db)):
    """Get current positions"""
    try:
        trading_service = TradingService(db)
        positions = await trading_service.get_positions()
        return {"positions": positions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trades")
async def get_trade_history(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get trade history"""
    try:
        trades = db.query(Trade).order_by(Trade.timestamp.desc()).offset(offset).limit(limit).all()
        
        trade_list = []
        for trade in trades:
            trade_list.append({
                "id": trade.id,
                "symbol": trade.symbol,
                "action": trade.action,
                "quantity": trade.quantity,
                "price": trade.price,
                "timestamp": trade.timestamp.isoformat(),
                "pnl": trade.pnl,
                "status": trade.status
            })
        
        return {
            "trades": trade_list,
            "total": db.query(Trade).count()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/portfolio")
async def get_portfolio_summary(db: Session = Depends(get_db)):
    """Get portfolio summary"""
    try:
        trading_service = TradingService(db)
        summary = await trading_service.get_portfolio_summary()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/position/{symbol}")
async def close_position(symbol: str, db: Session = Depends(get_db)):
    """Close a position"""
    try:
        trading_service = TradingService(db)
        result = await trading_service.close_position(symbol)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))