#!/bin/bash

# Test Frontend Connection to Backend
# Northeastern University Chatbot - Lambda GPU

echo "🧪 TESTING FRONTEND CONNECTION TO BACKEND"
echo "=========================================="

# Check if backend is running
echo "1. Checking if backend API is running..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend API is running on port 8000"
else
    echo "❌ Backend API is not running on port 8000"
    echo "   Please start the backend first:"
    echo "   ./start_chatbot.sh"
    exit 1
fi

# Test health endpoint
echo ""
echo "2. Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:8000/health)
if [ $? -eq 0 ]; then
    echo "✅ Health endpoint working"
    echo "   Response: $(echo $HEALTH_RESPONSE | head -c 100)..."
else
    echo "❌ Health endpoint failed"
fi

# Test documents endpoint
echo ""
echo "3. Testing documents endpoint..."
DOCS_RESPONSE=$(curl -s http://localhost:8000/documents)
if [ $? -eq 0 ]; then
    echo "✅ Documents endpoint working"
    echo "   Response: $(echo $DOCS_RESPONSE | head -c 100)..."
else
    echo "❌ Documents endpoint failed"
fi

# Test chat endpoint
echo ""
echo "4. Testing chat endpoint..."
CHAT_RESPONSE=$(curl -s -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"question": "What programs does Northeastern offer?"}')
if [ $? -eq 0 ]; then
    echo "✅ Chat endpoint working"
    echo "   Response: $(echo $CHAT_RESPONSE | head -c 100)..."
else
    echo "❌ Chat endpoint failed"
fi

echo ""
echo "🎯 FRONTEND CONNECTION TEST COMPLETE"
echo "===================================="
echo ""
echo "If all tests passed, your frontend should now connect properly!"
echo ""
echo "To start the frontend:"
echo "  cd frontend"
echo "  python3 server.py"
echo ""
echo "Then open: http://localhost:3000"
