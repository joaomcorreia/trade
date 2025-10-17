import React, { useState, useEffect } from 'react';
import {
    Grid,
    Paper,
    Typography,
    Box,
    Card,
    CardContent,
    Button,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Chip,
    IconButton
} from '@mui/material';
import { Close as CloseIcon, Refresh as RefreshIcon } from '@mui/icons-material';
import { tradingService } from '../services/tradingService';
import { PortfolioSummary, Position, Trade } from '../types';

interface PortfolioProps {
    portfolioSummary: PortfolioSummary | null;
    onPortfolioChange: () => void;
    onNotification: (message: string) => void;
}

const Portfolio: React.FC<PortfolioProps> = ({ portfolioSummary, onPortfolioChange, onNotification }) => {
    const [positions, setPositions] = useState<Position[]>([]);
    const [trades, setTrades] = useState<Trade[]>([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadPositions();
        loadTradeHistory();
    }, []);

    const loadPositions = async () => {
        try {
            const response = await tradingService.getPositions();
            setPositions(response.positions);
        } catch (error) {
            console.error('Error loading positions:', error);
            onNotification('Error loading positions');
        }
    };

    const loadTradeHistory = async () => {
        try {
            const response = await tradingService.getTradeHistory(20);
            setTrades(response.trades);
        } catch (error) {
            console.error('Error loading trade history:', error);
            onNotification('Error loading trade history');
        }
    };

    const closePosition = async (symbol: string) => {
        setLoading(true);
        try {
            await tradingService.closePosition(symbol);
            onPortfolioChange();
            loadPositions();
            onNotification(`Position closed for ${symbol}`);
        } catch (error) {
            console.error('Error closing position:', error);
            onNotification('Error closing position');
        } finally {
            setLoading(false);
        }
    };

    const refreshData = async () => {
        setLoading(true);
        try {
            await Promise.all([loadPositions(), loadTradeHistory()]);
            onPortfolioChange();
        } catch (error) {
            console.error('Error refreshing data:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Grid container spacing={3}>
            {/* Portfolio Summary */}
            {portfolioSummary && (
                <Grid item xs={12}>
                    <Paper sx={{ p: 3 }}>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                            <Typography variant="h5" gutterBottom>
                                Portfolio Summary
                            </Typography>
                            <IconButton onClick={refreshData} disabled={loading}>
                                <RefreshIcon />
                            </IconButton>
                        </Box>

                        <Grid container spacing={3}>
                            <Grid item xs={12} sm={6} md={3}>
                                <Card>
                                    <CardContent>
                                        <Typography color="textSecondary" gutterBottom>
                                            Total Value
                                        </Typography>
                                        <Typography variant="h5">
                                            ${portfolioSummary.total_value.toLocaleString()}
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Grid>

                            <Grid item xs={12} sm={6} md={3}>
                                <Card>
                                    <CardContent>
                                        <Typography color="textSecondary" gutterBottom>
                                            Total P&L
                                        </Typography>
                                        <Typography
                                            variant="h5"
                                            color={portfolioSummary.total_pnl >= 0 ? 'success.main' : 'error.main'}
                                        >
                                            {portfolioSummary.total_pnl >= 0 ? '+' : ''}${portfolioSummary.total_pnl.toLocaleString()}
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Grid>

                            <Grid item xs={12} sm={6} md={3}>
                                <Card>
                                    <CardContent>
                                        <Typography color="textSecondary" gutterBottom>
                                            Return %
                                        </Typography>
                                        <Typography
                                            variant="h5"
                                            color={portfolioSummary.total_return_percent >= 0 ? 'success.main' : 'error.main'}
                                        >
                                            {portfolioSummary.total_return_percent >= 0 ? '+' : ''}{portfolioSummary.total_return_percent}%
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Grid>

                            <Grid item xs={12} sm={6} md={3}>
                                <Card>
                                    <CardContent>
                                        <Typography color="textSecondary" gutterBottom>
                                            Win Rate
                                        </Typography>
                                        <Typography variant="h5">
                                            {portfolioSummary.win_rate}%
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Grid>
                        </Grid>
                    </Paper>
                </Grid>
            )}

            {/* Current Positions */}
            <Grid item xs={12}>
                <Paper sx={{ p: 3 }}>
                    <Typography variant="h6" gutterBottom>
                        Current Positions
                    </Typography>

                    {positions.length > 0 ? (
                        <TableContainer>
                            <Table>
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Symbol</TableCell>
                                        <TableCell align="right">Quantity</TableCell>
                                        <TableCell align="right">Avg Price</TableCell>
                                        <TableCell align="right">Current Price</TableCell>
                                        <TableCell align="right">Market Value</TableCell>
                                        <TableCell align="right">P&L</TableCell>
                                        <TableCell align="right">P&L %</TableCell>
                                        <TableCell align="center">Actions</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {positions.map((position) => (
                                        <TableRow key={position.symbol}>
                                            <TableCell component="th" scope="row">
                                                <Typography variant="subtitle2">{position.symbol}</Typography>
                                            </TableCell>
                                            <TableCell align="right">{position.quantity}</TableCell>
                                            <TableCell align="right">${position.avg_price.toFixed(2)}</TableCell>
                                            <TableCell align="right">${position.current_price.toFixed(2)}</TableCell>
                                            <TableCell align="right">${position.market_value.toLocaleString()}</TableCell>
                                            <TableCell align="right">
                                                <Typography
                                                    color={position.unrealized_pnl >= 0 ? 'success.main' : 'error.main'}
                                                >
                                                    {position.unrealized_pnl >= 0 ? '+' : ''}${position.unrealized_pnl.toFixed(2)}
                                                </Typography>
                                            </TableCell>
                                            <TableCell align="right">
                                                <Chip
                                                    label={`${position.unrealized_pnl_percent >= 0 ? '+' : ''}${position.unrealized_pnl_percent.toFixed(2)}%`}
                                                    color={position.unrealized_pnl_percent >= 0 ? 'success' : 'error'}
                                                    size="small"
                                                />
                                            </TableCell>
                                            <TableCell align="center">
                                                <IconButton
                                                    size="small"
                                                    color="error"
                                                    onClick={() => closePosition(position.symbol)}
                                                    disabled={loading}
                                                >
                                                    <CloseIcon />
                                                </IconButton>
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    ) : (
                        <Typography variant="body2" color="textSecondary">
                            No current positions
                        </Typography>
                    )}
                </Paper>
            </Grid>

            {/* Trade History */}
            <Grid item xs={12}>
                <Paper sx={{ p: 3 }}>
                    <Typography variant="h6" gutterBottom>
                        Recent Trades
                    </Typography>

                    {trades.length > 0 ? (
                        <TableContainer>
                            <Table>
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Date</TableCell>
                                        <TableCell>Symbol</TableCell>
                                        <TableCell>Action</TableCell>
                                        <TableCell align="right">Quantity</TableCell>
                                        <TableCell align="right">Price</TableCell>
                                        <TableCell align="right">P&L</TableCell>
                                        <TableCell>Status</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {trades.map((trade) => (
                                        <TableRow key={trade.id}>
                                            <TableCell>
                                                {new Date(trade.timestamp).toLocaleDateString()}
                                            </TableCell>
                                            <TableCell>{trade.symbol}</TableCell>
                                            <TableCell>
                                                <Chip
                                                    label={trade.action.toUpperCase()}
                                                    color={trade.action === 'buy' ? 'success' : 'error'}
                                                    size="small"
                                                />
                                            </TableCell>
                                            <TableCell align="right">{trade.quantity}</TableCell>
                                            <TableCell align="right">${trade.price.toFixed(2)}</TableCell>
                                            <TableCell align="right">
                                                {trade.pnl !== null && trade.pnl !== 0 && (
                                                    <Typography
                                                        color={trade.pnl >= 0 ? 'success.main' : 'error.main'}
                                                    >
                                                        {trade.pnl >= 0 ? '+' : ''}${trade.pnl.toFixed(2)}
                                                    </Typography>
                                                )}
                                            </TableCell>
                                            <TableCell>
                                                <Chip
                                                    label={trade.status}
                                                    color={trade.status === 'executed' ? 'success' : 'default'}
                                                    size="small"
                                                />
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    ) : (
                        <Typography variant="body2" color="textSecondary">
                            No trade history
                        </Typography>
                    )}
                </Paper>
            </Grid>
        </Grid>
    );
};

export default Portfolio;