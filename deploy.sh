#!/bin/bash

# JCW Trade Hub - Server Deployment Script
# Run this script on your server after uploading files

echo "🚀 Setting up JCW Trade Hub on your server..."

# Set variables
DOMAIN="jcwtradehub.com"
WEB_ROOT="/home/$DOMAIN/public_html"
BACKEND_DIR="$WEB_ROOT/backend"

echo "📂 Setting up directories..."

# Navigate to web root
cd $WEB_ROOT

# Ensure we're in the right place
if [ ! -d "backend" ]; then
    echo "❌ Backend directory not found. Please ensure files are uploaded correctly."
    exit 1
fi

echo "🐍 Setting up Python environment..."

# Set up backend
cd $BACKEND_DIR

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy python-multipart aiofiles
pip install yfinance pandas numpy openai python-dotenv websockets
pip install requests python-jose[cryptography] passlib[bcrypt]

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating environment file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your OpenAI API key!"
fi

echo "🌐 Setting up frontend..."

# Move frontend build files to web root (if not already there)
if [ -d "../frontend/build" ]; then
    echo "📁 Moving frontend files to web root..."
    cp -r ../frontend/build/* ../
    echo "✅ Frontend files moved"
else
    echo "ℹ️  Frontend build files already in place"
fi

# Create .htaccess for proper routing
cat > ../.htaccess << 'EOF'
# JCW Trade Hub - Frontend Routing and API Proxy

RewriteEngine On
RewriteBase /

# CORS Headers for API requests
Header always set Access-Control-Allow-Origin "*"
Header always set Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS"
Header always set Access-Control-Allow-Headers "Content-Type, Authorization"

# Handle API requests - proxy to backend (if backend runs on port 8000)
RewriteCond %{REQUEST_URI} ^/api/(.*)
RewriteRule ^api/(.*)$ http://localhost:8000/api/$1 [P,L,E=no-gzip:1]

# Handle React Router - send all non-file requests to index.html
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_URI} !^/api/
RewriteRule . /index.html [L]

# Enable compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/plain
    AddOutputFilterByType DEFLATE text/html
    AddOutputFilterByType DEFLATE text/xml
    AddOutputFilterByType DEFLATE text/css
    AddOutputFilterByType DEFLATE application/xml
    AddOutputFilterByType DEFLATE application/xhtml+xml
    AddOutputFilterByType DEFLATE application/rss+xml
    AddOutputFilterByType DEFLATE application/javascript
    AddOutputFilterByType DEFLATE application/x-javascript
</IfModule>

# Cache static assets
<IfModule mod_expires.c>
    ExpiresActive on
    ExpiresByType text/css "access plus 1 year"
    ExpiresByType application/javascript "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/gif "access plus 1 year"
    ExpiresByType image/svg+xml "access plus 1 year"
</IfModule>
EOF

echo "🔧 Creating systemd service..."

# Create systemd service file
sudo tee /etc/systemd/system/jcwtradehub.service > /dev/null << EOF
[Unit]
Description=JCW Trade Hub FastAPI Backend
After=network.target

[Service]
Type=simple
User=$DOMAIN
WorkingDirectory=$BACKEND_DIR
Environment=PATH=$BACKEND_DIR/venv/bin
ExecStart=$BACKEND_DIR/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable jcwtradehub
sudo systemctl start jcwtradehub

echo "🔍 Checking service status..."
sudo systemctl status jcwtradehub --no-pager

echo "🧪 Testing backend..."
sleep 3
curl -f http://localhost:8000/api/v1/health && echo "✅ Backend is running!" || echo "❌ Backend not responding"

echo "🎉 Setup complete!"
echo ""
echo "🌐 Your JCW Trade Hub should now be accessible at:"
echo "   Frontend: https://$DOMAIN"
echo "   Backend:  https://$DOMAIN:8000"
echo ""
echo "🔐 Login with these credentials:"
echo "   Username: admin | Password: jcwtrade2024"
echo "   Username: jcw   | Password: tradehub123"
echo "   Username: trader| Password: secure2024"
echo ""
echo "📋 Useful commands:"
echo "   Check backend status: sudo systemctl status jcwtradehub"
echo "   View backend logs:    sudo journalctl -u jcwtradehub -f"
echo "   Restart backend:      sudo systemctl restart jcwtradehub"
echo "   Test backend:         curl http://localhost:8000/api/v1/health"
echo ""
echo "⚙️  Don't forget to:"
echo "   1. Edit $BACKEND_DIR/.env and add your OpenAI API key"
echo "   2. Open port 8000 in your firewall if needed"
echo "   3. Configure SSL/HTTPS if desired"