export interface MarketData {
  symbol: string;
  price: number;
  change: number;
  change_percent: number;
  volume: number;
  high: number;
  low: number;
  open: number;
  timestamp: string;
}

export interface TechnicalIndicators {
  symbol: string;
  rsi: {
    current: number;
    overbought: boolean;
    oversold: boolean;
    history: number[];
  };
  macd: {
    macd: number;
    signal: number;
    histogram: number;
    bullish: boolean;
  };
  moving_averages: {
    sma_20: number;
    sma_50: number;
    ema_12: number;
    ema_26: number;
  };
  bollinger_bands: {
    upper: number;
    middle: number;
    lower: number;
  };
  volume: {
    current: number;
    average: number;
    volume_spike: boolean;
  };
}

export interface NewsArticle {
  title: string;
  description: string;
  url: string;
  published_at: string;
  source: string;
  sentiment: {
    sentiment: string;
    polarity: number;
    subjectivity: number;
  };
}

export interface Trade {
  id: number;
  symbol: string;
  action: string;
  quantity: number;
  price: number;
  timestamp: string;
  pnl: number;
  status: string;
}

export interface Position {
  symbol: string;
  quantity: number;
  avg_price: number;
  current_price: number;
  market_value: number;
  cost_basis: number;
  unrealized_pnl: number;
  unrealized_pnl_percent: number;
}

export interface AIDecision {
  symbol: string;
  decision: string;
  confidence: number;
  reasoning: string;
  suggested_quantity: number;
  risk_level: string;
  timestamp: string;
  auto_execute: boolean;
}

export interface PortfolioSummary {
  total_value: number;
  total_cost: number;
  unrealized_pnl: number;
  realized_pnl: number;
  total_pnl: number;
  total_return_percent: number;
  positions_count: number;
  total_trades: number;
  winning_trades: number;
  win_rate: number;
  positions: Position[];
}

export interface ChartData {
  timestamp: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}