@echo off
REM Quick start script for Cegid Y2 MCP Server on Windows

echo ================================
echo Cegid Y2 MCP Server - Quick Start
echo ================================
echo.

REM Check if .env file exists
if not exist "config\.env" (
    echo Creating .env file from template...
    copy config\.env.example config\.env
    echo [OK] .env file created at config\.env
    echo      Please edit it with your credentials:
    echo      notepad config\.env
    echo.
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3 is required but not installed.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do echo [OK] %%i found
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt
echo [OK] Dependencies installed

REM Create logs directory
if not exist "logs" mkdir logs

REM Start server
echo.
echo ================================
echo Starting Cegid Y2 MCP Server...
echo ================================
echo.
echo Server available at: http://localhost:8000
echo API Docs at: http://localhost:8000/docs
echo ReDoc at: http://localhost:8000/redoc
echo.
echo Press Ctrl+C to stop
echo.

python src\mcp_server.py
pause
