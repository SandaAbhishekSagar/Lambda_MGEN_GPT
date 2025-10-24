@echo off
REM Ultra-fast unified collection mode for sub-8-second responses

echo Setting up ultra-fast unified collection mode...

REM Set performance mode to ultra-fast
set PERFORMANCE_MODE=ultra_fast
set USE_CLOUD_CHROMA=true

REM Ultra-fast OpenAI settings
set OPENAI_MAX_TOKENS=300
set OPENAI_TEMPERATURE=0.2
set OPENAI_MODEL=gpt-4.1-mini

REM Optimize search settings for maximum speed
set MAX_WORKERS=10
set TIMEOUT_PER_COLLECTION=2
set RESULTS_PER_COLLECTION=3

echo Ultra-fast unified collection configuration:
echo PERFORMANCE_MODE=%PERFORMANCE_MODE%
echo USE_CLOUD_CHROMA=%USE_CLOUD_CHROMA%
echo OPENAI_MODEL=%OPENAI_MODEL%
echo OPENAI_MAX_TOKENS=%OPENAI_MAX_TOKENS%
echo OPENAI_TEMPERATURE=%OPENAI_TEMPERATURE%

echo Starting chatbot with ultra-fast unified collection...
echo Expected response time: 3-8 seconds (vs. 12-16 seconds before)
echo This mode uses gpt-4.1-mini with streaming for maximum speed!
python services/chat_service/lambda_gpu_chatbot_optimized.py
