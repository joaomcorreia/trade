from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.market_data import MarketDataService
from app.services.analysis import AnalysisService
from typing import Dict, List, Optional

router = APIRouter()

@router.get("/technical/{symbol}")
async def get_technical_analysis(
    symbol: str,
    period: str = "1y",
    db: Session = Depends(get_db)
):
    """Get comprehensive technical analysis"""
    try:
        analysis_service = AnalysisService()
        technical_analysis = await analysis_service.get_technical_analysis(symbol, period)
        return technical_analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/fundamental/{symbol}")
async def get_fundamental_analysis(symbol: str, db: Session = Depends(get_db)):
    """Get fundamental analysis"""
    try:
        analysis_service = AnalysisService()
        fundamental_analysis = await analysis_service.get_fundamental_analysis(symbol)
        return fundamental_analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/risk/{symbol}")
async def get_risk_analysis(symbol: str, db: Session = Depends(get_db)):
    """Get risk analysis for a symbol"""
    try:
        analysis_service = AnalysisService()
        risk_analysis = await analysis_service.get_risk_analysis(symbol)
        return risk_analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/correlation")
async def get_correlation_analysis(
    symbols: str,  # comma-separated symbols
    period: str = "1y",
    db: Session = Depends(get_db)
):
    """Get correlation analysis between symbols"""
    try:
        symbol_list = [s.strip().upper() for s in symbols.split(",")]
        analysis_service = AnalysisService()
        correlation = await analysis_service.get_correlation_analysis(symbol_list, period)
        return correlation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/screener")
async def stock_screener(
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_volume: Optional[int] = None,
    rsi_oversold: bool = False,
    rsi_overbought: bool = False,
    db: Session = Depends(get_db)
):
    """Screen stocks based on criteria"""
    try:
        analysis_service = AnalysisService()
        results = await analysis_service.screen_stocks({
            "min_price": min_price,
            "max_price": max_price,
            "min_volume": min_volume,
            "rsi_oversold": rsi_oversold,
            "rsi_overbought": rsi_overbought
        })
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))