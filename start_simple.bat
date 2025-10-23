@echo off
echo Starting Northeastern University Chatbot - Simple Version...
echo =========================================================

REM Check if we're in the right directory
if not exist "services\chat_service\simple_api.py" (
    echo Error: Please run this script from the project root directory
    pause
    exit /b 1
)

REM Load environment variables if .env file exists
if exist ".env" (
    echo Environment variables loaded
    for /f "tokens=1,2 delims==" %%a in (.env) do (
        if not "%%a"=="" if not "%%a:~0,1%"=="#" set %%a=%%b
    )
) else (
    echo Warning: No .env file found. Make sure environment variables are set.
)

REM Set PYTHONPATH
set PYTHONPATH=%CD%;%PYTHONPATH%

REM Start the simple API server
echo Starting Simple API server on port 8000...
python services\chat_service\simple_api.py

pause
