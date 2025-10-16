import asyncio
import pandas as pd
import numpy as np
from app.services.market_data import MarketDataService
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class AnalysisService:
    def __init__(self):
        self.market_service = MarketDataService()

    async def get_technical_analysis(self, symbol: str, period: str = "1y") -> Dict:
        """Get comprehensive technical analysis"""
        try:
            # Get indicators and historical data
            indicators = await self.market_service.get_technical_indicators(symbol, period)
            historical = await self.market_service.get_historical_data(symbol, period)
            
            # Analyze trends
            df = pd.DataFrame(historical["data"])
            df['close'] = pd.to_numeric(df['close'])
            
            # Calculate price changes
            price_change_1d = df['close'].pct_change().iloc[-1] * 100
            price_change_1w = df['close'].pct_change(periods=7).iloc[-1] * 100 if len(df) >= 7 else 0
            price_change_1m = df['close'].pct_change(periods=30).iloc[-1] * 100 if len(df) >= 30 else 0
            
            # Support and resistance levels
            support_resistance = self._calculate_support_resistance(df['close'])
            
            # Technical signals
            signals = self._generate_technical_signals(indicators)
            
            return {
                "symbol": symbol,
                "price_changes": {
                    "1_day": round(price_change_1d, 2),
                    "1_week": round(price_change_1w, 2),
                    "1_month": round(price_change_1m, 2)
                },
                "support_resistance": support_resistance,
                "indicators": indicators,
                "signals": signals,
                "overall_trend": self._determine_trend(df['close']),
                "volatility": self._calculate_volatility(df['close'])
            }
            
        except Exception as e:
            logger.error(f"Error in technical analysis for {symbol}: {e}")
            raise

    def _calculate_support_resistance(self, prices: pd.Series) -> Dict:
        """Calculate support and resistance levels"""
        try:
            # Simple method using recent highs and lows
            recent_high = prices.tail(20).max()
            recent_low = prices.tail(20).min()
            
            # Pivot points
            pivot = (recent_high + recent_low + prices.iloc[-1]) / 3
            resistance1 = 2 * pivot - recent_low
            support1 = 2 * pivot - recent_high
            
            return {
                "resistance": round(resistance1, 2),
                "support": round(support1, 2),
                "pivot": round(pivot, 2),
                "recent_high": round(recent_high, 2),
                "recent_low": round(recent_low, 2)
            }
        except:
            return {"resistance": None, "support": None, "pivot": None}

    def _generate_technical_signals(self, indicators: Dict) -> List[Dict]:
        """Generate trading signals from indicators"""
        signals = []
        
        try:
            rsi_data = indicators.get("rsi", {})
            macd_data = indicators.get("macd", {})
            volume_data = indicators.get("volume", {})
            
            # RSI signals
            if rsi_data.get("oversold"):
                signals.append({
                    "type": "buy",
                    "indicator": "RSI",
                    "message": f"RSI oversold at {rsi_data.get('current')}",
                    "strength": "strong"
                })
            elif rsi_data.get("overbought"):
                signals.append({
                    "type": "sell",
                    "indicator": "RSI",
                    "message": f"RSI overbought at {rsi_data.get('current')}",
                    "strength": "strong"
                })
            
            # MACD signals
            if macd_data.get("bullish"):
                signals.append({
                    "type": "buy",
                    "indicator": "MACD",
                    "message": "MACD bullish crossover",
                    "strength": "medium"
                })
            
            # Volume signals
            if volume_data.get("volume_spike"):
                signals.append({
                    "type": "watch",
                    "indicator": "Volume",
                    "message": "Unusual volume detected",
                    "strength": "medium"
                })
            
        except Exception as e:
            logger.error(f"Error generating signals: {e}")
        
        return signals

    def _determine_trend(self, prices: pd.Series) -> str:
        """Determine overall trend"""
        try:
            if len(prices) < 20:
                return "insufficient_data"
            
            recent_avg = prices.tail(10).mean()
            older_avg = prices.iloc[-30:-20].mean() if len(prices) >= 30 else prices.head(10).mean()
            
            if recent_avg > older_avg * 1.02:
                return "bullish"
            elif recent_avg < older_avg * 0.98:
                return "bearish"
            else:
                return "sideways"
        except:
            return "unknown"

    def _calculate_volatility(self, prices: pd.Series) -> float:
        """Calculate price volatility"""
        try:
            returns = prices.pct_change().dropna()
            volatility = returns.std() * np.sqrt(252) * 100  # Annualized volatility
            return round(volatility, 2)
        except:
            return 0.0

    async def get_fundamental_analysis(self, symbol: str) -> Dict:
        """Get fundamental analysis (simplified)"""
        try:
            # This would typically fetch from financial data providers
            # For demo, we'll return basic structure
            return {
                "symbol": symbol,
                "market_cap": "N/A",
                "pe_ratio": "N/A",
                "dividend_yield": "N/A",
                "revenue_growth": "N/A",
                "profit_margin": "N/A",
                "debt_to_equity": "N/A",
                "roe": "N/A",
                "note": "Fundamental data requires additional data provider integration"
            }
        except Exception as e:
            logger.error(f"Error in fundamental analysis for {symbol}: {e}")
            raise

    async def get_risk_analysis(self, symbol: str) -> Dict:
        """Get risk analysis"""
        try:
            historical = await self.market_service.get_historical_data(symbol, "1y")
            df = pd.DataFrame(historical["data"])
            df['close'] = pd.to_numeric(df['close'])
            
            # Calculate various risk metrics
            returns = df['close'].pct_change().dropna()
            
            # Value at Risk (95% confidence)
            var_95 = np.percentile(returns, 5) * 100
            
            # Maximum drawdown
            cumulative = (1 + returns).cumprod()
            running_max = cumulative.cummax()
            drawdown = (cumulative - running_max) / running_max
            max_drawdown = drawdown.min() * 100
            
            # Sharpe ratio (simplified, assuming 0% risk-free rate)
            sharpe_ratio = returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0
            
            # Beta (vs SPY as market proxy)
            try:
                spy_data = await self.market_service.get_historical_data("SPY", "1y")
                spy_df = pd.DataFrame(spy_data["data"])
                spy_df['close'] = pd.to_numeric(spy_df['close'])
                spy_returns = spy_df['close'].pct_change().dropna()
                
                # Align dates
                min_length = min(len(returns), len(spy_returns))
                if min_length > 30:
                    covariance = np.cov(returns.tail(min_length), spy_returns.tail(min_length))[0][1]
                    market_variance = np.var(spy_returns.tail(min_length))
                    beta = covariance / market_variance if market_variance > 0 else 1.0
                else:
                    beta = 1.0
            except:
                beta = 1.0
            
            return {
                "symbol": symbol,
                "var_95": round(var_95, 2),
                "max_drawdown": round(max_drawdown, 2),
                "volatility": round(returns.std() * np.sqrt(252) * 100, 2),
                "sharpe_ratio": round(sharpe_ratio, 2),
                "beta": round(beta, 2),
                "risk_rating": self._get_risk_rating(returns.std() * np.sqrt(252) * 100)
            }
            
        except Exception as e:
            logger.error(f"Error in risk analysis for {symbol}: {e}")
            raise

    def _get_risk_rating(self, volatility: float) -> str:
        """Get risk rating based on volatility"""
        if volatility < 15:
            return "Low"
        elif volatility < 25:
            return "Medium"
        elif volatility < 40:
            return "High"
        else:
            return "Very High"

    async def get_correlation_analysis(self, symbols: List[str], period: str = "1y") -> Dict:
        """Get correlation analysis between symbols"""
        try:
            correlation_matrix = {}
            price_data = {}
            
            # Fetch price data for all symbols
            for symbol in symbols:
                try:
                    historical = await self.market_service.get_historical_data(symbol, period)
                    df = pd.DataFrame(historical["data"])
                    price_data[symbol] = pd.to_numeric(df['close'])
                except:
                    continue
            
            # Calculate correlations
            if len(price_data) >= 2:
                # Align data by creating a DataFrame
                aligned_data = pd.DataFrame(price_data)
                correlation_matrix = aligned_data.corr().round(3).to_dict()
            
            return {
                "symbols": symbols,
                "correlation_matrix": correlation_matrix,
                "period": period
            }
            
        except Exception as e:
            logger.error(f"Error in correlation analysis: {e}")
            raise

    async def screen_stocks(self, criteria: Dict) -> Dict:
        """Screen stocks based on criteria"""
        try:
            # Default watchlist for screening
            watchlist = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "NVDA", "META", "NFLX", "AMD", "CRM"]
            
            results = []
            
            for symbol in watchlist:
                try:
                    price_data = await self.market_service.get_current_price(symbol)
                    indicators = await self.market_service.get_technical_indicators(symbol)
                    
                    # Apply filters
                    passes_filter = True
                    
                    if criteria.get("min_price") and price_data["price"] < criteria["min_price"]:
                        passes_filter = False
                    
                    if criteria.get("max_price") and price_data["price"] > criteria["max_price"]:
                        passes_filter = False
                    
                    if criteria.get("min_volume") and price_data["volume"] < criteria["min_volume"]:
                        passes_filter = False
                    
                    if criteria.get("rsi_oversold") and not indicators.get("rsi", {}).get("oversold"):
                        passes_filter = False
                    
                    if criteria.get("rsi_overbought") and not indicators.get("rsi", {}).get("overbought"):
                        passes_filter = False
                    
                    if passes_filter:
                        results.append({
                            "symbol": symbol,
                            "price": price_data["price"],
                            "change_percent": price_data["change_percent"],
                            "volume": price_data["volume"],
                            "rsi": indicators.get("rsi", {}).get("current"),
                            "macd_bullish": indicators.get("macd", {}).get("bullish")
                        })
                        
                except Exception as e:
                    logger.warning(f"Error screening {symbol}: {e}")
                    continue
            
            return {
                "criteria": criteria,
                "results": results,
                "total_found": len(results)
            }
            
        except Exception as e:
            logger.error(f"Error in stock screening: {e}")
            raise