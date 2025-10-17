# JCW Trade Hub - CyberPanel Deployment Guide

## 🎯 Deploying AI Trading Dashboard to jcwtradehub.com

### 🤖 Enhanced Features Now Available
- **AI Trading Assistant**: OpenAI-powered chat and market analysis
- **Real-time News Feed**: Market news with sentiment analysis  
- **Technical Indicators**: RSI, MACD, volume analysis
- **Auto-Trading**: AI-driven autonomous trading capability
- **Professional UI**: JCW TRADE HUB branded login system

### ✅ Prerequisites
- CyberPanel hosting (€5/month VPS)
- Domain: jcwtradehub.com (already owned)
- SSH access to server
- **API Keys for Full Functionality**:
  - OpenAI API key (for AI assistant features)
  - NewsAPI key (for real-time news)

### 📁 File Structure for CyberPanel
```
/home/jcwtradehub.com/
├── public_html/                 # React frontend (static files)
│   ├── index.html
│   ├── static/
│   └── assets/
├── backend/                     # FastAPI application
│   ├── app/
│   ├── requirements.txt
│   ├── main.py
│   └── .env
└── logs/
```

### 🚀 Step 1: Prepare Production Build

**Frontend Build:**
```bash
cd C:\projects\trade\frontend
npm run build
# Creates optimized static files in 'build' folder
```

**Backend Preparation:**
```bash
cd C:\projects\trade\backend
# Update requirements.txt for production
pip freeze > requirements.txt
```

### 🖥️ Step 2: CyberPanel Configuration

**Create Website:**
1. Login to CyberPanel
2. Websites → Create Website
3. Domain: jcwtradehub.com
4. Select PHP version: Python 3.x

**Upload Files:**
1. Frontend: Upload `build` folder contents to `public_html/`
2. Backend: Upload `backend` folder to `/home/jcwtradehub.com/backend/`

### 🐍 Step 3: Python App Configuration

**Create Python App in CyberPanel:**
1. Go to Python → Create App
2. Domain: jcwtradehub.com
3. App Name: ai-trading-backend
4. App Path: `/home/jcwtradehub.com/backend`
5. Startup File: `main.py`

**Install Dependencies:**
```bash
cd /home/jcwtradehub.com/backend
pip install -r requirements.txt
```

### 🌐 Step 4: Nginx Configuration

**API Proxy Configuration:**
```nginx
# Add to jcwtradehub.com nginx config
location /api/ {
    proxy_pass http://127.0.0.1:8001;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# WebSocket support for real-time data
location /ws/ {
    proxy_pass http://127.0.0.1:8001;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
}
```

### 🔒 Step 5: SSL Certificate (FREE)

**Auto SSL with CyberPanel:**
1. SSL → Issue SSL
2. Domain: jcwtradehub.com
3. Select: Let's Encrypt (FREE)
4. Auto-renewal: Enabled

### 🗄️ Step 6: Database Setup

**Option A: SQLite (Simple)**
- Already configured
- File-based database
- Perfect for starting

**Option B: PostgreSQL (Scalable)**
```bash
# Install PostgreSQL in CyberPanel
sudo apt install postgresql postgresql-contrib
sudo -u postgres createdb jcwtradehub
```

### ⚙️ Step 7: Environment Variables

**Create Production .env:**
```env
# /home/jcwtradehub.com/backend/.env
DATABASE_URL=sqlite:///./jcwtradehub.db
OPENAI_API_KEY=your_key_here
ALPHA_VANTAGE_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
CORS_ORIGINS=https://jcwtradehub.com,https://www.jcwtradehub.com
ENVIRONMENT=production
```

### 🚀 Step 8: Start Services

**Start Backend:**
```bash
cd /home/jcwtradehub.com/backend
python main.py
```

### 🤖 Step 8: AI & News Configuration

**Deploy Backend Automatically:**
```bash
# Upload and run the backend deployment script
chmod +x /home/jcwtradehub.com/deploy_backend.sh
sudo /home/jcwtradehub.com/deploy_backend.sh
```

**Configure API Keys:**
```bash
# Edit environment file
nano /home/jcwtradehub.com/backend/.env

# Add your API keys:
OPENAI_API_KEY=sk-your-openai-key-here
NEWS_API_KEY=your-newsapi-key-here
SECRET_KEY=your-secret-key-here
```

**Restart Backend Service:**
```bash
sudo systemctl restart jcwtradehub-backend
sudo systemctl status jcwtradehub-backend
```

### 📊 Step 9: Testing

**Test Frontend:** https://jcwtradehub.com
**Test Backend API:** http://your-server-ip:8000/docs
**Test AI Assistant:** Use chat in dashboard
**Test News Feed:** Check News & Analysis tab

### 🔑 API Keys Setup Guide

**OpenAI API Key** (for AI assistant):
1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Add to `.env` file: `OPENAI_API_KEY=sk-...`

**NewsAPI Key** (for news feed):
1. Go to https://newsapi.org/register
2. Get free API key
3. Add to `.env` file: `NEWS_API_KEY=...`

**Without API Keys:**
- Dashboard works with demo data
- AI uses rule-based responses
- News shows mock articles

### 🎯 Final Result

**Your Professional AI Trading Platform:**
- ✅ **URL**: https://jcwtradehub.com
- ✅ **Login System**: JCW TRADE HUB branded
- ✅ **AI Assistant**: Chat-based trading help
- ✅ **News Feed**: Real-time market news
- ✅ **Technical Analysis**: RSI, MACD indicators
- ✅ **SSL**: Secure HTTPS
- ✅ **Performance**: Fast loading
- ✅ **Mobile**: Responsive design
- ✅ **AI**: OpenAI integration
- ✅ **Real-time**: Live market data
- ✅ **Professional**: Production-ready

### 💰 Total Monthly Cost: €5

## 🎉 Ready to Deploy?

Your AI trading dashboard is CyberPanel-ready and can be deployed to jcwtradehub.com for just €5/month!