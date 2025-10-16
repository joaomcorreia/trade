import axios from 'axios';
import { AIDecision } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export interface AIAnalysisRequest {
  symbol: string;
  timeframe?: string;
  include_news?: boolean;
}

export interface AIChatRequest {
  message: string;
  context?: any;
}

export const aiService = {
  async analyzeSymbol(request: AIAnalysisRequest): Promise<any> {
    const response = await api.post('/ai/analyze', request);
    return response.data;
  },

  async getTradingDecision(symbol: string): Promise<AIDecision> {
    const response = await api.post(`/ai/decision?symbol=${symbol}`);
    return response.data;
  },

  async chat(request: AIChatRequest): Promise<{response: string}> {
    const response = await api.post('/ai/chat', request);
    return response.data;
  },

  async getRecommendations(): Promise<{recommendations: any[]}> {
    const response = await api.get('/ai/recommendations');
    return response.data;
  },

  async getMarketSentiment(symbol: string): Promise<any> {
    const response = await api.get(`/ai/sentiment/${symbol}`);
    return response.data;
  },

  async toggleAutoTrading(enabled: boolean): Promise<any> {
    const response = await api.post('/ai/auto-trade/toggle', null, {
      params: { enabled }
    });
    return response.data;
  },

  async getAutoTradingStatus(): Promise<any> {
    const response = await api.get('/ai/auto-trade/status');
    return response.data;
  }
};