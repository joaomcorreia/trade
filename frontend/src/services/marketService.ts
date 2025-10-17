import axios from 'axios';
import { MarketData, TechnicalIndicators, NewsArticle, ChartData } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
});

export const marketService = {
    async getCurrentPrice(symbol: string): Promise<MarketData> {
        const response = await api.get(`/market/price/${symbol}`);
        return response.data;
    },

    async getHistoricalData(symbol: string, period: string = '1y', interval: string = '1d'): Promise<{ symbol: string, data: ChartData[] }> {
        const response = await api.get(`/market/historical/${symbol}`, {
            params: { period, interval }
        });
        return response.data;
    },

    async getTechnicalIndicators(symbol: string, period: string = '1y'): Promise<TechnicalIndicators> {
        const response = await api.get(`/market/indicators/${symbol}`, {
            params: { period }
        });
        return response.data;
    },

    async getWatchlist(): Promise<{ watchlist: MarketData[] }> {
        const response = await api.get('/market/watchlist');
        return response.data;
    },

    async getNews(symbol: string): Promise<{ symbol: string, articles: NewsArticle[], total_results: number }> {
        const response = await api.get(`/market/news/${symbol}`);
        return response.data;
    }
};