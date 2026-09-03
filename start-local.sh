#!/bin/bash

# ============================================================================
# START LOCAL DEVELOPMENT SERVER (Linux/macOS)
# ============================================================================

set -e

echo "================================"
echo "Starting AI Options Trading Platform"
echo "================================"
echo ""

# Check virtual environment
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: ./setup-linux-macos.sh"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Check PostgreSQL
echo "Checking PostgreSQL..."
if psql -U postgres -c "SELECT 1" > /dev/null 2>&1; then
    echo "✅ PostgreSQL is running"
else
    echo "❌ PostgreSQL is not running!"
    echo ""
    echo "Start PostgreSQL:"
    echo "  macOS: brew services start postgresql@15"
    echo "  Linux: sudo systemctl start postgresql"
    exit 1
fi

echo ""

# Check Redis (optional)
echo "Checking Redis..."
if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis is running"
else
    echo "⚠️  Redis is not running (optional)"
    echo "   Some features may not work optimally"
fi

echo ""

# Navigate to backend
cd backend

# Run application
echo "Starting FastAPI backend..."
echo "================================"
echo ""

python main.py

# If we get here, app exited
echo ""
echo "Application stopped."
