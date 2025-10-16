from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.market_data import MarketDataService
from typing import List, Optional
import asyncio

router = APIRouter()

@router.get("/price/{symbol}")
async def get_current_price(symbol: str, db: Session = Depends(get_db)):
    """Get current price for a symbol"""
    try:
        market_service = MarketDataService()
        price_data = await market_service.get_current_price(symbol)
        return price_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/historical/{symbol}")
async def get_historical_data(
    symbol: str,
    period: str = "1y",
    interval: str = "1d",
    db: Session = Depends(get_db)
):
    """Get historical price data"""
    try:
        market_service = MarketDataService()
        historical_data = await market_service.get_historical_data(symbol, period, interval)
        return historical_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/indicators/{symbol}")
async def get_technical_indicators(
    symbol: str,
    period: str = "1y",
    db: Session = Depends(get_db)
):
    """Get technical indicators (RSI, MACD, Volume)"""
    try:
        market_service = MarketDataService()
        indicators = await market_service.get_technical_indicators(symbol, period)
        return indicators
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/watchlist")
async def get_watchlist(db: Session = Depends(get_db)):
    """Get user's watchlist"""
    # Default watchlist for demo
    watchlist = [
        "AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", 
        "NVDA", "META", "NFLX", "AMD", "CRM"
    ]
    
    try:
        market_service = MarketDataService()
        watchlist_data = []
        
        for symbol in watchlist:
            price_data = await market_service.get_current_price(symbol)
            watchlist_data.append({
                "symbol": symbol,
                **price_data
            })
        
        return {"watchlist": watchlist_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/news/{symbol}")
async def get_market_news(symbol: str, db: Session = Depends(get_db)):
    """Get news for a specific symbol"""
    try:
        market_service = MarketDataService()
        news_data = await market_service.get_market_news(symbol)
        return news_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))