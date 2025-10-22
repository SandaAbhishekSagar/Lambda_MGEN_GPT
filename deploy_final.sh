#!/bin/bash

# Final Lambda Labs GPU Deployment Script
# Ultra-fast Northeastern University Chatbot

echo "🚀 LAMBDA LABS GPU DEPLOYMENT - FINAL VERSION"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "services/chat_service/lambda_gpu_api.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source lambda_gpu_env/bin/activate

# Stop any existing servers
echo "🛑 Stopping existing servers..."
pkill -f "lambda_gpu_api" || true

# Wait a moment
sleep 2

# Start the API server
echo "🚀 Starting Lambda GPU API server..."
python3 services/chat_service/lambda_gpu_api.py &

# Wait for server to start
echo "⏳ Waiting for server to start..."
sleep 5

# Test the server
echo "🧪 Testing server endpoints..."

# Test health endpoint
echo "Testing health endpoint..."
curl -s http://localhost:8000/health | head -c 100
echo ""

# Test documents endpoint
echo "Testing documents endpoint..."
curl -s http://localhost:8000/documents | head -c 100
echo ""

# Test chat endpoint
echo "Testing chat endpoint..."
curl -s -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"question": "What programs does Northeastern offer?"}' | head -c 100
echo ""

echo "✅ Deployment complete!"
echo ""
echo "🌐 Your services are now running:"
echo "   - API Server: http://localhost:8000"
echo "   - Health Check: http://localhost:8000/health"
echo "   - Documents: http://localhost:8000/documents"
echo "   - Chat: http://localhost:8000/chat"
echo ""
echo "📊 To start the frontend:"
echo "   cd frontend"
echo "   python3 server.py"
echo ""
echo "🎉 Your Lambda Labs GPU chatbot is ready!"

