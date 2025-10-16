# GitHub Deployment Commands

## Initialize Git Repository and Push to GitHub

# 1. Initialize git (if not already done)
git init

# 2. Add remote repository
git remote add origin https://github.com/joaomcorreia/trade.git

# 3. Add all files
git add .

# 4. Create initial commit
git commit -m "Initial commit: AI Trading Dashboard for jcwtradehub.com

- FastAPI backend with AI trading engine
- React TypeScript frontend
- OpenAI integration for trading decisions
- Real-time market data with Yahoo Finance
- Technical analysis (RSI, MACD, Volume)
- Portfolio management
- News sentiment analysis
- WebSocket real-time updates
- CyberPanel deployment ready"

# 5. Push to GitHub
git branch -M main
git push -u origin main

## Production Deployment Commands

# Create production branch
git checkout -b production

# Build frontend for production
cd frontend
npm run build
cd ..

# Commit production build
git add .
git commit -m "Production build for jcwtradehub.com deployment"
git push origin production

## Quick Commands

# Check status
git status

# Add changes
git add .

# Commit changes
git commit -m "Update: description of changes"

# Push changes
git push

# Create new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main
git checkout production