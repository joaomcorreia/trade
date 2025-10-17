# JCW Trade Hub - Server Setup Guide

## 🎯 Quick Setup for jcwtradehub.com

Since you've uploaded files to `public_html`, let's get everything working!

## 📂 Current File Structure
```
/home/jcwtradehub.com/public_html/
├── frontend/build/              # React frontend files
├── backend/                     # FastAPI backend
├── frontend/                    # Source code (optional)
└── other files...
```

## 🚀 Step 1: Set Up Backend Python Environment

### SSH into your server and run:

```bash
# Navigate to your domain directory
cd /home/jcwtradehub.com/public_html

# Create Python virtual environment for backend
cd backend
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# If requirements.txt is missing, install manually:
pip install fastapi uvicorn sqlalchemy python-multipart aiofiles
pip install yfinance pandas numpy ta-lib openai python-dotenv
pip install websockets
```

### Create/Update Environment File:
```bash
# In backend directory
cp .env.example .env
nano .env
```

Add your configuration:
```
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./trading.db
ENVIRONMENT=production
FRONTEND_URL=https://jcwtradehub.com
BACKEND_URL=https://jcwtradehub.com:8000
```

## 🌐 Step 2: Configure Frontend

### Move frontend build files to web root:
```bash
# Navigate to public_html
cd /home/jcwtradehub.com/public_html

# Move React build files to web root
cp -r frontend/build/* .

# Or if build files are already in root, ensure index.html is accessible
ls -la index.html
```

### Update API URLs in frontend:
The frontend needs to know where your backend API is running. Check if there's a config file:

```bash
# Look for environment or config files
find . -name "*.env*" -o -name "*config*"
```

## 🔧 Step 3: Start Backend Server

### Option A: Using systemd (Recommended for production)

Create a service file:
```bash
sudo nano /etc/systemd/system/jcwtradehub.service
```

Add this content:
```ini
[Unit]
Description=JCW Trade Hub FastAPI Backend
After=network.target

[Service]
Type=simple
User=jcwtradehub.com
WorkingDirectory=/home/jcwtradehub.com/public_html/backend
Environment=PATH=/home/jcwtradehub.com/public_html/backend/venv/bin
ExecStart=/home/jcwtradehub.com/public_html/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable jcwtradehub
sudo systemctl start jcwtradehub
sudo systemctl status jcwtradehub
```

### Option B: Manual Start (for testing)
```bash
cd /home/jcwtradehub.com/public_html/backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🔥 Step 4: Configure Web Server (Nginx/Apache)

### For OpenLiteSpeed/Apache (CyberPanel default):

Create `.htaccess` in public_html:
```apache
# Serve React frontend
RewriteEngine On
RewriteBase /

# Handle API requests - proxy to backend
RewriteCond %{REQUEST_URI} ^/api/(.*)
RewriteRule ^api/(.*)$ http://localhost:8000/api/$1 [P,L]

# Handle all other requests with React
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.html [L]
```

### Alternative: Direct port access
If your hosting allows, you can access:
- Frontend: https://jcwtradehub.com
- Backend API: https://jcwtradehub.com:8000

## 🧪 Step 5: Test Everything

### Check Backend:
```bash
# Test backend directly
curl http://localhost:8000/api/health

# Check if process is running
ps aux | grep uvicorn
```

### Check Frontend:
```bash
# Ensure index.html is in web root
ls -la /home/jcwtradehub.com/public_html/index.html

# Check web server access
curl -I https://jcwtradehub.com
```

## 🔐 Step 6: Login Credentials

Your trading dashboard now has a secure login page with these credentials:
- `admin` / `jcwtrade2024`
- `jcw` / `tradehub123` 
- `trader` / `secure2024`

## 🚨 Common Issues & Solutions

### Issue 1: Backend won't start
```bash
# Check logs
journalctl -u jcwtradehub -f

# Check if port is available
netstat -tlnp | grep :8000

# Check Python environment
cd backend && source venv/bin/activate && python -c "import fastapi; print('OK')"
```

### Issue 2: Frontend shows blank page
```bash
# Check if build files exist
ls -la /home/jcwtradehub.com/public_html/index.html
ls -la /home/jcwtradehub.com/public_html/static/

# Check web server logs
tail -f /usr/local/lsws/logs/error.log
```

### Issue 3: API connection fails
- Ensure backend is running on port 8000
- Check firewall allows port 8000
- Verify API URLs in frontend configuration

## 📞 Quick Commands Reference

```bash
# Start backend manually
cd /home/jcwtradehub.com/public_html/backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Check backend status
curl http://localhost:8000/api/health

# Restart web server
sudo systemctl restart lsws

# View logs
tail -f /usr/local/lsws/logs/access.log
tail -f /usr/local/lsws/logs/error.log
```

## 🎉 Success!
Once everything is running:
1. Visit https://jcwtradehub.com
2. You should see the JCW TRADE HUB login page
3. Use the credentials above to log in
4. Access your AI trading dashboard!

---
*Need help? The backend should be accessible at port 8000, and the frontend should serve from the web root.*