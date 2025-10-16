import React, { useState, useEffect } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip
} from '@mui/material';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale
} from 'chart.js';
import 'chartjs-adapter-date-fns';
import { marketService } from '../services/marketService';
import { tradingService, TradeRequest } from '../services/tradingService';
import { MarketData, TechnicalIndicators, ChartData } from '../types';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale
);

interface TradingDashboardProps {
  onTradeExecuted: () => void;
  onNotification: (message: string) => void;
}

const TradingDashboard: React.FC<TradingDashboardProps> = ({ onTradeExecuted, onNotification }) => {
  const [selectedSymbol, setSelectedSymbol] = useState('AAPL');
  const [marketData, setMarketData] = useState<MarketData | null>(null);
  const [indicators, setIndicators] = useState<TechnicalIndicators | null>(null);
  const [chartData, setChartData] = useState<ChartData[]>([]);
  const [watchlist, setWatchlist] = useState<MarketData[]>([]);
  const [tradeQuantity, setTradeQuantity] = useState<number>(10);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadWatchlist();
    loadSymbolData(selectedSymbol);
  }, []);

  useEffect(() => {
    loadSymbolData(selectedSymbol);
  }, [selectedSymbol]);

  const loadWatchlist = async () => {
    try {
      const data = await marketService.getWatchlist();
      setWatchlist(data.watchlist);
    } catch (error) {
      console.error('Error loading watchlist:', error);
    }
  };

  const loadSymbolData = async (symbol: string) => {
    setLoading(true);
    try {
      const [priceData, indicatorData, historicalData] = await Promise.all([
        marketService.getCurrentPrice(symbol),
        marketService.getTechnicalIndicators(symbol),
        marketService.getHistoricalData(symbol, '3m', '1d')
      ]);

      setMarketData(priceData);
      setIndicators(indicatorData);
      setChartData(historicalData.data);
    } catch (error) {
      console.error('Error loading symbol data:', error);
      onNotification('Error loading market data');
    } finally {
      setLoading(false);
    }
  };

  const executeTrade = async (action: 'buy' | 'sell') => {
    if (!marketData) return;

    try {
      const tradeRequest: TradeRequest = {
        symbol: selectedSymbol,
        action,
        quantity: tradeQuantity,
        order_type: 'market'
      };

      await tradingService.executeTrade(tradeRequest);
      onTradeExecuted();
      onNotification(`${action.toUpperCase()} order executed for ${tradeQuantity} shares of ${selectedSymbol}`);
    } catch (error) {
      console.error('Error executing trade:', error);
      onNotification('Error executing trade');
    }
  };

  const getChartData = () => {
    return {
      labels: chartData.map(d => new Date(d.timestamp)),
      datasets: [
        {
          label: 'Price',
          data: chartData.map(d => d.close),
          borderColor: 'rgb(75, 192, 192)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          tension: 0.1
        }
      ]
    };
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: `${selectedSymbol} Price Chart`
      }
    },
    scales: {
      x: {
        type: 'time' as const,
        time: {
          unit: 'day' as const
        }
      },
      y: {
        beginAtZero: false
      }
    }
  };

  return (
    <Grid container spacing={3}>
      {/* Symbol Selection */}
      <Grid item xs={12}>
        <Paper sx={{ p: 2 }}>
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', mb: 2 }}>
            <FormControl sx={{ minWidth: 120 }}>
              <InputLabel>Symbol</InputLabel>
              <Select
                value={selectedSymbol}
                label="Symbol"
                onChange={(e) => setSelectedSymbol(e.target.value)}
              >
                {watchlist.map((stock) => (
                  <MenuItem key={stock.symbol} value={stock.symbol}>
                    {stock.symbol}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <Button variant="outlined" onClick={() => loadSymbolData(selectedSymbol)}>
              Refresh
            </Button>
          </Box>
        </Paper>
      </Grid>

      {/* Market Data */}
      {marketData && (
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Box sx={{ mb: 2 }}>
              <Typography variant="h5" gutterBottom>
                {marketData.symbol} - ${marketData.price}
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                <Chip 
                  label={`${marketData.change >= 0 ? '+' : ''}$${marketData.change.toFixed(2)}`}
                  color={marketData.change >= 0 ? 'success' : 'error'}
                />
                <Chip 
                  label={`${marketData.change_percent >= 0 ? '+' : ''}${marketData.change_percent.toFixed(2)}%`}
                  color={marketData.change_percent >= 0 ? 'success' : 'error'}
                />
                <Chip label={`Volume: ${marketData.volume.toLocaleString()}`} />
              </Box>
            </Box>
            
            <Box sx={{ height: 400 }}>
              {chartData.length > 0 && (
                <Line data={getChartData()} options={chartOptions} />
              )}
            </Box>
          </Paper>
        </Grid>
      )}

      {/* Trading Panel */}
      <Grid item xs={12} md={4}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Quick Trade
          </Typography>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              label="Quantity"
              type="number"
              value={tradeQuantity}
              onChange={(e) => setTradeQuantity(Number(e.target.value))}
              fullWidth
            />
            <Button 
              variant="contained" 
              color="success"
              onClick={() => executeTrade('buy')}
              fullWidth
            >
              BUY
            </Button>
            <Button 
              variant="contained" 
              color="error"
              onClick={() => executeTrade('sell')}
              fullWidth
            >
              SELL
            </Button>
          </Box>
        </Paper>

        {/* Technical Indicators */}
        {indicators && (
          <Paper sx={{ p: 2, mt: 2 }}>
            <Typography variant="h6" gutterBottom>
              Technical Indicators
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="body2">RSI:</Typography>
                <Chip 
                  label={indicators.rsi.current?.toFixed(2) || 'N/A'}
                  color={indicators.rsi.overbought ? 'error' : indicators.rsi.oversold ? 'success' : 'default'}
                  size="small"
                />
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="body2">MACD:</Typography>
                <Chip 
                  label={indicators.macd.bullish ? 'Bullish' : 'Bearish'}
                  color={indicators.macd.bullish ? 'success' : 'error'}
                  size="small"
                />
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="body2">Volume:</Typography>
                <Chip 
                  label={indicators.volume.volume_spike ? 'High' : 'Normal'}
                  color={indicators.volume.volume_spike ? 'warning' : 'default'}
                  size="small"
                />
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="body2">SMA 20:</Typography>
                <Typography variant="body2">
                  ${indicators.moving_averages.sma_20?.toFixed(2) || 'N/A'}
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="body2">SMA 50:</Typography>
                <Typography variant="body2">
                  ${indicators.moving_averages.sma_50?.toFixed(2) || 'N/A'}
                </Typography>
              </Box>
            </Box>
          </Paper>
        )}
      </Grid>

      {/* Watchlist */}
      <Grid item xs={12}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Watchlist
          </Typography>
          <Grid container spacing={2}>
            {watchlist.map((stock) => (
              <Grid item xs={12} sm={6} md={3} key={stock.symbol}>
                <Card 
                  sx={{ 
                    cursor: 'pointer',
                    '&:hover': { boxShadow: 4 },
                    bgcolor: selectedSymbol === stock.symbol ? 'action.selected' : 'background.paper'
                  }}
                  onClick={() => setSelectedSymbol(stock.symbol)}
                >
                  <CardContent sx={{ p: 2 }}>
                    <Typography variant="h6">{stock.symbol}</Typography>
                    <Typography variant="h5">${stock.price}</Typography>
                    <Typography 
                      variant="body2" 
                      color={stock.change_percent >= 0 ? 'success.main' : 'error.main'}
                    >
                      {stock.change_percent >= 0 ? '+' : ''}{stock.change_percent.toFixed(2)}%
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Paper>
      </Grid>
    </Grid>
  );
};

export default TradingDashboard;