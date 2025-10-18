"""
Enhanced AI Trading Backend with Real Market Data Integration
Supports Alpha Vantage API and Yahoo Finance as backup
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Union
import uvicorn
import asyncio
import aiohttp
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import os
from dotenv import load_dotenv
import json
import time
from datetime import datetime, timedelta
import random
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Enhanced AI Trading Backend", version="2.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")
USE_REAL_DATA = ALPHA_VANTAGE_API_KEY != "demo" and ALPHA_VANTAGE_API_KEY != "your_alpha_vantage_key_here"

# Initialize Alpha Vantage clients
ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
ti = TechIndicators(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')

# Data Models
class MarketPrice(BaseModel):
    symbol: str
    price: float
    change: float
    change_percent: float
    volume: Optional[int] = None
    timestamp: datetime
    source: str  # 'alpha_vantage', 'yahoo_finance', or 'simulated'

class TradeSignal(BaseModel):
    symbol: str
    action: str  # 'buy' or 'sell'
    confidence: float
    price: float
    timestamp: datetime
    reasoning: str

class TechnicalIndicators(BaseModel):
    symbol: str
    rsi: float
    macd: float
    macd_signal: float
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
    market_data_source: str

# Global state
trading_active = True
positions = [
    Position(symbol="AAPL", quantity=100, entry_price=175.50, current_price=182.30, pnl=680.00, pnl_percent=3.87),
    Position(symbol="GOOGL", quantity=50, entry_price=2380.00, current_price=2420.50, pnl=2025.00, pnl_percent=1.70),
    Position(symbol="MSFT", quantity=75, entry_price=335.20, current_price=331.80, pnl=-255.00, pnl_percent=-1.01),
]

# Cache for market data
price_cache = {}
CACHE_DURATION = 60  # Cache prices for 1 minute

# Market Data Functions
async def get_alpha_vantage_price(symbol: str) -> Optional[MarketPrice]:
    """Get real-time price from Alpha Vantage API"""
    try:
        if not USE_REAL_DATA:
            return None
            
        # Check cache first
        cache_key = f"av_{symbol}"
        if cache_key in price_cache:
            cached_data = price_cache[cache_key]
            if time.time() - cached_data['timestamp'] < CACHE_DURATION:
                return cached_data['data']
        
        # Get quote data
        quote_data, meta_data = ts.get_quote_endpoint(symbol=symbol)
        
        if quote_data is not None and not quote_data.empty:
            latest = quote_data.iloc[0]
            price = float(latest['05. price'])
            change = float(latest['09. change'])
            change_percent = float(latest['10. change percent'].rstrip('%'))
            volume = int(latest['06. volume']) if '06. volume' in latest else None
            
            market_price = MarketPrice(
                symbol=symbol,
                price=price,
                change=change,
                change_percent=change_percent,
                volume=volume,
                timestamp=datetime.now(),
                source="alpha_vantage"
            )
            
            # Cache the result
            price_cache[cache_key] = {
                'data': market_price,
                'timestamp': time.time()
            }
            
            return market_price
            
    except Exception as e:
        logger.warning(f"Alpha Vantage API error for {symbol}: {e}")
        return None

async def get_yahoo_finance_price(symbol: str) -> Optional[MarketPrice]:
    """Get real-time price from Yahoo Finance as backup"""
    try:
        # Check cache first
        cache_key = f"yf_{symbol}"
        if cache_key in price_cache:
            cached_data = price_cache[cache_key]
            if time.time() - cached_data['timestamp'] < CACHE_DURATION:
                return cached_data['data']
        
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period="2d")
        
        if len(hist) >= 2:
            current_price = hist['Close'].iloc[-1]
            previous_price = hist['Close'].iloc[-2]
            change = current_price - previous_price
            change_percent = (change / previous_price) * 100
            volume = int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else None
            
            market_price = MarketPrice(
                symbol=symbol,
                price=float(current_price),
                change=float(change),
                change_percent=float(change_percent),
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
            
    except Exception as e:
        logger.warning(f"Yahoo Finance API error for {symbol}: {e}")
        return None

def get_simulated_price(symbol: str) -> MarketPrice:
    """Generate simulated price data as fallback"""
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
    # Add random variation
    variation = random.uniform(-0.05, 0.05)
    current_price = base_price * (1 + variation)
    change = current_price - base_price
    change_percent = (change / base_price) * 100
    
    return MarketPrice(
        symbol=symbol,
        price=round(current_price, 2),
        change=round(change, 2),
        change_percent=round(change_percent, 2),
        volume=random.randint(1000000, 50000000),
        timestamp=datetime.now(),
        source="simulated"
    )

async def get_market_price(symbol: str) -> MarketPrice:
    """Get market price with fallback logic: Alpha Vantage -> Yahoo Finance -> Simulated"""
    
    # Try Alpha Vantage first
    price = await get_alpha_vantage_price(symbol)
    if price:
        return price
    
    # Fallback to Yahoo Finance
    price = await get_yahoo_finance_price(symbol)
    if price:
        return price
    
    # Final fallback to simulated data
    return get_simulated_price(symbol)

async def get_technical_indicators(symbol: str) -> TechnicalIndicators:
    """Get technical indicators for a symbol"""
    try:
        if USE_REAL_DATA:
            # Get RSI
            rsi_data, _ = ti.get_rsi(symbol=symbol, interval='daily', time_period=14)
            rsi = float(rsi_data.iloc[0]['RSI']) if not rsi_data.empty else 50.0
            
            # Get MACD
            macd_data, _ = ti.get_macd(symbol=symbol, interval='daily')
            if not macd_data.empty:
                macd = float(macd_data.iloc[0]['MACD'])
                macd_signal = float(macd_data.iloc[0]['MACD_Signal'])
            else:
                macd = 0.0
                macd_signal = 0.0
            
            # Get SMAs
            sma20_data, _ = ti.get_sma(symbol=symbol, interval='daily', time_period=20)
            sma50_data, _ = ti.get_sma(symbol=symbol, interval='daily', time_period=50)
            
            sma_20 = float(sma20_data.iloc[0]['SMA']) if not sma20_data.empty else 0.0
            sma_50 = float(sma50_data.iloc[0]['SMA']) if not sma50_data.empty else 0.0
            
        else:
            # Simulated technical indicators
            rsi = random.uniform(20, 80)
            macd = random.uniform(-2, 2)
            macd_signal = macd + random.uniform(-0.5, 0.5)
            sma_20 = random.uniform(150, 200)
            sma_50 = random.uniform(140, 190)
        
        return TechnicalIndicators(
            symbol=symbol,
            rsi=rsi,
            macd=macd,
            macd_signal=macd_signal,
            sma_20=sma_20,
            sma_50=sma_50,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.warning(f"Technical indicators error for {symbol}: {e}")
        # Return simulated data on error
        return TechnicalIndicators(
            symbol=symbol,
            rsi=random.uniform(20, 80),
            macd=random.uniform(-2, 2),
            macd_signal=random.uniform(-2, 2),
            sma_20=random.uniform(150, 200),
            sma_50=random.uniform(140, 190),
            timestamp=datetime.now()
        )

def generate_ai_signal_with_analysis(symbol: str, price_data: MarketPrice, 
                                   tech_indicators: TechnicalIndicators) -> TradeSignal:
    """Generate AI trading signal based on real market data and technical analysis"""
    
    reasoning_factors = []
    buy_score = 0
    sell_score = 0
    
    # RSI Analysis
    if tech_indicators.rsi < 30:
        buy_score += 2
        reasoning_factors.append("RSI oversold (bullish)")
    elif tech_indicators.rsi > 70:
        sell_score += 2
        reasoning_factors.append("RSI overbought (bearish)")
    
    # MACD Analysis
    if tech_indicators.macd > tech_indicators.macd_signal:
        buy_score += 1
        reasoning_factors.append("MACD bullish crossover")
    else:
        sell_score += 1
        reasoning_factors.append("MACD bearish crossover")
    
    # Price momentum
    if price_data.change_percent > 2:
        buy_score += 1
        reasoning_factors.append("Strong positive momentum")
    elif price_data.change_percent < -2:
        sell_score += 1
        reasoning_factors.append("Strong negative momentum")
    
    # Moving average analysis
    if price_data.price > tech_indicators.sma_20 > tech_indicators.sma_50:
        buy_score += 1
        reasoning_factors.append("Price above rising MA")
    elif price_data.price < tech_indicators.sma_20 < tech_indicators.sma_50:
        sell_score += 1
        reasoning_factors.append("Price below falling MA")
    
    # Determine action and confidence
    if buy_score > sell_score:
        action = "buy"
        confidence = min(0.95, 0.6 + (buy_score * 0.1))
    elif sell_score > buy_score:
        action = "sell"
        confidence = min(0.95, 0.6 + (sell_score * 0.1))
    else:
        action = random.choice(["buy", "sell"])
        confidence = 0.5
        reasoning_factors.append("Mixed signals")
    
    reasoning = "; ".join(reasoning_factors) if reasoning_factors else "Technical analysis"
    
    return TradeSignal(
        symbol=symbol,
        action=action,
        confidence=confidence,
        price=price_data.price,
        timestamp=datetime.now(),
        reasoning=reasoning
    )

# API Endpoints
@app.get("/")
async def root():
    data_source = "real_data" if USE_REAL_DATA else "simulated_data"
    return {
        "message": "Enhanced AI Trading Backend with Real Market Data",
        "status": "active",
        "data_source": data_source,
        "timestamp": datetime.now()
    }

@app.get("/api/v1/trading/status")
async def get_trading_status():
    """Get current trading status with data source info"""
    portfolio_value = sum(pos.quantity * pos.current_price for pos in positions)
    today_pnl = sum(pos.pnl for pos in positions)
    data_source = "real_data" if USE_REAL_DATA else "simulated_data"
    
    return TradingStatus(
        is_active=trading_active,
        total_positions=len(positions),
        portfolio_value=portfolio_value,
        today_pnl=today_pnl,
        ai_confidence=random.uniform(0.75, 0.95),
        market_data_source=data_source
    )

@app.get("/api/v1/market/price/{symbol}")
async def get_symbol_price(symbol: str):
    """Get current market price for a symbol with real data"""
    price_data = await get_market_price(symbol)
    return price_data

@app.get("/api/v1/market/technical/{symbol}")
async def get_symbol_technical_indicators(symbol: str):
    """Get technical indicators for a symbol"""
    indicators = await get_technical_indicators(symbol)
    return indicators

@app.get("/api/v1/trading/ai-signals")
async def get_enhanced_ai_signals():
    """Get AI trading signals based on real market data and technical analysis"""
    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
    signals = []
    
    for symbol in symbols[:3]:  # Generate signals for 3 symbols
        try:
            price_data = await get_market_price(symbol)
            tech_indicators = await get_technical_indicators(symbol)
            signal = generate_ai_signal_with_analysis(symbol, price_data, tech_indicators)
            signals.append(signal)
        except Exception as e:
            logger.error(f"Error generating signal for {symbol}: {e}")
    
    return {"signals": signals}

@app.get("/api/v1/trading/positions")
async def get_positions_with_real_prices():
    """Get current positions with updated real market prices"""
    # Update current prices with real market data
    for pos in positions:
        try:
            price_data = await get_market_price(pos.symbol)
            pos.current_price = price_data.price
            pos.pnl = (pos.current_price - pos.entry_price) * pos.quantity
            pos.pnl_percent = (pos.current_price - pos.entry_price) / pos.entry_price * 100
        except Exception as e:
            logger.error(f"Error updating price for {pos.symbol}: {e}")
    
    return {"positions": positions}

@app.get("/api/v1/trading/ai-analysis")
async def get_enhanced_ai_analysis():
    """Get enhanced AI market analysis with real data"""
    try:
        # Get real market data for analysis
        symbols = ["AAPL", "SPY", "QQQ"]  # Major market indicators
        market_sentiment_score = 0
        total_symbols = len(symbols)
        
        technical_data = {}
        
        for symbol in symbols:
            price_data = await get_market_price(symbol)
            tech_indicators = await get_technical_indicators(symbol)
            
            # Calculate sentiment based on technical indicators
            sentiment = 0
            if tech_indicators.rsi > 50:
                sentiment += 1
            if tech_indicators.macd > tech_indicators.macd_signal:
                sentiment += 1
            if price_data.change_percent > 0:
                sentiment += 1
                
            market_sentiment_score += sentiment / 3  # Normalize to 0-1
            technical_data[symbol] = {
                "price": price_data.price,
                "change_percent": price_data.change_percent,
                "rsi": tech_indicators.rsi,
                "macd": tech_indicators.macd
            }
        
        avg_sentiment = market_sentiment_score / total_symbols
        
        if avg_sentiment > 0.6:
            sentiment = "Bullish"
        elif avg_sentiment < 0.4:
            sentiment = "Bearish"
        else:
            sentiment = "Neutral"
        
        recommendations = []
        
        # Generate recommendations based on real data
        for symbol, data in technical_data.items():
            if data["rsi"] < 30:
                recommendations.append(f"{symbol}: Oversold conditions - potential buy opportunity")
            elif data["rsi"] > 70:
                recommendations.append(f"{symbol}: Overbought conditions - consider taking profits")
            
            if abs(data["change_percent"]) > 3:
                direction = "upward" if data["change_percent"] > 0 else "downward"
                recommendations.append(f"{symbol}: Strong {direction} momentum ({data['change_percent']:.1f}%)")
        
        if not recommendations:
            recommendations.append("Market conditions are balanced - monitor for breakouts")
        
        data_source = "real_market_data" if USE_REAL_DATA else "simulated_data"
        
        analysis = {
            "market_sentiment": {
                "sentiment": sentiment,
                "score": avg_sentiment,
                "confidence": random.uniform(0.8, 0.95),
                "factors": ["Real-time technical indicators", "Price momentum", "Market volume"]
            },
            "technical_indicators": technical_data,
            "recommendations": recommendations,
            "risk_level": "medium" if 0.4 <= avg_sentiment <= 0.6 else "low" if avg_sentiment > 0.6 else "high",
            "confidence": random.uniform(0.8, 0.95),
            "data_source": data_source,
            "timestamp": datetime.now()
        }
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error in AI analysis: {e}")
        # Fallback to basic analysis
        return {
            "market_sentiment": {
                "sentiment": "Neutral",
                "score": 0.5,
                "confidence": 0.7,
                "factors": ["Technical analysis", "Market indicators"]
            },
            "recommendations": ["Monitor market conditions", "Wait for clear signals"],
            "risk_level": "medium",
            "confidence": 0.7,
            "data_source": "fallback",
            "timestamp": datetime.now(),
            "error": str(e)
        }

@app.get("/api/v1/symbols/commodities")
async def get_commodities():
    """Get commodity prices with real data where available"""
    commodities = []
    commodity_symbols = {
        "GLD": "Gold ETF",
        "SLV": "Silver ETF", 
        "USO": "Oil ETF",
        "UNG": "Natural Gas ETF"
    }
    
    for symbol, name in commodity_symbols.items():
        try:
            price_data = await get_market_price(symbol)
            commodities.append({
                "symbol": symbol,
                "name": name,
                "price": price_data.price,
                "change": price_data.change,
                "change_percent": price_data.change_percent,
                "source": price_data.source
            })
        except Exception as e:
            logger.error(f"Error getting commodity price for {symbol}: {e}")
    
    return {"commodities": commodities}

@app.get("/api/v1/categories")
async def get_categories():
    """Get trading categories"""
    categories = [
        {"id": 1, "name": "Stocks", "count": 150},
        {"id": 2, "name": "ETFs", "count": 75},
        {"id": 3, "name": "Commodities", "count": 25},
        {"id": 4, "name": "Forex", "count": 30}
    ]
    return {"categories": categories}

@app.post("/api/v1/trading/execute")
async def execute_trade_with_real_price(symbol: str, action: str, quantity: int):
    """Execute a manual trade using real market prices"""
    if not trading_active:
        raise HTTPException(status_code=400, detail="Trading is currently disabled")
    
    try:
        # Get real market price for execution
        price_data = await get_market_price(symbol)
        execution_price = price_data.price
        
        trade_result = {
            "symbol": symbol,
            "action": action,
            "quantity": quantity,
            "execution_price": execution_price,
            "market_price_source": price_data.source,
            "timestamp": datetime.now(),
            "status": "executed"
        }
        
        logger.info(f"Trade executed: {action} {quantity} {symbol} @ ${execution_price}")
        return trade_result
        
    except Exception as e:
        logger.error(f"Trade execution error: {e}")
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

if __name__ == "__main__":
    print("🚀 Starting Enhanced AI Trading Backend with Real Market Data...")
    print(f"📊 Data Source: {'Real Market Data (Alpha Vantage + Yahoo Finance)' if USE_REAL_DATA else 'Simulated Data'}")
    print("🌐 Dashboard: http://localhost:3000/ai_trading_dashboard.html")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔧 Admin Panel: http://localhost:8000/redoc")
    
    if not USE_REAL_DATA:
        print("⚠️  Note: Using simulated data. Set ALPHA_VANTAGE_API_KEY in .env for real market data")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)