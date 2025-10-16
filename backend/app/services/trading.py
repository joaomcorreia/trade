import asyncio
from sqlalchemy.orm import Session
from app.models.trade import Trade
from app.models.portfolio import Portfolio
from app.services.market_data import MarketDataService
from app.core.config import settings
from typing import Dict, List, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class TradingService:
    def __init__(self, db: Session):
        self.db = db
        self.market_service = MarketDataService()

    async def execute_trade(
        self, 
        symbol: str, 
        action: str, 
        quantity: int, 
        order_type: str = "market",
        limit_price: Optional[float] = None
    ) -> Dict:
        """Execute a trade"""
        try:
            # Get current price
            price_data = await self.market_service.get_current_price(symbol)
            current_price = price_data["price"]
            
            # For demo purposes, we'll use current price for market orders
            execution_price = limit_price if order_type == "limit" and limit_price else current_price
            
            # Calculate fees (0.1% commission)
            fees = execution_price * quantity * 0.001
            
            # Create trade record
            trade = Trade(
                symbol=symbol,
                action=action,
                quantity=quantity,
                price=execution_price,
                order_type=order_type,
                status="executed",
                fees=fees,
                ai_decision=False
            )
            
            self.db.add(trade)
            
            # Update portfolio
            await self._update_portfolio(symbol, action, quantity, execution_price)
            
            self.db.commit()
            
            logger.info(f"Trade executed: {action} {quantity} {symbol} at ${execution_price}")
            
            return {
                "trade_id": trade.id,
                "symbol": symbol,
                "action": action,
                "quantity": quantity,
                "price": execution_price,
                "fees": fees,
                "status": "executed",
                "timestamp": trade.timestamp.isoformat()
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error executing trade: {e}")
            raise

    async def _update_portfolio(self, symbol: str, action: str, quantity: int, price: float):
        """Update portfolio after trade execution"""
        portfolio_item = self.db.query(Portfolio).filter(Portfolio.symbol == symbol).first()
        
        if not portfolio_item:
            # New position
            if action == "buy":
                portfolio_item = Portfolio(
                    symbol=symbol,
                    quantity=quantity,
                    avg_price=price
                )
                self.db.add(portfolio_item)
        else:
            # Update existing position
            if action == "buy":
                # Add to position
                total_cost = (portfolio_item.quantity * portfolio_item.avg_price) + (quantity * price)
                total_quantity = portfolio_item.quantity + quantity
                portfolio_item.avg_price = total_cost / total_quantity
                portfolio_item.quantity = total_quantity
            elif action == "sell":
                # Reduce position
                portfolio_item.quantity -= quantity
                if portfolio_item.quantity <= 0:
                    # Close position
                    self.db.delete(portfolio_item)

    async def get_positions(self) -> List[Dict]:
        """Get current portfolio positions"""
        try:
            positions = self.db.query(Portfolio).all()
            position_list = []
            
            for position in positions:
                # Get current price
                price_data = await self.market_service.get_current_price(position.symbol)
                current_price = price_data["price"]
                
                market_value = position.quantity * current_price
                cost_basis = position.quantity * position.avg_price
                unrealized_pnl = market_value - cost_basis
                
                position_list.append({
                    "symbol": position.symbol,
                    "quantity": position.quantity,
                    "avg_price": round(position.avg_price, 2),
                    "current_price": current_price,
                    "market_value": round(market_value, 2),
                    "cost_basis": round(cost_basis, 2),
                    "unrealized_pnl": round(unrealized_pnl, 2),
                    "unrealized_pnl_percent": round((unrealized_pnl / cost_basis) * 100, 2) if cost_basis > 0 else 0
                })
            
            return position_list
            
        except Exception as e:
            logger.error(f"Error getting positions: {e}")
            raise

    async def get_portfolio_summary(self) -> Dict:
        """Get portfolio summary"""
        try:
            positions = await self.get_positions()
            
            total_value = sum(pos["market_value"] for pos in positions)
            total_cost = sum(pos["cost_basis"] for pos in positions)
            total_pnl = sum(pos["unrealized_pnl"] for pos in positions)
            
            # Get realized P&L from closed trades
            trades = self.db.query(Trade).all()
            realized_pnl = sum(trade.pnl for trade in trades if trade.pnl is not None)
            
            # Calculate some basic metrics
            total_trades = len(trades)
            winning_trades = len([t for t in trades if t.pnl and t.pnl > 0])
            win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
            
            return {
                "total_value": round(total_value, 2),
                "total_cost": round(total_cost, 2),
                "unrealized_pnl": round(total_pnl, 2),
                "realized_pnl": round(realized_pnl, 2),
                "total_pnl": round(total_pnl + realized_pnl, 2),
                "total_return_percent": round((total_pnl / total_cost) * 100, 2) if total_cost > 0 else 0,
                "positions_count": len(positions),
                "total_trades": total_trades,
                "winning_trades": winning_trades,
                "win_rate": round(win_rate, 2),
                "positions": positions
            }
            
        except Exception as e:
            logger.error(f"Error getting portfolio summary: {e}")
            raise

    async def close_position(self, symbol: str) -> Dict:
        """Close entire position for a symbol"""
        try:
            portfolio_item = self.db.query(Portfolio).filter(Portfolio.symbol == symbol).first()
            
            if not portfolio_item:
                raise Exception(f"No position found for {symbol}")
            
            # Execute sell order for entire position
            result = await self.execute_trade(
                symbol=symbol,
                action="sell",
                quantity=portfolio_item.quantity,
                order_type="market"
            )
            
            return {
                "message": f"Position closed for {symbol}",
                "trade": result
            }
            
        except Exception as e:
            logger.error(f"Error closing position for {symbol}: {e}")
            raise