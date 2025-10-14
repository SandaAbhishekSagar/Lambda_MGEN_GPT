#!/bin/bash
# Quick setup script for Lambda Labs + Vercel integration

echo "🚀 Lambda Labs + Vercel Integration Setup"
echo "=========================================="
echo ""

# Get Lambda Labs public IP
echo "📍 Getting your Lambda Labs public IP..."
PUBLIC_IP=$(curl -s ifconfig.me)
echo "✅ Your public IP: $PUBLIC_IP"
echo ""

# API URL
API_URL="http://${PUBLIC_IP}:8000"
echo "🌐 Your API URL: $API_URL"
echo ""

# Test API health
echo "🧪 Testing API health..."
if curl -s "${API_URL}/health" > /dev/null; then
    echo "✅ API is responding!"
    echo ""
    echo "📊 API Health Status:"
    curl -s "${API_URL}/health" | python3 -m json.tool
    echo ""
else
    echo "❌ API is not responding. Please check:"
    echo "   1. Is the API running? (./start_lambda_gpu.sh)"
    echo "   2. Is port 8000 open in firewall?"
    echo "   3. Is the API bound to 0.0.0.0?"
    echo ""
    exit 1
fi

# Test GPU info
echo "🎮 GPU Information:"
curl -s "${API_URL}/gpu-info" | python3 -m json.tool
echo ""

# Update frontend config
echo "📝 Updating frontend configuration..."
cd frontend

# Backup existing config
if [ -f "config.js" ]; then
    cp config.js config.js.backup
    echo "✅ Backed up existing config.js to config.js.backup"
fi

# Create new config
cat > config.js << EOF
// Lambda Labs GPU Backend Configuration
// Auto-generated on $(date)
// Lambda Labs IP: ${PUBLIC_IP}

// Production API URL
window.API_BASE_URL = "${API_URL}";

// Alternative: Use HTTPS with custom domain
// window.API_BASE_URL = "https://your-domain.com";
EOF

echo "✅ Updated frontend/config.js with Lambda Labs URL"
echo ""

# Show next steps
echo "🎯 Next Steps:"
echo "=============="
echo ""
echo "1. Deploy frontend to Vercel:"
echo "   cd frontend"
echo "   vercel --prod"
echo ""
echo "2. Test your deployment:"
echo "   curl ${API_URL}/health"
echo ""
echo "3. Open your Vercel URL in browser and test the chatbot"
echo ""
echo "4. (Optional) Set up custom domain with SSL:"
echo "   - Point your domain to: ${PUBLIC_IP}"
echo "   - Set up Nginx reverse proxy"
echo "   - Install Let's Encrypt SSL certificate"
echo ""
echo "📚 For detailed instructions, see: LAMBDA_VERCEL_INTEGRATION.md"
echo ""

# Offer to deploy to Vercel
read -p "Would you like to deploy to Vercel now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Deploying to Vercel..."
    
    # Check if vercel CLI is installed
    if ! command -v vercel &> /dev/null; then
        echo "📦 Installing Vercel CLI..."
        npm install -g vercel
    fi
    
    # Deploy
    cd frontend
    vercel --prod
    
    echo ""
    echo "✅ Deployment complete!"
else
    echo "👍 Skipping Vercel deployment"
    echo "   You can deploy later with: cd frontend && vercel --prod"
fi

echo ""
echo "🎉 Integration setup complete!"
echo ""
echo "📋 Configuration Summary:"
echo "   Lambda IP: ${PUBLIC_IP}"
echo "   API URL: ${API_URL}"
echo "   Frontend Config: frontend/config.js"
echo ""
echo "🔗 Useful Commands:"
echo "   Test API: curl ${API_URL}/health"
echo "   Monitor GPU: ./monitor_gpu.sh"
echo "   View logs: tail -f /var/log/chatbot.log"
echo ""

