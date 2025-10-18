# 🚀 AI Trading Platform

A comprehensive AI-powered trading platform with real-time market data, intelligent signal generation, and a modern web dashboard.

## ✨ Features

### 🔥 Core Features
- **Real-time Market Data** - Live prices from Yahoo Finance API (no API keys required)
- **AI Trading Signals** - Intelligent buy/sell recommendations with confidence scores
- **Multi-Market Support** - Stocks, Crypto, Forex, Commodities, and Indices
- **WebSocket Streaming** - Live price updates and portfolio tracking
- **Database Persistence** - SQLite database for trading history and AI signals
- **Modern Web Dashboard** - Responsive HTML/CSS/JS interface

### 📊 Market Coverage
- **Stocks**: AAPL, MSFT, GOOGL, TSLA, AMZN, NVDA, META, NFLX, JPM, V
- **Cryptocurrency**: BTC-USD, ETH-USD, ADA-USD, DOT-USD, SOL-USD, LINK-USD
- **Forex**: EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CAD, USD/CHF
- **Commodities**: Gold, Silver, Crude Oil, Natural Gas, Copper
- **Indices**: S&P 500, Dow Jones, NASDAQ, Russell 2000, VIX

### 🤖 AI Features
- **Technical Analysis** - RSI, MACD, SMA indicators
- **Sentiment Analysis** - Market news integration with real-time context
- **Risk Assessment** - Portfolio risk evaluation
- **Pattern Recognition** - Price pattern analysis

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Internet connection for market data

### Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ai-trading-platform.git
   cd ai-trading-platform
   ```

2. **Install dependencies**
   ```bash
   pip install fastapi uvicorn yfinance sqlalchemy databases aiosqlite websockets requests
   ```

3. **Start the platform**
   
   **Option A: Use the launcher (Windows)**
   ```bash
   quick_start.bat
   ```
   
   **Option B: Manual startup**
   ```bash
   # Terminal 1: Start backend
   python complete_ai_backend.py
   
   # Terminal 2: Start frontend
   python -m http.server 3000
   ```

4. **Access the platform**
   - 📊 **Trading Dashboard**: http://localhost:3000/ai_trading_dashboard.html
   - 📚 **API Documentation**: http://localhost:8002/docs
   - ⚡ **WebSocket**: ws://localhost:8002/ws
   
   **Windows:**
   ```cmd
   setup.bat
   ```
   
   **Linux/Mac:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Configure API Keys**
   ```bash
   cd backend
   # Edit .env file with your API keys
   ```

4. **Start the application**
   
   **Backend:**
   ```bash
   cd backend
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   uvicorn app.main:app --reload
   ```
   
   **Frontend:**
   ```bash
   cd frontend
   npm start
   ```

5. **Access the dashboard**
   Open http://localhost:3000

## 🔑 API Keys Configuration

Add these keys to `backend/.env`:

```env
# Required for market data
ALPHA_VANTAGE_API_KEY=your_key_here

# Required for news analysis
NEWS_API_KEY=your_key_here

# Optional for AI assistant
OPENAI_API_KEY=your_key_here
```

### Get API Keys:
- **Alpha Vantage**: https://www.alphavantage.co/support/#api-key
- **News API**: https://newsapi.org/register
- **OpenAI**: https://platform.openai.com/api-keys

## 📊 Dashboard Overview

### 1. Trading Dashboard
- Live price charts with technical indicators
- Watchlist with real-time updates
- Quick trade execution interface
- Technical analysis signals

### 2. Portfolio Management
- Current positions and P&L
- Trade history and performance metrics
- Risk analysis and position sizing
- Automated portfolio rebalancing

### 3. AI Assistant
- Intelligent market analysis
- Trading recommendations
- Chat interface for queries
- Automatic trading capabilities (when enabled)

### 4. News & Analysis
- Real-time market news
- Sentiment analysis
- Market impact assessment
- Correlation analysis

## ⚙️ Configuration

### Trading Parameters
Edit `config.yaml` to customize:
- Technical indicator settings
- Risk management rules
- AI confidence thresholds
- Trading hours and limits

### Environment Variables
Key settings in `.env`:
- API keys for data sources
- Database configuration
- Trading mode (paper/live)
- AI features toggle

## 🤖 AI Features

### Analysis Engine
- Multi-factor analysis combining technical indicators
- News sentiment integration
- Market volatility assessment
- Risk-adjusted confidence scoring

### Trading Decisions
- Autonomous buy/sell/hold recommendations
- Position sizing suggestions
- Risk level assessment
- Execution timing optimization

### Chat Assistant
- Interactive trading guidance
- Strategy discussions
- Market insights and explanations
- Educational content

## 📈 Technical Indicators

### Supported Indicators
- **RSI** - Relative Strength Index
- **MACD** - Moving Average Convergence Divergence
- **Moving Averages** - SMA, EMA
- **Bollinger Bands** - Volatility indicators
- **Volume Analysis** - Trading volume patterns

### Customization
All indicators are configurable through:
- Period lengths
- Thresholds (overbought/oversold)
- Signal sensitivity
- Timeframe analysis

## 🔒 Risk Management

### Built-in Protections
- Position size limits
- Stop-loss automation
- Maximum daily trades
- Volatility-based adjustments

### Portfolio Controls
- Diversification requirements
- Correlation limits
- Maximum drawdown protection
- Dynamic position sizing

## 🚨 Important Disclaimers

- **Educational Purpose**: This software is for educational and research purposes
- **Trading Risks**: All trading involves significant financial risk
- **No Guarantees**: Past performance doesn't guarantee future results
- **Paper Trading**: Start with paper trading to test strategies
- **Professional Advice**: Consult financial advisors for investment decisions

## 🛠️ Development

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

### Adding Features
- Backend: Add endpoints in `app/api/endpoints/`
- Frontend: Add components in `src/components/`
- AI: Extend analysis in `app/ai/trading_ai.py`

## 📝 License

This project is for educational purposes. Please review and comply with all applicable financial regulations in your jurisdiction.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the configuration guide
3. Submit an issue on GitHub

---

**Remember**: Always trade responsibly and never risk more than you can afford to lose.