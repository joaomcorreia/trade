# 🚀 Quick Setup Guide

Get your AI Trading Platform running in under 5 minutes!

## Prerequisites

- Python 3.8 or higher
- Internet connection for market data
- 10MB free disk space

## 1-Click Setup (Windows)
```bash
ssh your-username@your-server-ip
```

### 2. Navigate to your domain directory
```bash
cd /home/jcwtradehub.com/public_html
```

### 3. Run the deployment script
```bash
# Make the script executable
chmod +x deploy.sh

# Run the deployment script
./deploy.sh
```

**OR do it manually:**

### 4. Set up Python backend (Manual method)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy yfinance openai python-dotenv websockets
```

### 5. Configure environment
```bash
# Copy and edit environment file
cp .env.example .env
nano .env
```

Add your OpenAI API key:
```
OPENAI_API_KEY=your_key_here
DATABASE_URL=sqlite:///./trading.db
ENVIRONMENT=production
```

### 6. Move frontend files to web root
```bash
# If build files are in frontend/build/
cp -r frontend/build/* .

# Verify index.html is in web root
ls -la index.html
```

### 7. Start the backend server
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
```

### 8. Test everything
```bash
# Test backend
curl http://localhost:8000/api/v1/health

# Check if frontend is accessible
curl -I https://jcwtradehub.com
```

## 🎯 Expected Results

✅ **Frontend**: https://jcwtradehub.com shows login page  
✅ **Backend**: Port 8000 serves API  
✅ **Login**: Use `admin`/`jcwtrade2024` to access dashboard  

## 🔧 Troubleshooting

**Backend won't start:**
- Check Python version: `python3 --version` (needs 3.7+)
- Check dependencies: `pip list`
- Check logs: `journalctl -u jcwtradehub -f`

**Frontend shows blank page:**
- Verify index.html in web root: `ls /home/jcwtradehub.com/public_html/index.html`
- Check web server logs

**API connection fails:**
- Ensure port 8000 is open
- Check if backend is running: `ps aux | grep uvicorn`
- Test direct API access: `curl http://localhost:8000/api/v1/health`

## 📞 Quick Commands

```bash
# Start backend manually
cd /home/jcwtradehub.com/public_html/backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Check what's running
ps aux | grep uvicorn
netstat -tlnp | grep :8000

# View logs
tail -f /var/log/messages
```

## 🎉 Success!
When working, you'll see:
1. Professional JCW TRADE HUB login page
2. Secure authentication system
3. Full AI trading dashboard
4. Real-time market data and trading