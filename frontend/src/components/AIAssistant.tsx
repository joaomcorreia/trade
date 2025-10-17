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
    List,
    ListItem,
    ListItemText,
    Chip,
    Avatar,
    Divider,
    Switch,
    FormControlLabel,
    Alert
} from '@mui/material';
import {
    SmartToy as AIIcon,
    Person as PersonIcon,
    TrendingUp as TrendingUpIcon,
    TrendingDown as TrendingDownIcon
} from '@mui/icons-material';
import { aiService, AIChatRequest } from '../services/aiService';
import { AIDecision } from '../types';

interface AIAssistantProps {
    onNotification: (message: string) => void;
}

interface ChatMessage {
    id: number;
    message: string;
    sender: 'user' | 'ai';
    timestamp: Date;
}

const AIAssistant: React.FC<AIAssistantProps> = ({ onNotification }) => {
    const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
    const [inputMessage, setInputMessage] = useState('');
    const [recommendations, setRecommendations] = useState<any[]>([]);
    const [autoTradingEnabled, setAutoTradingEnabled] = useState(false);
    const [autoTradingStatus, setAutoTradingStatus] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [analysisSymbol, setAnalysisSymbol] = useState('AAPL');
    const [aiDecision, setAiDecision] = useState<AIDecision | null>(null);

    useEffect(() => {
        loadRecommendations();
        loadAutoTradingStatus();
        // Add welcome message
        setChatMessages([{
            id: 1,
            message: "Hello! I'm your AI trading assistant. I can help you with market analysis, trading strategies, and provide real-time insights. How can I assist you today?",
            sender: 'ai',
            timestamp: new Date()
        }]);
    }, []);

    const loadRecommendations = async () => {
        try {
            const response = await aiService.getRecommendations();
            setRecommendations(response.recommendations);
        } catch (error) {
            console.error('Error loading recommendations:', error);
        }
    };

    const loadAutoTradingStatus = async () => {
        try {
            const status = await aiService.getAutoTradingStatus();
            setAutoTradingStatus(status);
            setAutoTradingEnabled(status.enabled);
        } catch (error) {
            console.error('Error loading auto trading status:', error);
        }
    };

    const sendMessage = async () => {
        if (!inputMessage.trim()) return;

        const userMessage: ChatMessage = {
            id: chatMessages.length + 1,
            message: inputMessage,
            sender: 'user',
            timestamp: new Date()
        };

        setChatMessages(prev => [...prev, userMessage]);
        setInputMessage('');
        setLoading(true);

        try {
            const chatRequest: AIChatRequest = {
                message: inputMessage,
                context: {
                    recommendations,
                    autoTradingStatus
                }
            };

            const response = await aiService.chat(chatRequest);

            const aiMessage: ChatMessage = {
                id: chatMessages.length + 2,
                message: response.response,
                sender: 'ai',
                timestamp: new Date()
            };

            setChatMessages(prev => [...prev, aiMessage]);
        } catch (error) {
            console.error('Error sending message:', error);
            onNotification('Error communicating with AI assistant');
        } finally {
            setLoading(false);
        }
    };

    const getAIAnalysis = async () => {
        setLoading(true);
        try {
            const decision = await aiService.getTradingDecision(analysisSymbol);
            setAiDecision(decision);
            onNotification(`AI analysis completed for ${analysisSymbol}`);
        } catch (error) {
            console.error('Error getting AI analysis:', error);
            onNotification('Error getting AI analysis');
        } finally {
            setLoading(false);
        }
    };

    const toggleAutoTrading = async () => {
        try {
            const newEnabled = !autoTradingEnabled;
            await aiService.toggleAutoTrading(newEnabled);
            setAutoTradingEnabled(newEnabled);
            loadAutoTradingStatus();
            onNotification(`Auto trading ${newEnabled ? 'enabled' : 'disabled'}`);
        } catch (error) {
            console.error('Error toggling auto trading:', error);
            onNotification('Error updating auto trading settings');
        }
    };

    return (
        <Grid container spacing={3}>
            {/* AI Chat */}
            <Grid item xs={12} md={8}>
                <Paper sx={{ p: 3, height: 600, display: 'flex', flexDirection: 'column' }}>
                    <Typography variant="h6" gutterBottom>
                        AI Trading Assistant
                    </Typography>

                    <Box sx={{ flexGrow: 1, overflowY: 'auto', mb: 2, maxHeight: 450 }}>
                        {chatMessages.map((msg) => (
                            <Box
                                key={msg.id}
                                sx={{
                                    display: 'flex',
                                    mb: 2,
                                    justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start'
                                }}
                            >
                                <Box sx={{ display: 'flex', alignItems: 'flex-start', maxWidth: '80%' }}>
                                    {msg.sender === 'ai' && (
                                        <Avatar sx={{ mr: 1, bgcolor: 'primary.main' }}>
                                            <AIIcon />
                                        </Avatar>
                                    )}
                                    <Paper
                                        sx={{
                                            p: 2,
                                            bgcolor: msg.sender === 'user' ? 'primary.light' : 'grey.100',
                                            color: msg.sender === 'user' ? 'white' : 'text.primary'
                                        }}
                                    >
                                        <Typography variant="body2">{msg.message}</Typography>
                                        <Typography variant="caption" sx={{ opacity: 0.7, mt: 1, display: 'block' }}>
                                            {msg.timestamp.toLocaleTimeString()}
                                        </Typography>
                                    </Paper>
                                    {msg.sender === 'user' && (
                                        <Avatar sx={{ ml: 1, bgcolor: 'secondary.main' }}>
                                            <PersonIcon />
                                        </Avatar>
                                    )}
                                </Box>
                            </Box>
                        ))}
                    </Box>

                    <Box sx={{ display: 'flex', gap: 1 }}>
                        <TextField
                            fullWidth
                            variant="outlined"
                            placeholder="Ask me about trading, market analysis, or strategies..."
                            value={inputMessage}
                            onChange={(e) => setInputMessage(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                            disabled={loading}
                        />
                        <Button
                            variant="contained"
                            onClick={sendMessage}
                            disabled={loading || !inputMessage.trim()}
                        >
                            Send
                        </Button>
                    </Box>
                </Paper>
            </Grid>

            {/* AI Controls & Analysis */}
            <Grid item xs={12} md={4}>
                {/* Auto Trading Controls */}
                <Paper sx={{ p: 3, mb: 3 }}>
                    <Typography variant="h6" gutterBottom>
                        Auto Trading
                    </Typography>

                    <FormControlLabel
                        control={
                            <Switch
                                checked={autoTradingEnabled}
                                onChange={toggleAutoTrading}
                                color="primary"
                            />
                        }
                        label="Enable Auto Trading"
                    />

                    {autoTradingStatus && (
                        <Box sx={{ mt: 2 }}>
                            <Typography variant="body2" color="textSecondary">
                                Confidence Threshold: {(autoTradingStatus.confidence_threshold * 100).toFixed(0)}%
                            </Typography>
                            <Typography variant="body2" color="textSecondary">
                                Max Trades/Day: {autoTradingStatus.max_trades_per_day}
                            </Typography>
                            <Typography variant="body2" color="textSecondary">
                                Mode: {autoTradingStatus.trading_mode}
                            </Typography>
                        </Box>
                    )}

                    {autoTradingEnabled && (
                        <Alert severity="warning" sx={{ mt: 2 }}>
                            Auto trading is enabled. The AI will execute trades automatically based on its analysis.
                        </Alert>
                    )}
                </Paper>

                {/* AI Analysis */}
                <Paper sx={{ p: 3, mb: 3 }}>
                    <Typography variant="h6" gutterBottom>
                        AI Analysis
                    </Typography>

                    <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                        <TextField
                            label="Symbol"
                            value={analysisSymbol}
                            onChange={(e) => setAnalysisSymbol(e.target.value.toUpperCase())}
                            size="small"
                        />
                        <Button
                            variant="contained"
                            onClick={getAIAnalysis}
                            disabled={loading}
                        >
                            Analyze
                        </Button>
                    </Box>

                    {aiDecision && (
                        <Card sx={{ mt: 2 }}>
                            <CardContent>
                                <Typography variant="subtitle1" gutterBottom>
                                    {aiDecision.symbol} Analysis
                                </Typography>

                                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                                    {aiDecision.decision === 'buy' ? (
                                        <TrendingUpIcon color="success" />
                                    ) : aiDecision.decision === 'sell' ? (
                                        <TrendingDownIcon color="error" />
                                    ) : null}
                                    <Chip
                                        label={aiDecision.decision.toUpperCase()}
                                        color={
                                            aiDecision.decision === 'buy' ? 'success' :
                                                aiDecision.decision === 'sell' ? 'error' : 'default'
                                        }
                                        sx={{ ml: 1 }}
                                    />
                                    <Chip
                                        label={`${(aiDecision.confidence * 100).toFixed(0)}% confidence`}
                                        variant="outlined"
                                        sx={{ ml: 1 }}
                                    />
                                </Box>

                                <Typography variant="body2" color="textSecondary" gutterBottom>
                                    Reasoning:
                                </Typography>
                                <Typography variant="body2">
                                    {aiDecision.reasoning}
                                </Typography>

                                {aiDecision.suggested_quantity > 0 && (
                                    <Typography variant="body2" sx={{ mt: 1 }}>
                                        Suggested Quantity: {aiDecision.suggested_quantity}
                                    </Typography>
                                )}
                            </CardContent>
                        </Card>
                    )}
                </Paper>

                {/* AI Recommendations */}
                <Paper sx={{ p: 3 }}>
                    <Typography variant="h6" gutterBottom>
                        Daily Recommendations
                    </Typography>

                    {recommendations.length > 0 ? (
                        <List>
                            {recommendations.map((rec, index) => (
                                <React.Fragment key={index}>
                                    <ListItem sx={{ px: 0 }}>
                                        <ListItemText
                                            primary={
                                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                                    <Typography variant="subtitle2">{rec.symbol}</Typography>
                                                    <Chip
                                                        label={rec.action.toUpperCase()}
                                                        size="small"
                                                        color={
                                                            rec.action === 'buy' ? 'success' :
                                                                rec.action === 'sell' ? 'error' : 'default'
                                                        }
                                                    />
                                                    <Chip
                                                        label={`${(rec.confidence * 100).toFixed(0)}%`}
                                                        size="small"
                                                        variant="outlined"
                                                    />
                                                </Box>
                                            }
                                            secondary={rec.reasoning}
                                        />
                                    </ListItem>
                                    {index < recommendations.length - 1 && <Divider />}
                                </React.Fragment>
                            ))}
                        </List>
                    ) : (
                        <Typography variant="body2" color="textSecondary">
                            No recommendations available
                        </Typography>
                    )}

                    <Button
                        variant="outlined"
                        onClick={loadRecommendations}
                        sx={{ mt: 2 }}
                        fullWidth
                    >
                        Refresh Recommendations
                    </Button>
                </Paper>
            </Grid>
        </Grid>
    );
};

export default AIAssistant;