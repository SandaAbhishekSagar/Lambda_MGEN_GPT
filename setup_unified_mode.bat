@echo off
REM Unified collection mode setup for 80,000 records in single collection

echo Setting up unified collection mode...

REM Set performance mode to unified
set PERFORMANCE_MODE=unified
set USE_CLOUD_CHROMA=true

REM Optimize OpenAI settings for speed
set OPENAI_MAX_TOKENS=400
set OPENAI_TEMPERATURE=0.2
set OPENAI_MODEL=gpt-4o-mini

REM Optimize search settings for unified collection
set MAX_WORKERS=10
set TIMEOUT_PER_COLLECTION=2
set RESULTS_PER_COLLECTION=5

echo Unified collection configuration:
echo PERFORMANCE_MODE=%PERFORMANCE_MODE%
echo USE_CLOUD_CHROMA=%USE_CLOUD_CHROMA%
echo OPENAI_MAX_TOKENS=%OPENAI_MAX_TOKENS%
echo MAX_WORKERS=%MAX_WORKERS%

echo Starting chatbot with unified collection (80,000 records)...
echo This mode uses a single optimized collection for maximum speed!
python services/chat_service/lambda_gpu_chatbot_optimized.py
