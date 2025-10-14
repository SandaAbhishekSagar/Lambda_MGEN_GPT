#!/bin/bash
# Setup SSL/HTTPS for Lambda Labs with Let's Encrypt

echo "🔒 Setting up SSL/HTTPS for Lambda Labs"
echo "========================================"
echo ""

# Check if domain is provided
if [ -z "$1" ]; then
    echo "❌ Error: Domain name required"
    echo ""
    echo "Usage: ./setup_ssl_lambda.sh your-domain.com"
    echo ""
    echo "You need to:"
    echo "1. Register a domain (e.g., from Namecheap, GoDaddy, etc.)"
    echo "2. Point the domain's A record to your Lambda IP: $(curl -s ifconfig.me)"
    echo "3. Run this script: ./setup_ssl_lambda.sh your-domain.com"
    echo ""
    exit 1
fi

DOMAIN=$1
LAMBDA_IP=$(curl -s ifconfig.me)

echo "📋 Configuration:"
echo "   Domain: $DOMAIN"
echo "   Lambda IP: $LAMBDA_IP"
echo ""

# Check if domain resolves to this IP
echo "🔍 Checking DNS configuration..."
RESOLVED_IP=$(dig +short $DOMAIN | tail -n1)

if [ "$RESOLVED_IP" != "$LAMBDA_IP" ]; then
    echo "⚠️  Warning: Domain does not resolve to this IP yet"
    echo "   Domain resolves to: $RESOLVED_IP"
    echo "   Expected IP: $LAMBDA_IP"
    echo ""
    echo "Please update your domain's DNS A record to point to: $LAMBDA_IP"
    echo "DNS propagation can take up to 48 hours (usually 5-30 minutes)"
    echo ""
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install Nginx
echo "📦 Installing Nginx..."
sudo apt update
sudo apt install -y nginx

# Configure Nginx as reverse proxy
echo "⚙️  Configuring Nginx..."
sudo tee /etc/nginx/sites-available/chatbot > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN;
    
    # Redirect HTTP to HTTPS (will be enabled after SSL setup)
    # return 301 https://\$server_name\$request_uri;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # CORS headers (in case needed)
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Content-Type, Authorization' always;
    }
}
EOF

# Enable site
sudo ln -sf /etc/nginx/sites-available/chatbot /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx config
echo "🧪 Testing Nginx configuration..."
sudo nginx -t

if [ $? -ne 0 ]; then
    echo "❌ Nginx configuration test failed"
    exit 1
fi

# Restart Nginx
echo "🔄 Restarting Nginx..."
sudo systemctl restart nginx
sudo systemctl enable nginx

# Install Certbot
echo "📦 Installing Certbot..."
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate
echo "🔒 Obtaining SSL certificate..."
echo ""
echo "⚠️  Important: You'll be asked for an email address"
echo "   This is required for SSL certificate renewal notifications"
echo ""

sudo certbot --nginx -d $DOMAIN --non-interactive --agree-tos --register-unsafely-without-email || \
sudo certbot --nginx -d $DOMAIN

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SSL certificate installed successfully!"
    echo ""
    echo "🎉 Your API is now available at:"
    echo "   https://$DOMAIN"
    echo ""
    echo "📝 Next steps:"
    echo "1. Update frontend/config.js:"
    echo "   window.API_BASE_URL = \"https://$DOMAIN\";"
    echo ""
    echo "2. Test the API:"
    echo "   curl https://$DOMAIN/health"
    echo ""
    echo "3. Deploy to Vercel:"
    echo "   cd frontend && vercel --prod"
    echo ""
    echo "🔄 SSL certificate will auto-renew every 90 days"
else
    echo ""
    echo "❌ SSL certificate installation failed"
    echo ""
    echo "Common issues:"
    echo "1. Domain doesn't resolve to this IP yet (check DNS)"
    echo "2. Port 80 is blocked (check firewall)"
    echo "3. Another service is using port 80"
    echo ""
    echo "Troubleshooting:"
    echo "- Check DNS: dig +short $DOMAIN"
    echo "- Check port 80: sudo netstat -tlnp | grep :80"
    echo "- Check firewall: sudo ufw status"
fi

# Setup auto-renewal
echo "⚙️  Setting up automatic SSL renewal..."
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

echo ""
echo "✅ Setup complete!"

