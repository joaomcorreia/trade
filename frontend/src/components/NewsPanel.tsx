import React, { useState, useEffect } from 'react';
import {
    Grid,
    Paper,
    Typography,
    Box,
    Card,
    CardContent,
    List,
    ListItem,
    ListItemText,
    Chip,
    Link,
    Tabs,
    Tab,
    FormControl,
    InputLabel,
    Select,
    MenuItem
} from '@mui/material';
import { marketService } from '../services/marketService';
import { NewsArticle } from '../types';

interface TabPanelProps {
    children?: React.ReactNode;
    index: number;
    value: number;
}

function TabPanel(props: TabPanelProps) {
    const { children, value, index, ...other } = props;
    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`news-tabpanel-${index}`}
            aria-labelledby={`news-tab-${index}`}
            {...other}
        >
            {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
        </div>
    );
}

const NewsPanel: React.FC = () => {
    const [selectedSymbol, setSelectedSymbol] = useState('AAPL');
    const [news, setNews] = useState<NewsArticle[]>([]);
    const [loading, setLoading] = useState(false);
    const [currentTab, setCurrentTab] = useState(0);
    const [marketSentiment, setMarketSentiment] = useState<any>(null);

    const watchlistSymbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'NVDA', 'META'];

    useEffect(() => {
        loadNews(selectedSymbol);
    }, [selectedSymbol]);

    const loadNews = async (symbol: string) => {
        setLoading(true);
        try {
            const response = await marketService.getNews(symbol);
            setNews(response.articles);

            // Calculate overall sentiment
            const sentiments = response.articles.map(article => article.sentiment.polarity);
            const avgSentiment = sentiments.reduce((sum, s) => sum + s, 0) / sentiments.length;

            setMarketSentiment({
                symbol,
                avgSentiment,
                totalArticles: response.articles.length,
                positiveCount: sentiments.filter(s => s > 0.1).length,
                negativeCount: sentiments.filter(s => s < -0.1).length,
                neutralCount: sentiments.filter(s => s >= -0.1 && s <= 0.1).length
            });
        } catch (error) {
            console.error('Error loading news:', error);
        } finally {
            setLoading(false);
        }
    };

    const getSentimentColor = (sentiment: string) => {
        switch (sentiment) {
            case 'positive': return 'success';
            case 'negative': return 'error';
            default: return 'default';
        }
    };

    const getSentimentIcon = (polarity: number) => {
        if (polarity > 0.1) return '📈';
        if (polarity < -0.1) return '📉';
        return '➡️';
    };

    const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
        setCurrentTab(newValue);
    };

    return (
        <Grid container spacing={3}>
            {/* Controls */}
            <Grid item xs={12}>
                <Paper sx={{ p: 2 }}>
                    <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
                        <FormControl sx={{ minWidth: 120 }}>
                            <InputLabel>Symbol</InputLabel>
                            <Select
                                value={selectedSymbol}
                                label="Symbol"
                                onChange={(e) => setSelectedSymbol(e.target.value)}
                            >
                                {watchlistSymbols.map((symbol) => (
                                    <MenuItem key={symbol} value={symbol}>
                                        {symbol}
                                    </MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                    </Box>
                </Paper>
            </Grid>

            {/* Market Sentiment Summary */}
            {marketSentiment && (
                <Grid item xs={12}>
                    <Paper sx={{ p: 3 }}>
                        <Typography variant="h6" gutterBottom>
                            Market Sentiment for {marketSentiment.symbol}
                        </Typography>

                        <Grid container spacing={3}>
                            <Grid item xs={12} sm={6} md={3}>
                                <Card>
                                    <CardContent sx={{ textAlign: 'center' }}>
                                        <Typography variant="h4">
                                            {getSentimentIcon(marketSentiment.avgSentiment)}
                                        </Typography>
                                        <Typography variant="h6">
                                            {marketSentiment.avgSentiment > 0.1 ? 'Positive' :
                                                marketSentiment.avgSentiment < -0.1 ? 'Negative' : 'Neutral'}
                                        </Typography>
                                        <Typography variant="body2" color="textSecondary">
                                            Overall Sentiment
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Grid>

                            <Grid item xs={12} sm={6} md={3}>
                                <Card>
                                    <CardContent sx={{ textAlign: 'center' }}>
                                        <Typography variant="h4" color="success.main">
                                            {marketSentiment.positiveCount}
                                        </Typography>
                                        <Typography variant="h6">Positive</Typography>
                                        <Typography variant="body2" color="textSecondary">
                                            Articles
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Grid>

                            <Grid item xs={12} sm={6} md={3}>
                                <Card>
                                    <CardContent sx={{ textAlign: 'center' }}>
                                        <Typography variant="h4" color="error.main">
                                            {marketSentiment.negativeCount}
                                        </Typography>
                                        <Typography variant="h6">Negative</Typography>
                                        <Typography variant="body2" color="textSecondary">
                                            Articles
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Grid>

                            <Grid item xs={12} sm={6} md={3}>
                                <Card>
                                    <CardContent sx={{ textAlign: 'center' }}>
                                        <Typography variant="h4">
                                            {marketSentiment.neutralCount}
                                        </Typography>
                                        <Typography variant="h6">Neutral</Typography>
                                        <Typography variant="body2" color="textSecondary">
                                            Articles
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Grid>
                        </Grid>
                    </Paper>
                </Grid>
            )}

            {/* News Tabs */}
            <Grid item xs={12}>
                <Paper>
                    <Tabs value={currentTab} onChange={handleTabChange} variant="fullWidth">
                        <Tab label="All News" />
                        <Tab label="Positive News" />
                        <Tab label="Negative News" />
                    </Tabs>

                    <TabPanel value={currentTab} index={0}>
                        <Typography variant="h6" gutterBottom>
                            Latest News for {selectedSymbol}
                        </Typography>
                        <NewsList articles={news} />
                    </TabPanel>

                    <TabPanel value={currentTab} index={1}>
                        <Typography variant="h6" gutterBottom>
                            Positive News for {selectedSymbol}
                        </Typography>
                        <NewsList articles={news.filter(article => article.sentiment.sentiment === 'positive')} />
                    </TabPanel>

                    <TabPanel value={currentTab} index={2}>
                        <Typography variant="h6" gutterBottom>
                            Negative News for {selectedSymbol}
                        </Typography>
                        <NewsList articles={news.filter(article => article.sentiment.sentiment === 'negative')} />
                    </TabPanel>
                </Paper>
            </Grid>
        </Grid>
    );
};

// News List Component
interface NewsListProps {
    articles: NewsArticle[];
}

const NewsList: React.FC<NewsListProps> = ({ articles }) => {
    if (articles.length === 0) {
        return (
            <Typography variant="body2" color="textSecondary" sx={{ p: 2 }}>
                No news articles found
            </Typography>
        );
    }

    return (
        <List>
            {articles.map((article, index) => (
                <ListItem key={index} sx={{ flexDirection: 'column', alignItems: 'flex-start', py: 2 }}>
                    <Box sx={{ width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
                        <Box sx={{ flexGrow: 1, mr: 2 }}>
                            <Link
                                href={article.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                sx={{ textDecoration: 'none' }}
                            >
                                <Typography variant="h6" component="h3" gutterBottom>
                                    {article.title}
                                </Typography>
                            </Link>

                            {article.description && (
                                <Typography variant="body2" color="textSecondary" paragraph>
                                    {article.description}
                                </Typography>
                            )}

                            <Box sx={{ display: 'flex', gap: 1, alignItems: 'center', flexWrap: 'wrap' }}>
                                <Typography variant="caption" color="textSecondary">
                                    {article.source} • {new Date(article.published_at).toLocaleDateString()}
                                </Typography>
                                <Chip
                                    label={article.sentiment.sentiment}
                                    color={getSentimentColor(article.sentiment.sentiment) as any}
                                    size="small"
                                />
                                <Typography variant="caption" color="textSecondary">
                                    Score: {article.sentiment.polarity.toFixed(2)}
                                </Typography>
                            </Box>
                        </Box>

                        <Typography variant="h3" sx={{ minWidth: 40, textAlign: 'center' }}>
                            {getSentimentIcon(article.sentiment.polarity)}
                        </Typography>
                    </Box>
                </ListItem>
            ))}
        </List>
    );

    function getSentimentColor(sentiment: string) {
        switch (sentiment) {
            case 'positive': return 'success';
            case 'negative': return 'error';
            default: return 'default';
        }
    }

    function getSentimentIcon(polarity: number) {
        if (polarity > 0.1) return '📈';
        if (polarity < -0.1) return '📉';
        return '➡️';
    }
};

export default NewsPanel;