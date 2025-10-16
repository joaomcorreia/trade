import axios from 'axios';
import { Trade, Position, PortfolioSummary } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export interface TradeRequest {
  symbol: string;
  action: string;
  quantity: number;
  order_type?: string;
  limit_price?: number;
}

export const tradingService = {
  async executeTrade(tradeRequest: TradeRequest): Promise<any> {
    const response = await api.post('/trading/execute', tradeRequest);
    return response.data;
  },

  async getPositions(): Promise<{positions: Position[]}> {
    const response = await api.get('/trading/positions');
    return response.data;
  },

  async getTradeHistory(limit: number = 50, offset: number = 0): Promise<{trades: Trade[], total: number}> {
    const response = await api.get('/trading/trades', {
      params: { limit, offset }
    });
    return response.data;
  },

  async getPortfolioSummary(): Promise<PortfolioSummary> {
    const response = await api.get('/trading/portfolio');
    return response.data;
  },

  async closePosition(symbol: string): Promise<any> {
    const response = await api.delete(`/trading/position/${symbol}`);
    return response.data;
  }
};