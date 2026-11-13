@echo off
title KL Campus Navigation System
echo ===================================================
echo     KL Campus Navigation System — Starting Up...
echo ===================================================
echo.

python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install requirements.
    pause
    exit /b %errorlevel%
)

echo.
echo Starting FastAPI web server at http://localhost:8000 ...
echo Press Ctrl+C to stop the server.
echo.
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
pause
