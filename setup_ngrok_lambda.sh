#!/bin/bash
# Quick HTTPS setup using Ngrok (temporary solution)

echo "🚇 Setting up Ngrok tunnel for Lambda Labs"
echo "==========================================="
echo ""

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "📦 Installing Ngrok..."
    
    # Download and install ngrok
    wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
    tar xvzf ngrok-v3-stable-linux-amd64.tgz
    sudo mv ngrok /usr/local/bin/
    rm ngrok-v3-stable-linux-amd64.tgz
    
    echo "✅ Ngrok installed"
else
    echo "✅ Ngrok already installed"
fi

echo ""
echo "⚠️  Important: Ngrok Setup"
echo "=========================="
echo ""
echo "1. Sign up for free at: https://dashboard.ngrok.com/signup"
echo "2. Get your authtoken from: https://dashboard.ngrok.com/get-started/your-authtoken"
echo "3. Run: ngrok config add-authtoken YOUR_TOKEN"
echo ""

read -p "Have you configured your authtoken? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Please configure ngrok first:"
    echo "1. Visit: https://dashboard.ngrok.com/signup"
    echo "2. Get your token"
    echo "3. Run: ngrok config add-authtoken YOUR_TOKEN"
    echo "4. Run this script again"
    exit 1
fi

# Start ngrok tunnel
echo ""
echo "🚇 Starting Ngrok tunnel..."
echo ""
echo "⚠️  Keep this terminal open!"
echo "   Closing it will stop the tunnel"
echo ""

# Start ngrok in background and capture URL
ngrok http 8000 > /dev/null &
NGROK_PID=$!

# Wait for ngrok to start
sleep 3

# Get the public URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])" 2>/dev/null)

if [ -z "$NGROK_URL" ]; then
    echo "❌ Failed to get Ngrok URL"
    echo "   Make sure ngrok is configured correctly"
    kill $NGROK_PID 2>/dev/null
    exit 1
fi

echo "✅ Ngrok tunnel started!"
echo ""
echo "🌐 Your HTTPS URL: $NGROK_URL"
echo ""
echo "📝 Update frontend/config.js:"
echo "   window.API_BASE_URL = \"$NGROK_URL\";"
echo ""
echo "🧪 Test the API:"
echo "   curl $NGROK_URL/health"
echo ""
echo "⚠️  Important Notes:"
echo "   - This URL is temporary and changes on restart"
echo "   - Free tier has limitations (40 requests/min)"
echo "   - For production, use a custom domain with SSL"
echo ""
echo "🔄 To stop the tunnel:"
echo "   kill $NGROK_PID"
echo ""
echo "Press Ctrl+C to stop the tunnel and exit"
echo ""

# Keep script running
wait $NGROK_PID

