from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.ai.trading_ai import TradingAI
from app.services.market_data import MarketDataService
from pydantic import BaseModel
from typing import Dict, List, Optional

router = APIRouter()

class AIAnalysisRequest(BaseModel):
    symbol: str
    timeframe: str = "1d"
    include_news: bool = True

class AIChatRequest(BaseModel):
    message: str
    context: Optional[Dict] = None

@router.post("/analyze")
async def ai_analysis(request: AIAnalysisRequest, db: Session = Depends(get_db)):
    """Get AI analysis for a symbol"""
    try:
        trading_ai = TradingAI()
        analysis = await trading_ai.analyze_symbol(
            symbol=request.symbol,
            timeframe=request.timeframe,
            include_news=request.include_news
        )
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/decision")
async def ai_trading_decision(symbol: str, db: Session = Depends(get_db)):
    """Get AI trading decision for a symbol"""
    try:
        trading_ai = TradingAI()
        decision = await trading_ai.make_trading_decision(symbol)
        return decision
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat")
async def ai_chat(request: AIChatRequest, db: Session = Depends(get_db)):
    """Chat with AI assistant"""
    try:
        trading_ai = TradingAI()
        response = await trading_ai.chat(request.message, request.context)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations")
async def get_ai_recommendations(db: Session = Depends(get_db)):
    """Get AI trading recommendations"""
    try:
        trading_ai = TradingAI()
        recommendations = await trading_ai.get_daily_recommendations()
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sentiment/{symbol}")
async def get_market_sentiment(symbol: str, db: Session = Depends(get_db)):
    """Get market sentiment analysis"""
    try:
        trading_ai = TradingAI()
        sentiment = await trading_ai.analyze_market_sentiment(symbol)
        return sentiment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/auto-trade/toggle")
async def toggle_auto_trading(enabled: bool, db: Session = Depends(get_db)):
    """Enable/disable automatic trading"""
    try:
        trading_ai = TradingAI()
        result = await trading_ai.toggle_auto_trading(enabled)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/auto-trade/status")
async def get_auto_trading_status(db: Session = Depends(get_db)):
    """Get automatic trading status"""
    try:
        trading_ai = TradingAI()
        status = await trading_ai.get_auto_trading_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))