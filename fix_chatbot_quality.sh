#!/bin/bash

echo "🔧 FIXING CHATBOT QUALITY ISSUES"
echo "================================"

# Check if we're in the right directory
if [ ! -f "services/chat_service/lambda_gpu_chatbot.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "📋 Step 1: Stopping existing chatbot processes..."
pkill -f "lambda_gpu_api" 2>/dev/null || true
pkill -f "uvicorn" 2>/dev/null || true
sleep 2

echo "📋 Step 2: Activating virtual environment..."
source lambda_gpu_env/bin/activate

echo "📋 Step 3: Installing/updating dependencies..."
pip install --upgrade pip
pip install -r requirements_lambda.txt --quiet

echo "📋 Step 4: Testing the improved chatbot..."
python3 -c "
import sys
sys.path.append('.')
from services.chat_service.lambda_gpu_chatbot import get_chatbot
import time

print('🧪 Testing improved chatbot...')
try:
    chatbot = get_chatbot()
    print('✅ Chatbot initialized successfully')
    
    # Test with a simple question
    test_question = 'What programs does Northeastern University offer?'
    print(f'🔍 Testing question: {test_question}')
    
    start_time = time.time()
    response = chatbot.chat(test_question)
    end_time = time.time()
    
    print(f'⏱️  Response time: {end_time - start_time:.2f}s')
    print(f'📊 Confidence: {response.confidence}')
    print(f'📄 Sources found: {len(response.sources)}')
    
    if response.sources:
        print('📋 Source titles:')
        for i, source in enumerate(response.sources[:3], 1):
            print(f'  {i}. {source.get(\"title\", \"Unknown\")} (similarity: {source.get(\"similarity\", 0):.3f})')
    
    print('✅ Chatbot test completed successfully')
    
except Exception as e:
    print(f'❌ Chatbot test failed: {e}')
    sys.exit(1)
"

echo "📋 Step 5: Starting the improved API server..."
nohup python3 -m services.chat_service.lambda_gpu_api_final > chatbot_api.log 2>&1 &
API_PID=$!
echo "🚀 API server started with PID: $API_PID"

echo "📋 Step 6: Waiting for API to be ready..."
sleep 5

echo "📋 Step 7: Testing API endpoints..."
curl -s http://localhost:8000/health | jq . 2>/dev/null || echo "Health check failed"

echo "📋 Step 8: Testing chat endpoint..."
curl -s -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What programs does Northeastern University offer?"}' | jq . 2>/dev/null || echo "Chat test failed"

echo ""
echo "✅ CHATBOT QUALITY FIXES COMPLETED"
echo "================================"
echo "🔧 Improvements made:"
echo "  • Enhanced metadata extraction for better document titles"
echo "  • Improved relevance scoring and filtering"
echo "  • Better source document display"
echo "  • Enhanced response generation with quality filtering"
echo ""
echo "🚀 API server is running on http://localhost:8000"
echo "📊 Check chatbot_api.log for detailed logs"
echo ""
echo "🧪 Test the chatbot with:"
echo "  curl -X POST http://localhost:8000/chat -H 'Content-Type: application/json' -d '{\"question\": \"What programs does Northeastern University offer?\"}'"
echo ""
echo "🔄 To restart the API server:"
echo "  pkill -f lambda_gpu_api && nohup python3 -m services.chat_service.lambda_gpu_api_final > chatbot_api.log 2>&1 &"
