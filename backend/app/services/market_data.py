import yfinance as yf
import pandas as pd
import numpy as np
# import talib  # Comment out for now
import asyncio
import requests
from typing import Dict, List, Optional
from app.core.config import settings
# from textblob import TextBlob  # Temporarily disabled due to dependency issues
import logging

logger = logging.getLogger(__name__)

class MarketDataService:
    def __init__(self):
        self.alpha_vantage_key = settings.alpha_vantage_api_key
        self.news_api_key = settings.news_api_key

    async def get_current_price(self, symbol: str) -> Dict:
        """Get current price and basic info for a symbol"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="1d")
            
            if hist.empty:
                raise Exception(f"No data found for symbol {symbol}")
            
            current_price = hist['Close'].iloc[-1]
            prev_close = info.get('previousClose', current_price)
            change = current_price - prev_close
            change_percent = (change / prev_close) * 100 if prev_close else 0
            
            return {
                "symbol": symbol,
                "price": round(current_price, 2),
                "change": round(change, 2),
                "change_percent": round(change_percent, 2),
                "volume": int(hist['Volume'].iloc[-1]) if 'Volume' in hist else 0,
                "high": round(hist['High'].iloc[-1], 2),
                "low": round(hist['Low'].iloc[-1], 2),
                "open": round(hist['Open'].iloc[-1], 2),
                "timestamp": hist.index[-1].isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting current price for {symbol}: {e}")
            raise

    async def get_historical_data(self, symbol: str, period: str = "1y", interval: str = "1d") -> Dict:
        """Get historical price data"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period, interval=interval)
            
            if hist.empty:
                raise Exception(f"No historical data found for symbol {symbol}")
            
            # Convert to list of dictionaries
            data = []
            for index, row in hist.iterrows():
                data.append({
                    "timestamp": index.isoformat(),
                    "open": round(row['Open'], 2),
                    "high": round(row['High'], 2),
                    "low": round(row['Low'], 2),
                    "close": round(row['Close'], 2),
                    "volume": int(row['Volume']) if 'Volume' in row else 0
                })
            
            return {
                "symbol": symbol,
                "period": period,
                "interval": interval,
                "data": data
            }
        except Exception as e:
            logger.error(f"Error getting historical data for {symbol}: {e}")
            raise

    async def get_technical_indicators(self, symbol: str, period: str = "1y") -> Dict:
        """Calculate technical indicators using pandas (simple implementations)"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if len(hist) < 50:  # Need enough data for indicators
                raise Exception(f"Insufficient data for indicators calculation")
            
            prices = hist['Close']
            
            # Calculate RSI (simplified)
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=settings.rsi_period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=settings.rsi_period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # Calculate MACD (simplified)
            ema_12 = prices.ewm(span=settings.macd_fast).mean()
            ema_26 = prices.ewm(span=settings.macd_slow).mean()
            macd = ema_12 - ema_26
            macd_signal = macd.ewm(span=settings.macd_signal).mean()
            macd_hist = macd - macd_signal
            
            # Calculate moving averages
            sma_20 = prices.rolling(window=20).mean()
            sma_50 = prices.rolling(window=50).mean()
            
            # Calculate Bollinger Bands (simplified)
            sma_20_bb = prices.rolling(window=20).mean()
            std_20 = prices.rolling(window=20).std()
            bb_upper = sma_20_bb + (std_20 * 2)
            bb_lower = sma_20_bb - (std_20 * 2)
            bb_middle = sma_20_bb
            
            # Volume indicators
            volume_sma = hist['Volume'].rolling(window=20).mean()
            
            # Get current values (last non-NaN values)
            current_rsi = float(rsi.dropna().iloc[-1]) if len(rsi.dropna()) > 0 else None
            current_macd = float(macd.dropna().iloc[-1]) if len(macd.dropna()) > 0 else None
            current_macd_signal = float(macd_signal.dropna().iloc[-1]) if len(macd_signal.dropna()) > 0 else None
            current_macd_hist = float(macd_hist.dropna().iloc[-1]) if len(macd_hist.dropna()) > 0 else None
            
            return {
                "symbol": symbol,
                "rsi": {
                    "current": round(current_rsi, 2) if current_rsi else None,
                    "overbought": current_rsi > settings.rsi_overbought if current_rsi else False,
                    "oversold": current_rsi < settings.rsi_oversold if current_rsi else False,
                    "history": [round(x, 2) for x in rsi.dropna().tail(30)]  # Last 30 values
                },
                "macd": {
                    "macd": round(current_macd, 4) if current_macd else None,
                    "signal": round(current_macd_signal, 4) if current_macd_signal else None,
                    "histogram": round(current_macd_hist, 4) if current_macd_hist else None,
                    "bullish": current_macd > current_macd_signal if current_macd and current_macd_signal else False
                },
                "moving_averages": {
                    "sma_20": round(float(sma_20.dropna().iloc[-1]), 2) if len(sma_20.dropna()) > 0 else None,
                    "sma_50": round(float(sma_50.dropna().iloc[-1]), 2) if len(sma_50.dropna()) > 0 else None,
                    "ema_12": round(float(ema_12.dropna().iloc[-1]), 2) if len(ema_12.dropna()) > 0 else None,
                    "ema_26": round(float(ema_26.dropna().iloc[-1]), 2) if len(ema_26.dropna()) > 0 else None
                },
                "bollinger_bands": {
                    "upper": round(float(bb_upper.dropna().iloc[-1]), 2) if len(bb_upper.dropna()) > 0 else None,
                    "middle": round(float(bb_middle.dropna().iloc[-1]), 2) if len(bb_middle.dropna()) > 0 else None,
                    "lower": round(float(bb_lower.dropna().iloc[-1]), 2) if len(bb_lower.dropna()) > 0 else None
                },
                "volume": {
                    "current": int(hist['Volume'].iloc[-1]) if 'Volume' in hist else 0,
                    "average": int(volume_sma.dropna().iloc[-1]) if len(volume_sma.dropna()) > 0 else 0,
                    "volume_spike": hist['Volume'].iloc[-1] > (volume_sma.dropna().iloc[-1] * 1.5) if len(volume_sma.dropna()) > 0 else False
                }
            }
        except Exception as e:
            logger.error(f"Error calculating indicators for {symbol}: {e}")
            raise

    async def get_market_news(self, symbol: str, limit: int = 10) -> Dict:
        """Get news for a symbol with sentiment analysis"""
        try:
            # For demo purposes, we'll use a simple news fetch
            # In production, you'd use NewsAPI or similar service
            
            if not self.news_api_key:
                # Return mock news for demo
                return self._get_mock_news(symbol, limit)
            
            # Use NewsAPI if key is available
            url = f"https://newsapi.org/v2/everything"
            params = {
                "q": symbol,
                "sortBy": "publishedAt",
                "pageSize": limit,
                "apiKey": self.news_api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            news_data = response.json()
            
            # Add sentiment analysis
            articles = []
            for article in news_data.get("articles", []):
                sentiment = self._analyze_sentiment(article.get("title", "") + " " + article.get("description", ""))
                articles.append({
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url"),
                    "published_at": article.get("publishedAt"),
                    "source": article.get("source", {}).get("name"),
                    "sentiment": sentiment
                })
            
            return {
                "symbol": symbol,
                "articles": articles,
                "total_results": news_data.get("totalResults", 0)
            }
            
        except Exception as e:
            logger.error(f"Error getting news for {symbol}: {e}")
            return self._get_mock_news(symbol, limit)

    def _analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of text - simplified version without TextBlob"""
        try:
            # Simple keyword-based sentiment analysis
            text_lower = text.lower()
            positive_words = ['good', 'great', 'excellent', 'positive', 'rise', 'up', 'gain', 'profit', 'bull', 'strong']
            negative_words = ['bad', 'terrible', 'negative', 'fall', 'down', 'loss', 'bear', 'weak', 'decline', 'crash']
            
            positive_count = sum(1 for word in positive_words if word in text_lower)
            negative_count = sum(1 for word in negative_words if word in text_lower)
            
            if positive_count > negative_count:
                sentiment = "positive"
                polarity = 0.5
            elif negative_count > positive_count:
                sentiment = "negative" 
                polarity = -0.5
            else:
                sentiment = "neutral"
                polarity = 0.0
            
            return {
                "sentiment": sentiment,
                "polarity": round(polarity, 3),
                "subjectivity": 0.5  # Default subjectivity
            }
        except:
            return {"sentiment": "neutral", "polarity": 0.0, "subjectivity": 0.0}

    def _get_mock_news(self, symbol: str, limit: int) -> Dict:
        """Generate mock news for demo purposes"""
        mock_articles = [
            {
                "title": f"{symbol} Reports Strong Q3 Earnings",
                "description": f"{symbol} exceeded analyst expectations with strong revenue growth.",
                "url": f"https://example.com/news/{symbol.lower()}-earnings",
                "published_at": "2024-10-16T10:00:00Z",
                "source": "Financial Times",
                "sentiment": {"sentiment": "positive", "polarity": 0.5, "subjectivity": 0.6}
            },
            {
                "title": f"Analysts Upgrade {symbol} Price Target",
                "description": f"Wall Street analysts raise price target for {symbol} following positive market trends.",
                "url": f"https://example.com/news/{symbol.lower()}-upgrade",
                "published_at": "2024-10-16T08:30:00Z",
                "source": "MarketWatch",
                "sentiment": {"sentiment": "positive", "polarity": 0.3, "subjectivity": 0.4}
            },
            {
                "title": f"{symbol} Announces New Product Launch",
                "description": f"{symbol} unveils innovative new product line expected to drive growth.",
                "url": f"https://example.com/news/{symbol.lower()}-product",
                "published_at": "2024-10-15T16:45:00Z",
                "source": "Tech Crunch",
                "sentiment": {"sentiment": "positive", "polarity": 0.4, "subjectivity": 0.7}
            }
        ]
        
        return {
            "symbol": symbol,
            "articles": mock_articles[:limit],
            "total_results": len(mock_articles)
        }