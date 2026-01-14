#!/bin/bash
# Quick start script for Cegid Y2 MCP Server

set -e

echo "================================"
echo "Cegid Y2 MCP Server - Quick Start"
echo "================================"
echo ""

# Check if .env file exists
if [ ! -f "config/.env" ]; then
    echo "Creating .env file from template..."
    cp config/.env.example config/.env
    echo "✓ .env file created at config/.env"
    echo "  Please edit it with your credentials:"
    echo "  nano config/.env"
    echo ""
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

echo "✓ Python $(python3 --version) found"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Create logs directory
mkdir -p logs

# Start server
echo ""
echo "================================"
echo "Starting Cegid Y2 MCP Server..."
echo "================================"
echo ""
echo "Server available at: http://localhost:8000"
echo "API Docs at: http://localhost:8000/docs"
echo "ReDoc at: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python src/mcp_server.py
