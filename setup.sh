#!/bin/bash

# RAG Document Assistant - Setup Script for Linux/macOS

set -e  # Exit on error

echo ""
echo "================================================================"
echo "  RAG Document Assistant - Setup"
echo "================================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 is not installed"
    echo "Please install Python 3.11+ using: brew install python3 (macOS) or apt install python3 (Linux)"
    exit 1
fi

echo "[OK] Python found: $(python3 --version)"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "[OK] Virtual environment created"
else
    echo "[OK] Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "[WARNING] .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "[NOTICE] Edit .env with your actual API keys"
    echo ""
    echo "[IMPORTANT] Add your MISTRAL_API_KEY to .env file"
    echo "You can get it from: https://console.mistral.ai/api-keys"
fi

# Initialize database if needed
if [ ! -d "chroma_db" ]; then
    echo ""
    echo "Initializing vector database..."
    echo "[NOTICE] Make sure you have a PDF file at: documents_loaders/deep_learning.pdf"
    echo ""
    python create_db.py
else
    echo "[OK] Vector database already initialized"
fi

echo ""
echo "================================================================"
echo "  Setup Complete!"
echo "================================================================"
echo ""
echo "To start the application:"
echo "  streamlit run app.py"
echo ""
echo "Or for CLI interface:"
echo "  python core.py"
echo ""
echo "Virtual environment info:"
echo "  To deactivate: deactivate"
echo "  To reactivate: source venv/bin/activate"
echo ""
