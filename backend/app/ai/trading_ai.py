import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import openai
from app.services.market_data import MarketDataService
from app.services.analysis import AnalysisService
from app.core.config import settings
import numpy as np

logger = logging.getLogger(__name__)

class TradingAI:
    def __init__(self):
        self.market_service = MarketDataService()
        self.analysis_service = AnalysisService()
        self.openai_client = None
        self.auto_trading_enabled = settings.ai_trading_enabled
        
        # Initialize OpenAI client if API key is available
        if settings.openai_api_key:
            openai.api_key = settings.openai_api_key
            self.openai_client = openai

    async def analyze_symbol(self, symbol: str, timeframe: str = "1d", include_news: bool = True) -> Dict:
        """Comprehensive AI analysis of a symbol"""
        try:
            # Gather all relevant data
            price_data = await self.market_service.get_current_price(symbol)
            indicators = await self.market_service.get_technical_indicators(symbol)
            technical_analysis = await self.analysis_service.get_technical_analysis(symbol)
            risk_analysis = await self.analysis_service.get_risk_analysis(symbol)
            
            news_data = None
            if include_news:
                news_data = await self.market_service.get_market_news(symbol)
            
            # Generate AI analysis
            ai_insights = await self._generate_ai_insights(
                symbol, price_data, indicators, technical_analysis, risk_analysis, news_data
            )
            
            return {
                "symbol": symbol,
                "timestamp": datetime.now().isoformat(),
                "price_data": price_data,
                "technical_indicators": indicators,
                "technical_analysis": technical_analysis,
                "risk_analysis": risk_analysis,
                "news_sentiment": self._analyze_news_sentiment(news_data) if news_data else None,
                "ai_insights": ai_insights,
                "recommendation": await self._generate_recommendation(symbol, ai_insights)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing symbol {symbol}: {e}")
            raise

    async def make_trading_decision(self, symbol: str) -> Dict:
        """Make a trading decision for a symbol"""
        try:
            analysis = await self.analyze_symbol(symbol)
            
            # Calculate decision confidence based on multiple factors
            confidence_score = await self._calculate_confidence(analysis)
            
            # Generate decision
            decision = await self._make_decision(analysis, confidence_score)
            
            return {
                "symbol": symbol,
                "decision": decision["action"],  # "buy", "sell", "hold"
                "confidence": confidence_score,
                "reasoning": decision["reasoning"],
                "suggested_quantity": decision.get("quantity", 0),
                "risk_level": decision.get("risk_level", "medium"),
                "timestamp": datetime.now().isoformat(),
                "auto_execute": confidence_score >= settings.ai_confidence_threshold and self.auto_trading_enabled
            }
            
        except Exception as e:
            logger.error(f"Error making trading decision for {symbol}: {e}")
            raise

    async def _generate_ai_insights(
        self, symbol: str, price_data: Dict, indicators: Dict, 
        technical_analysis: Dict, risk_analysis: Dict, news_data: Optional[Dict]
    ) -> Dict:
        """Generate AI insights using GPT or rule-based analysis"""
        
        # Rule-based analysis (fallback if no OpenAI key)
        insights = {
            "trend_analysis": self._analyze_trend(technical_analysis),
            "momentum_analysis": self._analyze_momentum(indicators),
            "volatility_assessment": self._assess_volatility(risk_analysis),
            "support_resistance": self._analyze_support_resistance(technical_analysis),
            "volume_analysis": self._analyze_volume(indicators)
        }
        
        # If OpenAI is available, enhance with GPT analysis
        if self.openai_client and settings.openai_api_key:
            try:
                gpt_insights = await self._get_gpt_insights(symbol, price_data, indicators, technical_analysis, news_data)
                insights["gpt_analysis"] = gpt_insights
            except Exception as e:
                logger.warning(f"GPT analysis failed: {e}")
                insights["gpt_analysis"] = "GPT analysis unavailable"
        
        return insights

    def _analyze_trend(self, technical_analysis: Dict) -> str:
        """Analyze trend from technical data"""
        trend = technical_analysis.get("overall_trend", "unknown")
        price_changes = technical_analysis.get("price_changes", {})
        
        if trend == "bullish" and price_changes.get("1_week", 0) > 2:
            return "Strong uptrend confirmed by price action"
        elif trend == "bearish" and price_changes.get("1_week", 0) < -2:
            return "Strong downtrend confirmed by price action"
        elif trend == "sideways":
            return "Consolidation phase - waiting for breakout"
        else:
            return f"Trend: {trend}"

    def _analyze_momentum(self, indicators: Dict) -> str:
        """Analyze momentum indicators"""
        rsi = indicators.get("rsi", {})
        macd = indicators.get("macd", {})
        
        momentum_signals = []
        
        if rsi.get("oversold"):
            momentum_signals.append("RSI shows oversold conditions")
        elif rsi.get("overbought"):
            momentum_signals.append("RSI shows overbought conditions")
        
        if macd.get("bullish"):
            momentum_signals.append("MACD shows bullish momentum")
        
        return "; ".join(momentum_signals) if momentum_signals else "Neutral momentum"

    def _assess_volatility(self, risk_analysis: Dict) -> str:
        """Assess volatility and risk"""
        volatility = risk_analysis.get("volatility", 0)
        risk_rating = risk_analysis.get("risk_rating", "Unknown")
        
        return f"Volatility: {volatility}% - {risk_rating} risk"

    def _analyze_support_resistance(self, technical_analysis: Dict) -> str:
        """Analyze support and resistance levels"""
        sr = technical_analysis.get("support_resistance", {})
        
        if sr.get("support") and sr.get("resistance"):
            return f"Support at ${sr['support']}, Resistance at ${sr['resistance']}"
        else:
            return "Support/Resistance levels unclear"

    def _analyze_volume(self, indicators: Dict) -> str:
        """Analyze volume patterns"""
        volume = indicators.get("volume", {})
        
        if volume.get("volume_spike"):
            return "Unusual volume spike detected"
        else:
            return "Normal volume patterns"

    async def _get_gpt_insights(self, symbol: str, price_data: Dict, indicators: Dict, technical_analysis: Dict, news_data: Optional[Dict]) -> str:
        """Get insights from GPT"""
        try:
            # Prepare context for GPT
            context = f"""
            Analyze the following trading data for {symbol}:
            
            Current Price: ${price_data.get('price')} ({price_data.get('change_percent')}%)
            Volume: {price_data.get('volume')}
            
            Technical Indicators:
            - RSI: {indicators.get('rsi', {}).get('current')}
            - MACD: {indicators.get('macd', {})}
            - Moving Averages: {indicators.get('moving_averages', {})}
            
            Technical Analysis:
            - Trend: {technical_analysis.get('overall_trend')}
            - Volatility: {technical_analysis.get('volatility')}%
            - Support/Resistance: {technical_analysis.get('support_resistance', {})}
            
            News Sentiment: {self._analyze_news_sentiment(news_data) if news_data else 'No news data'}
            
            Provide a concise trading analysis and key insights.
            """
            
            response = await self.openai_client.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert financial analyst. Provide concise, actionable trading insights."},
                    {"role": "user", "content": context}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error getting GPT insights: {e}")
            return "GPT analysis unavailable"

    def _analyze_news_sentiment(self, news_data: Optional[Dict]) -> Dict:
        """Analyze news sentiment"""
        if not news_data or not news_data.get("articles"):
            return {"overall": "neutral", "score": 0.0, "article_count": 0}
        
        articles = news_data["articles"]
        sentiments = [article.get("sentiment", {}).get("polarity", 0) for article in articles]
        
        avg_sentiment = np.mean(sentiments) if sentiments else 0
        
        if avg_sentiment > 0.1:
            overall = "positive"
        elif avg_sentiment < -0.1:
            overall = "negative"
        else:
            overall = "neutral"
        
        return {
            "overall": overall,
            "score": round(avg_sentiment, 3),
            "article_count": len(articles),
            "positive_articles": len([s for s in sentiments if s > 0.1]),
            "negative_articles": len([s for s in sentiments if s < -0.1])
        }

    async def _calculate_confidence(self, analysis: Dict) -> float:
        """Calculate confidence score for trading decision"""
        confidence_factors = []
        
        # Technical indicators confidence
        indicators = analysis.get("technical_indicators", {})
        
        # RSI signals
        rsi = indicators.get("rsi", {})
        if rsi.get("oversold") or rsi.get("overbought"):
            confidence_factors.append(0.3)  # Strong RSI signal
        
        # MACD signals
        macd = indicators.get("macd", {})
        if macd.get("bullish"):
            confidence_factors.append(0.2)
        
        # Volume confirmation
        volume = indicators.get("volume", {})
        if volume.get("volume_spike"):
            confidence_factors.append(0.15)
        
        # Trend confirmation
        trend = analysis.get("technical_analysis", {}).get("overall_trend")
        if trend in ["bullish", "bearish"]:
            confidence_factors.append(0.2)
        
        # News sentiment
        news_sentiment = analysis.get("news_sentiment")
        if news_sentiment and abs(news_sentiment.get("score", 0)) > 0.2:
            confidence_factors.append(0.15)
        
        # Calculate final confidence
        base_confidence = min(sum(confidence_factors), 1.0)
        
        # Apply risk adjustment
        risk_analysis = analysis.get("risk_analysis", {})
        volatility = risk_analysis.get("volatility", 20)
        
        # Reduce confidence for high volatility
        if volatility > 40:
            base_confidence *= 0.7
        elif volatility > 25:
            base_confidence *= 0.85
        
        return round(min(max(base_confidence, 0.0), 1.0), 3)

    async def _make_decision(self, analysis: Dict, confidence: float) -> Dict:
        """Make trading decision based on analysis"""
        indicators = analysis.get("technical_indicators", {})
        technical = analysis.get("technical_analysis", {})
        news_sentiment = analysis.get("news_sentiment", {})
        
        # Decision logic
        buy_signals = 0
        sell_signals = 0
        reasoning_parts = []
        
        # RSI signals
        rsi = indicators.get("rsi", {})
        if rsi.get("oversold"):
            buy_signals += 2
            reasoning_parts.append("RSI oversold")
        elif rsi.get("overbought"):
            sell_signals += 2
            reasoning_parts.append("RSI overbought")
        
        # MACD signals
        if indicators.get("macd", {}).get("bullish"):
            buy_signals += 1
            reasoning_parts.append("MACD bullish")
        
        # Trend signals
        trend = technical.get("overall_trend")
        if trend == "bullish":
            buy_signals += 1
            reasoning_parts.append("Bullish trend")
        elif trend == "bearish":
            sell_signals += 1
            reasoning_parts.append("Bearish trend")
        
        # News sentiment
        if news_sentiment.get("overall") == "positive":
            buy_signals += 1
            reasoning_parts.append("Positive news sentiment")
        elif news_sentiment.get("overall") == "negative":
            sell_signals += 1
            reasoning_parts.append("Negative news sentiment")
        
        # Volume confirmation
        if indicators.get("volume", {}).get("volume_spike"):
            reasoning_parts.append("Volume spike")
        
        # Make decision
        if buy_signals > sell_signals and confidence >= 0.5:
            action = "buy"
            risk_level = "low" if confidence > 0.8 else "medium"
        elif sell_signals > buy_signals and confidence >= 0.5:
            action = "sell"
            risk_level = "low" if confidence > 0.8 else "medium"
        else:
            action = "hold"
            risk_level = "low"
        
        # Calculate suggested quantity based on confidence and risk
        if action in ["buy", "sell"]:
            base_quantity = int(settings.default_position_size / analysis.get("price_data", {}).get("price", 100))
            quantity = int(base_quantity * confidence)
        else:
            quantity = 0
        
        return {
            "action": action,
            "reasoning": "; ".join(reasoning_parts) or "Insufficient signals",
            "quantity": quantity,
            "risk_level": risk_level,
            "buy_signals": buy_signals,
            "sell_signals": sell_signals
        }

    async def _generate_recommendation(self, symbol: str, ai_insights: Dict) -> Dict:
        """Generate trading recommendation"""
        return {
            "action": "hold",  # Conservative default
            "confidence": "medium",
            "time_horizon": "short_term",
            "key_factors": list(ai_insights.keys()),
            "note": "Recommendation based on current market analysis"
        }

    async def chat(self, message: str, context: Optional[Dict] = None) -> str:
        """Chat with AI assistant"""
        try:
            if not self.openai_client or not settings.openai_api_key:
                return self._rule_based_chat_response(message, context)
            
            # Prepare context for GPT
            system_prompt = """You are an AI trading assistant. You help users with:
            - Market analysis and insights
            - Trading strategy discussions
            - Technical indicator explanations
            - Risk management advice
            - General trading questions
            
            Keep responses concise and actionable. Always remind users that trading involves risk."""
            
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add context if provided
            if context:
                context_msg = f"Current trading context: {json.dumps(context, indent=2)}"
                messages.append({"role": "user", "content": context_msg})
            
            messages.append({"role": "user", "content": message})
            
            response = await self.openai_client.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error in AI chat: {e}")
            return "I'm having trouble processing your request right now. Please try again later."

    def _rule_based_chat_response(self, message: str, context: Optional[Dict] = None) -> str:
        """Simple rule-based chat responses"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["rsi", "relative strength"]):
            return "RSI (Relative Strength Index) measures overbought/oversold conditions. Values above 70 suggest overbought, below 30 suggest oversold."
        
        elif any(word in message_lower for word in ["macd", "moving average convergence"]):
            return "MACD shows momentum and trend changes. When MACD line crosses above signal line, it's often bullish."
        
        elif any(word in message_lower for word in ["volume", "trading volume"]):
            return "Volume confirms price movements. High volume with price moves suggests strong conviction."
        
        elif any(word in message_lower for word in ["risk", "risk management"]):
            return "Always use stop losses, never risk more than 2% per trade, and diversify your portfolio."
        
        elif any(word in message_lower for word in ["buy", "sell", "trade"]):
            return "I can help analyze markets, but trading decisions should be based on your own research and risk tolerance."
        
        else:
            return "I'm here to help with trading analysis and questions. What would you like to know about market indicators, risk management, or trading strategies?"

    async def get_daily_recommendations(self) -> List[Dict]:
        """Get daily trading recommendations"""
        try:
            # Default watchlist
            watchlist = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
            recommendations = []
            
            for symbol in watchlist:
                try:
                    decision = await self.make_trading_decision(symbol)
                    if decision["confidence"] >= 0.6:  # Only include high-confidence recommendations
                        recommendations.append({
                            "symbol": symbol,
                            "action": decision["decision"],
                            "confidence": decision["confidence"],
                            "reasoning": decision["reasoning"][:100] + "..." if len(decision["reasoning"]) > 100 else decision["reasoning"]
                        })
                except Exception as e:
                    logger.warning(f"Error getting recommendation for {symbol}: {e}")
                    continue
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting daily recommendations: {e}")
            return []

    async def analyze_market_sentiment(self, symbol: str) -> Dict:
        """Analyze overall market sentiment for a symbol"""
        try:
            news_data = await self.market_service.get_market_news(symbol)
            sentiment = self._analyze_news_sentiment(news_data)
            
            # Add technical sentiment
            indicators = await self.market_service.get_technical_indicators(symbol)
            
            technical_sentiment = "neutral"
            if indicators.get("rsi", {}).get("oversold"):
                technical_sentiment = "bullish"
            elif indicators.get("rsi", {}).get("overbought"):
                technical_sentiment = "bearish"
            elif indicators.get("macd", {}).get("bullish"):
                technical_sentiment = "bullish"
            
            return {
                "symbol": symbol,
                "news_sentiment": sentiment,
                "technical_sentiment": technical_sentiment,
                "overall_sentiment": self._combine_sentiments(sentiment, technical_sentiment),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing market sentiment for {symbol}: {e}")
            raise

    def _combine_sentiments(self, news_sentiment: Dict, technical_sentiment: str) -> str:
        """Combine news and technical sentiment"""
        news_score = news_sentiment.get("score", 0)
        
        # Simple combination logic
        if news_score > 0.1 and technical_sentiment == "bullish":
            return "very_bullish"
        elif news_score < -0.1 and technical_sentiment == "bearish":
            return "very_bearish"
        elif news_score > 0.1 or technical_sentiment == "bullish":
            return "bullish"
        elif news_score < -0.1 or technical_sentiment == "bearish":
            return "bearish"
        else:
            return "neutral"

    async def toggle_auto_trading(self, enabled: bool) -> Dict:
        """Toggle automatic trading on/off"""
        self.auto_trading_enabled = enabled
        
        return {
            "auto_trading_enabled": self.auto_trading_enabled,
            "message": f"Automatic trading {'enabled' if enabled else 'disabled'}",
            "timestamp": datetime.now().isoformat()
        }

    async def get_auto_trading_status(self) -> Dict:
        """Get current auto trading status"""
        return {
            "enabled": self.auto_trading_enabled,
            "confidence_threshold": settings.ai_confidence_threshold,
            "max_trades_per_day": settings.ai_max_trades_per_day,
            "trading_mode": settings.trading_mode
        }