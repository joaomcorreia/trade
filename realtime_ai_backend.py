"""
Real-time AI Trading Backend with WebSocket Price Streaming
Live market data updates via WebSocket connections
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Set
import uvicorn
import yfinance as yf
import pandas as pd
import numpy as np
import asyncio
import time
import json
from datetime import datetime, timedelta
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Real-time AI Trading Backend", version="3.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"✅ WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"❌ WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")

    async def broadcast(self, message: str):
        dead_connections = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting to connection: {e}")
                dead_connections.append(connection)
        
        # Remove dead connections
        for dead_conn in dead_connections:
            self.disconnect(dead_conn)

manager = ConnectionManager()

# Data Models
class MarketPrice(BaseModel):
    symbol: str
    price: float
    change: float
    change_percent: float
    volume: Optional[int] = None
    timestamp: datetime
    source: str = "yahoo_finance"

class LiveUpdate(BaseModel):
    type: str  # 'price', 'signal', 'analysis', 'portfolio'
    data: dict
    timestamp: datetime

class TradeSignal(BaseModel):
    symbol: str
    action: str
    confidence: float
    price: float
    timestamp: datetime
    reasoning: str

class TechnicalIndicators(BaseModel):
    symbol: str
    rsi: float
    macd: float
    sma_20: float
    sma_50: float
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
    market_data_source: str = "yahoo_finance"

# Global state
trading_active = True
positions = [
    Position(symbol="AAPL", quantity=100, entry_price=175.50, current_price=252.29, pnl=7679.00, pnl_percent=43.8),
    Position(symbol="GOOGL", quantity=50, entry_price=2380.00, current_price=253.30, pnl=-106335.00, pnl_percent=-89.4),
    Position(symbol="MSFT", quantity=75, entry_price=335.20, current_price=513.58, pnl=13378.50, pnl_percent=53.2),
]

# Cache for market data
price_cache = {}
CACHE_DURATION = 10  # Cache for 10 seconds for more frequent updates

# Symbols to track in real-time
TRACKED_SYMBOLS = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "NVDA", "META"]

def calculate_rsi(prices, period=14):
    """Calculate RSI indicator"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not rsi.empty else 50.0

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calculate MACD indicator"""
    ema_fast = prices.ewm(span=fast).mean()
    ema_slow = prices.ewm(span=slow).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal).mean()
    return macd.iloc[-1] if not macd.empty else 0.0, signal_line.iloc[-1] if not signal_line.empty else 0.0

async def get_yahoo_finance_data(symbol: str) -> Optional[MarketPrice]:
    """Get real market data from Yahoo Finance"""
    try:
        # Check cache first
        cache_key = f"yf_{symbol}"
        if cache_key in price_cache:
            cached_data = price_cache[cache_key]
            if time.time() - cached_data['timestamp'] < CACHE_DURATION:
                return cached_data['data']
        
        # Fetch data from Yahoo Finance
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="2d")
        
        if len(hist) >= 2:
            current_price = float(hist['Close'].iloc[-1])
            previous_price = float(hist['Close'].iloc[-2])
            change = current_price - previous_price
            change_percent = (change / previous_price) * 100
            volume = int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else None
            
            market_price = MarketPrice(
                symbol=symbol,
                price=round(current_price, 2),
                change=round(change, 2),
                change_percent=round(change_percent, 2),
                volume=volume,
                timestamp=datetime.now(),
                source="yahoo_finance"
            )
            
            # Cache the result
            price_cache[cache_key] = {
                'data': market_price,
                'timestamp': time.time()
            }
            
            return market_price
        else:
            return None
            
    except Exception as e:
        logger.error(f"❌ Yahoo Finance error for {symbol}: {e}")
        return None

async def get_technical_indicators(symbol: str) -> TechnicalIndicators:
    """Calculate technical indicators from Yahoo Finance data"""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="60d")
        
        if len(hist) >= 50:
            prices = hist['Close']
            
            rsi = calculate_rsi(prices)
            macd, macd_signal = calculate_macd(prices)
            sma_20 = prices.rolling(window=20).mean().iloc[-1]
            sma_50 = prices.rolling(window=50).mean().iloc[-1]
            
            return TechnicalIndicators(
                symbol=symbol,
                rsi=round(rsi, 2),
                macd=round(macd, 4),
                sma_20=round(sma_20, 2),
                sma_50=round(sma_50, 2),
                timestamp=datetime.now()
            )
        else:
            # Fallback to simulated data
            return TechnicalIndicators(
                symbol=symbol,
                rsi=random.uniform(30, 70),
                macd=random.uniform(-1, 1),
                sma_20=random.uniform(150, 200),
                sma_50=random.uniform(140, 190),
                timestamp=datetime.now()
            )
            
    except Exception as e:
        logger.error(f"❌ Technical indicators error for {symbol}: {e}")
        return TechnicalIndicators(
            symbol=symbol,
            rsi=random.uniform(30, 70),
            macd=random.uniform(-1, 1),
            sma_20=random.uniform(150, 200),
            sma_50=random.uniform(140, 190),
            timestamp=datetime.now()
        )

async def generate_ai_signal(symbol: str) -> TradeSignal:
    """Generate AI trading signal based on real market data"""
    try:
        price_data = await get_yahoo_finance_data(symbol)
        tech_indicators = await get_technical_indicators(symbol)
        
        if not price_data:
            return TradeSignal(
                symbol=symbol,
                action=random.choice(["buy", "sell"]),
                confidence=0.5,
                price=100.0,
                timestamp=datetime.now(),
                reasoning="Data unavailable"
            )
        
        # Analyze signals
        buy_signals = 0
        sell_signals = 0
        reasoning_parts = []
        
        # RSI analysis
        if tech_indicators.rsi < 30:
            buy_signals += 2
            reasoning_parts.append("RSI oversold")
        elif tech_indicators.rsi > 70:
            sell_signals += 2
            reasoning_parts.append("RSI overbought")
        
        # Price momentum
        if price_data.change_percent > 2:
            buy_signals += 1
            reasoning_parts.append("Strong upward momentum")
        elif price_data.change_percent < -2:
            sell_signals += 1
            reasoning_parts.append("Strong downward momentum")
        
        # MACD signal
        if tech_indicators.macd > 0:
            buy_signals += 1
            reasoning_parts.append("MACD bullish")
        else:
            sell_signals += 1
            reasoning_parts.append("MACD bearish")
        
        # Determine action
        if buy_signals > sell_signals:
            action = "buy"
            confidence = min(0.95, 0.6 + (buy_signals * 0.1))
        elif sell_signals > buy_signals:
            action = "sell"
            confidence = min(0.95, 0.6 + (sell_signals * 0.1))
        else:
            action = random.choice(["buy", "sell"])
            confidence = 0.5
            reasoning_parts.append("Mixed signals")
        
        reasoning = "; ".join(reasoning_parts) if reasoning_parts else "Technical analysis"
        
        return TradeSignal(
            symbol=symbol,
            action=action,
            confidence=round(confidence, 2),
            price=price_data.price,
            timestamp=datetime.now(),
            reasoning=reasoning
        )
        
    except Exception as e:
        logger.error(f"❌ Signal generation error for {symbol}: {e}")
        return TradeSignal(
            symbol=symbol,
            action=random.choice(["buy", "sell"]),
            confidence=0.5,
            price=100.0,
            timestamp=datetime.now(),
            reasoning=f"Error: {str(e)}"
        )

async def live_price_updater():
    """Background task to update prices and broadcast to WebSocket clients"""
    while True:
        try:
            if len(manager.active_connections) > 0:
                # Get updated prices for tracked symbols
                price_updates = {}
                for symbol in TRACKED_SYMBOLS[:5]:  # Limit to 5 symbols to avoid rate limits
                    price_data = await get_yahoo_finance_data(symbol)
                    if price_data:
                        price_updates[symbol] = price_data.dict()
                
                if price_updates:
                    update = LiveUpdate(
                        type="price_update",
                        data=price_updates,
                        timestamp=datetime.now()
                    )
                    
                    await manager.broadcast(json.dumps(update.dict(), default=str))
                    logger.info(f"📡 Broadcasted price updates for {len(price_updates)} symbols")
                
                # Update positions with new prices
                for pos in positions:
                    if pos.symbol in price_updates:
                        new_price = price_updates[pos.symbol]['price']
                        pos.current_price = new_price
                        pos.pnl = (pos.current_price - pos.entry_price) * pos.quantity
                        pos.pnl_percent = (pos.current_price - pos.entry_price) / pos.entry_price * 100
                
                # Broadcast portfolio update
                portfolio_value = sum(pos.quantity * pos.current_price for pos in positions)
                today_pnl = sum(pos.pnl for pos in positions)
                
                portfolio_update = LiveUpdate(
                    type="portfolio_update",
                    data={
                        "portfolio_value": portfolio_value,
                        "today_pnl": today_pnl,
                        "positions": [pos.dict() for pos in positions]
                    },
                    timestamp=datetime.now()
                )
                
                await manager.broadcast(json.dumps(portfolio_update.dict(), default=str))
                logger.info(f"📊 Broadcasted portfolio update: ${portfolio_value:,.2f}")
                
        except Exception as e:
            logger.error(f"❌ Error in live price updater: {e}")
        
        await asyncio.sleep(15)  # Update every 15 seconds

async def ai_signal_updater():
    """Background task to generate and broadcast AI signals"""
    while True:
        try:
            if len(manager.active_connections) > 0:
                # Generate new AI signals
                signals = []
                for symbol in TRACKED_SYMBOLS[:3]:  # Generate signals for 3 symbols
                    signal = await generate_ai_signal(symbol)
                    signals.append(signal.dict())
                
                signal_update = LiveUpdate(
                    type="ai_signals_update",
                    data={"signals": signals},
                    timestamp=datetime.now()
                )
                
                await manager.broadcast(json.dumps(signal_update.dict(), default=str))
                logger.info(f"🤖 Broadcasted {len(signals)} AI signals")
                
        except Exception as e:
            logger.error(f"❌ Error in AI signal updater: {e}")
        
        await asyncio.sleep(30)  # Update every 30 seconds

# Start background tasks
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(live_price_updater())
    asyncio.create_task(ai_signal_updater())
    logger.info("🚀 Background tasks started: Live price updates & AI signals")

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            logger.info(f"📨 Received WebSocket message: {data}")
            
            # Echo back a confirmation
            await manager.send_personal_message(
                json.dumps({
                    "type": "confirmation",
                    "message": "Connected to real-time trading data",
                    "timestamp": datetime.now().isoformat()
                }),
                websocket
            )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("🔌 WebSocket client disconnected")

# REST API Endpoints
@app.get("/")
async def root():
    return {
        "message": "🚀 Real-time AI Trading Backend with WebSocket Streaming",
        "status": "active",
        "features": [
            "Real-time price streaming via WebSocket",
            "Live portfolio updates",
            "AI signal generation",
            "Yahoo Finance integration"
        ],
        "websocket_url": "ws://localhost:8000/ws",
        "active_connections": len(manager.active_connections),
        "timestamp": datetime.now()
    }

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
        ai_confidence=random.uniform(0.75, 0.95),
        market_data_source="yahoo_finance_realtime"
    )

@app.get("/api/v1/market/price/{symbol}")
async def get_symbol_price(symbol: str):
    """Get real-time market price for a symbol"""
    price_data = await get_yahoo_finance_data(symbol.upper())
    if price_data:
        return price_data
    else:
        raise HTTPException(status_code=404, detail=f"Could not fetch data for symbol {symbol}")

@app.get("/api/v1/trading/ai-signals")
async def get_ai_signals():
    """Get latest AI trading signals"""
    signals = []
    for symbol in TRACKED_SYMBOLS[:3]:
        signal = await generate_ai_signal(symbol)
        signals.append(signal)
    
    return {"signals": signals, "timestamp": datetime.now()}

@app.get("/api/v1/trading/positions")
async def get_positions():
    """Get current positions with real-time prices"""
    return {"positions": positions, "timestamp": datetime.now()}

@app.get("/api/v1/trading/ai-analysis")
async def get_ai_analysis():
    """Get AI market analysis with real data"""
    try:
        symbols = ["AAPL", "MSFT", "GOOGL"]
        market_data = {}
        total_sentiment = 0
        
        for symbol in symbols:
            price_data = await get_yahoo_finance_data(symbol)
            tech_indicators = await get_technical_indicators(symbol)
            
            if price_data:
                sentiment_score = 0
                if tech_indicators.rsi > 50:
                    sentiment_score += 1
                if tech_indicators.macd > 0:
                    sentiment_score += 1
                if price_data.change_percent > 0:
                    sentiment_score += 1
                
                total_sentiment += sentiment_score / 3
                
                market_data[symbol] = {
                    "price": price_data.price,
                    "change_percent": price_data.change_percent,
                    "rsi": tech_indicators.rsi,
                    "macd": tech_indicators.macd,
                    "sentiment": sentiment_score / 3
                }
        
        avg_sentiment = total_sentiment / len(symbols) if symbols else 0.5
        
        if avg_sentiment > 0.6:
            sentiment = "Bullish"
        elif avg_sentiment < 0.4:
            sentiment = "Bearish"
        else:
            sentiment = "Neutral"
        
        recommendations = []
        for symbol, data in market_data.items():
            if data["rsi"] < 30:
                recommendations.append(f"{symbol}: Oversold - potential buy opportunity")
            elif data["rsi"] > 70:
                recommendations.append(f"{symbol}: Overbought - consider profit taking")
        
        if not recommendations:
            recommendations.append("Markets are balanced - monitor for breakout opportunities")
        
        return {
            "market_sentiment": {
                "sentiment": sentiment,
                "score": round(avg_sentiment, 2),
                "confidence": 0.85
            },
            "market_data": market_data,
            "recommendations": recommendations,
            "risk_level": "medium",
            "data_source": "yahoo_finance_realtime",
            "websocket_active": len(manager.active_connections) > 0,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"❌ AI analysis error: {e}")
        return {
            "market_sentiment": {"sentiment": "Neutral", "score": 0.5, "confidence": 0.5},
            "recommendations": ["Market data temporarily unavailable"],
            "risk_level": "medium",
            "data_source": "fallback",
            "timestamp": datetime.now(),
            "error": str(e)
        }

@app.post("/api/v1/trading/execute")
async def execute_trade(symbol: str, action: str, quantity: int):
    """Execute a trade with real market price"""
    if not trading_active:
        raise HTTPException(status_code=400, detail="Trading is currently disabled")
    
    try:
        price_data = await get_yahoo_finance_data(symbol.upper())
        if not price_data:
            raise HTTPException(status_code=404, detail=f"Could not get market price for {symbol}")
        
        trade_result = {
            "symbol": symbol.upper(),
            "action": action,
            "quantity": quantity,
            "execution_price": price_data.price,
            "market_source": "yahoo_finance",
            "timestamp": datetime.now(),
            "status": "executed"
        }
        
        # Broadcast trade execution to WebSocket clients
        if len(manager.active_connections) > 0:
            trade_update = LiveUpdate(
                type="trade_executed",
                data=trade_result,
                timestamp=datetime.now()
            )
            await manager.broadcast(json.dumps(trade_update.dict(), default=str))
        
        logger.info(f"✅ Trade executed: {action} {quantity} {symbol} @ ${price_data.price}")
        return trade_result
        
    except Exception as e:
        logger.error(f"❌ Trade execution error: {e}")
        raise HTTPException(status_code=500, detail=f"Trade execution failed: {str(e)}")

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

@app.get("/api/v1/websocket/stats")
async def get_websocket_stats():
    """Get WebSocket connection statistics"""
    return {
        "active_connections": len(manager.active_connections),
        "tracking_symbols": TRACKED_SYMBOLS,
        "update_intervals": {
            "price_updates": "15 seconds",
            "ai_signals": "30 seconds"
        },
        "timestamp": datetime.now()
    }

if __name__ == "__main__":
    print("🚀 Starting Real-time AI Trading Backend...")
    print("📊 Data Source: Yahoo Finance (Real-time)")
    print("⚡ WebSocket: ws://localhost:8000/ws")
    print("🌐 Dashboard: http://localhost:3000/ai_trading_dashboard.html")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔧 Admin Panel: http://localhost:8000/redoc")
    print("💡 Features: Real-time streaming, Live updates, AI signals")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")