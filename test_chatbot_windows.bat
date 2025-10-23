@echo off
REM Test Lambda GPU Chatbot - Windows Version
REM Tests all endpoints and functionality

echo 🧪 TESTING LAMBDA GPU CHATBOT
echo ==============================

REM Activate virtual environment
call lambda_gpu_env\Scripts\activate.bat

echo 📦 Step 1: Testing HuggingFace compatibility...
python -c "
import sys
try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings = model.encode(['test sentence'])
    print('✅ HuggingFace compatibility working!')
    sys.exit(0)
except Exception as e:
    print(f'❌ HuggingFace test failed: {e}')
    sys.exit(1)
"

if %errorlevel% neq 0 (
    echo ❌ HuggingFace test failed
    exit 1
)

echo ✅ HuggingFace compatibility test passed!

echo.
echo 📦 Step 2: Testing chatbot initialization...
python -c "
import sys
try:
    from services.chat_service.lambda_gpu_chatbot import LambdaGPUChatbot
    chatbot = LambdaGPUChatbot()
    print('✅ Chatbot initialization successful!')
    sys.exit(0)
except Exception as e:
    print(f'❌ Chatbot initialization failed: {e}')
    sys.exit(1)
"

if %errorlevel% neq 0 (
    echo ❌ Chatbot initialization failed
    exit 1
)

echo ✅ Chatbot initialization test passed!

echo.
echo 📦 Step 3: Testing API endpoints...
echo Testing health endpoint...
curl -s http://localhost:8000/health > nul
if %errorlevel% equ 0 (
    echo ✅ Health endpoint working
) else (
    echo ❌ Health endpoint failed - make sure API server is running
)

echo Testing documents endpoint...
curl -s http://localhost:8000/documents > nul
if %errorlevel% equ 0 (
    echo ✅ Documents endpoint working
) else (
    echo ❌ Documents endpoint failed
)

echo Testing chat endpoint...
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{\"question\": \"What programs does Northeastern offer?\"}" > nul
if %errorlevel% equ 0 (
    echo ✅ Chat endpoint working
) else (
    echo ❌ Chat endpoint failed
)

echo.
echo 🎉 ALL TESTS COMPLETED!
echo ======================
echo.
echo 🚀 To start your chatbot:
echo    start_chatbot_windows.bat
echo.
echo 🌐 To start frontend:
echo    cd frontend
echo    python server.py
echo.
echo 📊 To monitor GPU:
echo    nvidia-smi
