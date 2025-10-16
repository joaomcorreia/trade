import React, { useState, useEffect } from 'react';
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  AppBar,
  Toolbar,
  Typography,
  Container,
  Grid,
  Paper,
  Box,
  Tab,
  Tabs,
  Alert,
  Snackbar
} from '@mui/material';
import TradingDashboard from './components/TradingDashboard';
import Portfolio from './components/Portfolio';
import AIAssistant from './components/AIAssistant';
import NewsPanel from './components/NewsPanel';
import { tradingService } from './services/tradingService';
import { PortfolioSummary } from './types';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
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

function App() {
  const [currentTab, setCurrentTab] = useState(0);
  const [portfolioSummary, setPortfolioSummary] = useState<PortfolioSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [notification, setNotification] = useState<string | null>(null);

  useEffect(() => {
    loadPortfolioSummary();
  }, []);

  const loadPortfolioSummary = async () => {
    try {
      const summary = await tradingService.getPortfolioSummary();
      setPortfolioSummary(summary);
    } catch (err) {
      console.error('Error loading portfolio:', err);
      setError('Failed to load portfolio data');
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
    setError(null);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="static" elevation={1}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            AI Trading Dashboard
          </Typography>
          {portfolioSummary && (
            <Box sx={{ display: 'flex', gap: 3, alignItems: 'center' }}>
              <Typography variant="body2">
                Portfolio: ${portfolioSummary.total_value.toLocaleString()}
              </Typography>
              <Typography 
                variant="body2" 
                color={portfolioSummary.total_pnl >= 0 ? 'success.main' : 'error.main'}
              >
                P&L: {portfolioSummary.total_pnl >= 0 ? '+' : ''}${portfolioSummary.total_pnl.toLocaleString()} 
                ({portfolioSummary.total_return_percent >= 0 ? '+' : ''}{portfolioSummary.total_return_percent}%)
              </Typography>
            </Box>
          )}
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
        open={!!error}
        autoHideDuration={6000}
        onClose={closeError}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert severity="error" onClose={closeError}>
          {error}
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

export default App;