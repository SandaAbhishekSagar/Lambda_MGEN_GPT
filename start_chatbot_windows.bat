@echo off
REM Start Lambda GPU Chatbot - Windows Version
REM Northeastern University Chatbot with GPU acceleration

echo 🚀 STARTING LAMBDA GPU CHATBOT
echo ===============================

REM Activate virtual environment
call lambda_gpu_env\Scripts\activate.bat

REM Load environment variables
if exist .env (
    echo ✅ Loading environment variables from .env
    for /f "usebackq tokens=1,2 delims==" %%a in (.env) do (
        if not "%%a"=="" if not "%%a"=="#" (
            set %%a=%%b
        )
    )
) else (
    echo ⚠️  Warning: .env file not found
)

REM Start the API server
echo 🚀 Starting Lambda GPU API server...
python services\chat_service\lambda_gpu_api.py

echo ✅ Chatbot started successfully!
echo 🌐 API Server: http://localhost:8000
echo 📊 Health Check: http://localhost:8000/health
echo 💬 Chat: http://localhost:8000/chat
echo 📚 Docs: http://localhost:8000/docs
