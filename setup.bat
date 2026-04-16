@echo off
REM RAG Document Assistant - Setup Script for Windows

echo.
echo ================================================================
echo  RAG Document Assistant - Setup
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python found

REM Create virtual environment
if not exist "venv" (
    echo.
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Check for .env file
if not exist ".env" (
    echo.
    echo [WARNING] .env file not found!
    echo Creating .env from .env.example...
    copy .env.example .env
    echo [NOTICE] Edit .env with your actual API keys
    echo.
    echo [IMPORTANT] Add your MISTRAL_API_KEY to .env file
    echo You can get it from: https://console.mistral.ai/api-keys
)

REM Initialize database if needed
if not exist "chroma_db" (
    echo.
    echo Initializing vector database...
    echo [NOTICE] Make sure you have a PDF file at: documents_loaders/deep_learning.pdf
    echo.
    python create_db.py
) else (
    echo [OK] Vector database already initialized
)

echo.
echo ================================================================
echo  Setup Complete!
echo ================================================================
echo.
echo To start the application:
echo   streamlit run app.py
echo.
echo Or for CLI interface:
echo   python core.py
echo.
pause
