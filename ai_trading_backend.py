"""
AI Trading Backend
A FastAPI-based trading system with AI analysis capabilities
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
import asyncio
import random
import time
from datetime import datetime, timedelta
import json

app = FastAPI(title="AI Trading Backend", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class TradeSignal(BaseModel):
    symbol: str
    action: str  # 'buy' or 'sell'
    confidence: float
    price: float
    timestamp: datetime

class Position(BaseModel):
    symbol: str
    quantity: int
    entry_price: float
    current_price: float
    pnl: float
    pnl_percent: float

class TradingStatus(BaseModel):
    is_active: bool
    total_positions: int
    portfolio_value: float
    today_pnl: float
    ai_confidence: float

# Global state
trading_active = True
positions = [
    Position(symbol="AAPL", quantity=100, entry_price=175.50, current_price=182.30, pnl=680.00, pnl_percent=3.87),
    Position(symbol="GOOGL", quantity=50, entry_price=2380.00, current_price=2420.50, pnl=2025.00, pnl_percent=1.70),
    Position(symbol="MSFT", quantity=75, entry_price=335.20, current_price=331.80, pnl=-255.00, pnl_percent=-1.01),
]

# AI Trading Functions
def generate_ai_signal() -> TradeSignal:
    """Generate a random AI trading signal for demo purposes"""
    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "NVDA", "META"]
    actions = ["buy", "sell"]
    
    symbol = random.choice(symbols)
    action = random.choice(actions)
    confidence = random.uniform(0.6, 0.95)
    price = random.uniform(100, 3000)
    
    return TradeSignal(
        symbol=symbol,
        action=action,
        confidence=confidence,
        price=price,
        timestamp=datetime.now()
    )

def calculate_rsi(prices: List[float], period: int = 14) -> float:
    """Calculate RSI indicator"""
    if len(prices) < period:
        return 50.0
    
    gains = []
    losses = []
    
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100.0
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def analyze_market_sentiment() -> Dict:
    """Analyze current market sentiment"""
    sentiment_score = random.uniform(-1, 1)
    
    if sentiment_score > 0.3:
        sentiment = "Bullish"
    elif sentiment_score < -0.3:
        sentiment = "Bearish"
    else:
        sentiment = "Neutral"
    
    return {
        "sentiment": sentiment,
        "score": sentiment_score,
        "confidence": random.uniform(0.7, 0.95),
        "factors": ["Technical indicators", "News sentiment", "Market volume"]
    }

# API Endpoints
@app.get("/")
async def root():
    return {"message": "AI Trading Backend API", "status": "active", "timestamp": datetime.now()}

@app.get("/api/v1/trading/status")
async def get_trading_status():
    """Get current trading status"""
    portfolio_value = sum(pos.quantity * pos.current_price for pos in positions)
    today_pnl = sum(pos.pnl for pos in positions)
    
    return TradingStatus(
        is_active=trading_active,
        total_positions=len(positions),
        portfolio_value=portfolio_value,
        today_pnl=today_pnl,
        ai_confidence=random.uniform(0.75, 0.95)
    )

@app.get("/api/v1/trading/positions")
async def get_positions():
    """Get current positions"""
    # Update current prices with small random changes
    for pos in positions:
        change_percent = random.uniform(-0.02, 0.02)
        pos.current_price = pos.current_price * (1 + change_percent)
        pos.pnl = (pos.current_price - pos.entry_price) * pos.quantity
        pos.pnl_percent = (pos.current_price - pos.entry_price) / pos.entry_price * 100
    
    return {"positions": positions}

@app.get("/api/v1/trading/ai-signals")
async def get_ai_signals():
    """Get latest AI trading signals"""
    signals = [generate_ai_signal() for _ in range(3)]
    return {"signals": signals}

@app.get("/api/v1/trading/ai-analysis")
async def get_ai_analysis():
    """Get AI market analysis"""
    market_sentiment = analyze_market_sentiment()
    
    # Generate random technical indicators
    rsi = random.uniform(20, 80)
    macd = random.uniform(-2, 2)
    
    analysis = {
        "market_sentiment": market_sentiment,
        "technical_indicators": {
            "rsi": rsi,
            "macd": macd,
            "moving_average_20": random.uniform(150, 200),
            "moving_average_50": random.uniform(140, 190)
        },
        "recommendations": [],
        "risk_level": "medium",
        "confidence": random.uniform(0.8, 0.95),
        "timestamp": datetime.now()
    }
    
    # Generate recommendations based on indicators
    if rsi < 30:
        analysis["recommendations"].append("RSI indicates oversold conditions - consider buying")
    elif rsi > 70:
        analysis["recommendations"].append("RSI indicates overbought conditions - consider selling")
    
    if macd > 0:
        analysis["recommendations"].append("MACD bullish signal")
    else:
        analysis["recommendations"].append("MACD bearish signal")
    
    return analysis

@app.post("/api/v1/trading/execute")
async def execute_trade(symbol: str, action: str, quantity: int):
    """Execute a manual trade"""
    if not trading_active:
        raise HTTPException(status_code=400, detail="Trading is currently disabled")
    
    # Simulate trade execution
    execution_price = random.uniform(100, 3000)
    
    trade_result = {
        "symbol": symbol,
        "action": action,
        "quantity": quantity,
        "execution_price": execution_price,
        "timestamp": datetime.now(),
        "status": "executed"
    }
    
    return trade_result

@app.post("/api/v1/trading/toggle")
async def toggle_trading():
    """Toggle trading on/off"""
    global trading_active
    trading_active = not trading_active
    
    return {
        "trading_active": trading_active,
        "message": f"Trading {'enabled' if trading_active else 'disabled'}",
        "timestamp": datetime.now()
    }

@app.get("/api/v1/market/price/{symbol}")
async def get_market_price(symbol: str):
    """Get current market price for a symbol"""
    # Simulate market data
    base_prices = {
        "AAPL": 182.30,
        "GOOGL": 2420.50,
        "MSFT": 331.80,
        "TSLA": 248.50,
        "AMZN": 3180.20,
        "NVDA": 875.30,
        "META": 485.60
    }
    
    base_price = base_prices.get(symbol, 100.0)
    current_price = base_price * (1 + random.uniform(-0.05, 0.05))
    
    return {
        "symbol": symbol,
        "price": round(current_price, 2),
        "change": round(current_price - base_price, 2),
        "change_percent": round((current_price - base_price) / base_price * 100, 2),
        "timestamp": datetime.now()
    }

@app.get("/api/v1/symbols/commodities")
async def get_commodities():
    """Get available commodity symbols"""
    commodities = [
        {"symbol": "Gold", "name": "Gold Spot", "price": 2045.30},
        {"symbol": "Silver", "name": "Silver Spot", "price": 24.85},
        {"symbol": "Oil", "name": "Crude Oil WTI", "price": 78.45},
        {"symbol": "Gas", "name": "Natural Gas", "price": 2.65}
    ]
    return {"commodities": commodities}

@app.get("/api/v1/categories")
async def get_categories():
    """Get trading categories"""
    categories = [
        {"id": 1, "name": "Stocks", "count": 150},
        {"id": 2, "name": "Crypto", "count": 50},
        {"id": 3, "name": "Commodities", "count": 25},
        {"id": 4, "name": "Forex", "count": 30}
    ]
    return {"categories": categories}

if __name__ == "__main__":
    print("Starting AI Trading Backend...")
    print("Dashboard: http://localhost:3000")
    print("API Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)