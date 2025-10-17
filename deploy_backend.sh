#!/bin/bash

# AI Trading Dashboard - Backend Configuration Script
# This script sets up the backend with all AI and news features

echo "🤖 Setting up AI Trading Dashboard Backend..."

# Create environment configuration
cat > /home/jcwtradehub.com/backend/.env << 'EOF'
# Database Configuration
DATABASE_URL=sqlite:///./trading_dashboard.db

# AI Configuration
OPENAI_API_KEY=your_openai_api_key_here
AI_TRADING_ENABLED=false
AI_CONFIDENCE_THRESHOLD=0.7

# News API Configuration  
NEWS_API_KEY=your_news_api_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here

# Technical Indicator Settings
RSI_PERIOD=14
MACD_FAST=12
MACD_SLOW=26
DEFAULT_POSITION_SIZE=1000

# CORS Settings
CORS_ORIGINS=["https://jcwtradehub.com", "http://localhost:3000"]

# Security
SECRET_KEY=your_secret_key_here
EOF

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd /home/jcwtradehub.com/backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install sqlalchemy==2.0.23
pip install pydantic==2.5.0
pip install python-multipart==0.0.6
pip install python-jose[cryptography]==3.3.0
pip install passlib[bcrypt]==1.7.4
pip install yfinance==0.2.28
pip install pandas==2.1.4
pip install numpy==1.25.2
pip install requests==2.31.0
pip install openai==1.3.7
pip install websockets==12.0

# Create systemd service
echo "🔧 Creating systemd service..."
sudo tee /etc/systemd/system/jcwtradehub-backend.service << 'EOF'
[Unit]
Description=JCW Trade Hub Backend API
After=network.target

[Service]
Type=exec
User=jcwtr8034
Group=jcwtr8034
WorkingDirectory=/home/jcwtradehub.com/backend
Environment=PATH=/home/jcwtradehub.com/backend/venv/bin
ExecStart=/home/jcwtradehub.com/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Set permissions
echo "🔐 Setting permissions..."
sudo chown -R jcwtr8034:jcwtr8034 /home/jcwtradehub.com/backend
sudo chmod +x /home/jcwtradehub.com/backend/*.py

# Create database
echo "🗄️ Initializing database..."
cd /home/jcwtradehub.com/backend
source venv/bin/activate
python -c "
from app.core.database import engine, Base
from app.models import portfolio, trade
Base.metadata.create_all(bind=engine)
print('Database initialized successfully!')
"

# Enable and start service
echo "🚀 Starting backend service..."
sudo systemctl daemon-reload
sudo systemctl enable jcwtradehub-backend
sudo systemctl start jcwtradehub-backend

# Check status
echo "📊 Backend service status:"
sudo systemctl status jcwtradehub-backend --no-pager -l

echo ""
echo "✅ Backend setup complete!"
echo ""
echo "🔧 Next steps:"
echo "1. Edit /home/jcwtradehub.com/backend/.env with your API keys:"
echo "   - OPENAI_API_KEY (for AI features)"
echo "   - NEWS_API_KEY (for news features)"
echo "   - SECRET_KEY (generate a secure key)"
echo ""
echo "2. Restart the service after updating API keys:"
echo "   sudo systemctl restart jcwtradehub-backend"
echo ""
echo "3. Test the API:"
echo "   curl http://localhost:8000/docs"
echo ""
echo "🎉 Your AI Trading Dashboard is ready!"