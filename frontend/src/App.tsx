import React, { useState, useEffect } from 'react';
import {
    ThemeProvider,
    createTheme,
    CssBaseline,
    AppBar,
    Toolbar,
    Typography,
    Container,
    Paper,
    Box,
    Tab,
    Tabs,
    Alert,
    Snackbar,
    IconButton,
    Menu,
    MenuItem
} from '@mui/material';
import { AccountCircle, ExitToApp } from '@mui/icons-material';
import TradingDashboard from './components/TradingDashboard';
import Portfolio from './components/Portfolio';
import AIAssistant from './components/AIAssistant';
import NewsPanel from './components/NewsPanel';
import Login from './components/Login';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { tradingService } from './services/tradingService';
import { PortfolioSummary } from './types';

const theme = createTheme({
    palette: {
        mode: 'light',
        primary: {
            main: '#00e676',
        },
        secondary: {
            main: '#ff6b6b',
        },
        background: {
            default: '#f8fafc',
        },
    },
    typography: {
        h4: {
            fontWeight: 600,
        },
        h6: {
            fontWeight: 500,
        },
    },
    components: {
        MuiAppBar: {
            styleOverrides: {
                root: {
                    background: 'linear-gradient(135deg, #1e293b 0%, #334155 100%)',
                    boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
                },
            },
        },
    },
});

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
            id={`tabpanel-${index}`}
            aria-labelledby={`tab-${index}`}
            {...other}
        >
            {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
        </div>
    );
}

function TradingApp() {
    const { isAuthenticated, login, logout, loading, error } = useAuth();
    const [currentTab, setCurrentTab] = useState(0);
    const [portfolioSummary, setPortfolioSummary] = useState<PortfolioSummary | null>(null);
    const [appError, setAppError] = useState<string | null>(null);
    const [notification, setNotification] = useState<string | null>(null);
    const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

    useEffect(() => {
        if (isAuthenticated) {
            loadPortfolioSummary();
        }
    }, [isAuthenticated]);

    const loadPortfolioSummary = async () => {
        try {
            const summary = await tradingService.getPortfolioSummary();
            setPortfolioSummary(summary);
        } catch (err) {
            console.error('Error loading portfolio:', err);
            setAppError('Failed to load portfolio data');
        }
    };

    const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
        setCurrentTab(newValue);
    };

    const showNotification = (message: string) => {
        setNotification(message);
    };

    const closeNotification = () => {
        setNotification(null);
    };

    const closeError = () => {
        setAppError(null);
    };

    const handleLogin = async (username: string, password: string) => {
        await login(username, password);
    };

    const handleMenuClick = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorEl(event.currentTarget);
    };

    const handleMenuClose = () => {
        setAnchorEl(null);
    };

    const handleLogout = () => {
        logout();
        setAnchorEl(null);
        setCurrentTab(0);
        setPortfolioSummary(null);
    };

    if (!isAuthenticated) {
        return <Login onLogin={handleLogin} error={error} loading={loading} />;
    }

    const username = localStorage.getItem('jcw_username') || 'User';

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <AppBar position="static" elevation={1}>
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 700 }}>
                        JCW TRADE HUB
                    </Typography>
                    {portfolioSummary && (
                        <Box sx={{ display: 'flex', gap: 3, alignItems: 'center', mr: 2 }}>
                            <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.9)' }}>
                                Portfolio: ${portfolioSummary.total_value.toLocaleString()}
                            </Typography>
                            <Typography
                                variant="body2"
                                sx={{
                                    color: portfolioSummary.total_pnl >= 0 ? '#00e676' : '#ff6b6b',
                                    fontWeight: 600,
                                }}
                            >
                                P&L: {portfolioSummary.total_pnl >= 0 ? '+' : ''}${portfolioSummary.total_pnl.toLocaleString()}
                                ({portfolioSummary.total_return_percent >= 0 ? '+' : ''}{portfolioSummary.total_return_percent}%)
                            </Typography>
                        </Box>
                    )}
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.8)' }}>
                            Welcome, {username}
                        </Typography>
                        <IconButton
                            onClick={handleMenuClick}
                            sx={{ color: 'white' }}
                        >
                            <AccountCircle />
                        </IconButton>
                        <Menu
                            anchorEl={anchorEl}
                            open={Boolean(anchorEl)}
                            onClose={handleMenuClose}
                            anchorOrigin={{
                                vertical: 'bottom',
                                horizontal: 'right',
                            }}
                            transformOrigin={{
                                vertical: 'top',
                                horizontal: 'right',
                            }}
                        >
                            <MenuItem onClick={handleLogout}>
                                <ExitToApp sx={{ mr: 1 }} />
                                Logout
                            </MenuItem>
                        </Menu>
                    </Box>
                </Toolbar>
            </AppBar>

            <Container maxWidth="xl" sx={{ mt: 2, mb: 4 }}>
                <Paper>
                    <Tabs value={currentTab} onChange={handleTabChange} variant="fullWidth">
                        <Tab label="Dashboard" />
                        <Tab label="Portfolio" />
                        <Tab label="AI Assistant" />
                        <Tab label="News & Analysis" />
                    </Tabs>
                </Paper>

                <TabPanel value={currentTab} index={0}>
                    <TradingDashboard
                        onTradeExecuted={loadPortfolioSummary}
                        onNotification={showNotification}
                    />
                </TabPanel>

                <TabPanel value={currentTab} index={1}>
                    <Portfolio
                        portfolioSummary={portfolioSummary}
                        onPortfolioChange={loadPortfolioSummary}
                        onNotification={showNotification}
                    />
                </TabPanel>

                <TabPanel value={currentTab} index={2}>
                    <AIAssistant onNotification={showNotification} />
                </TabPanel>

                <TabPanel value={currentTab} index={3}>
                    <NewsPanel />
                </TabPanel>
            </Container>

            <Snackbar
                open={!!appError}
                autoHideDuration={6000}
                onClose={closeError}
                anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
            >
                <Alert severity="error" onClose={closeError}>
                    {appError}
                </Alert>
            </Snackbar>

            <Snackbar
                open={!!notification}
                autoHideDuration={4000}
                onClose={closeNotification}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
            >
                <Alert severity="success" onClose={closeNotification}>
                    {notification}
                </Alert>
            </Snackbar>
        </ThemeProvider>
    );
}

function App() {
    return (
        <AuthProvider>
            <TradingApp />
        </AuthProvider>
    );
}

export default App;