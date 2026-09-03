#!/bin/bash

# ============================================================================
# AI OPTIONS TRADING PLATFORM - AUTOMATED SETUP (Linux/macOS)
# ============================================================================

set -e  # Exit on error

echo "================================"
echo "AI Options Trading Platform"
echo "Automated Local Setup (Linux/macOS)"
echo "================================"
echo ""

# ============================================================================
# STEP 1: Check Python
# ============================================================================

echo "Step 1: Checking Python 3.11+..."

if ! command -v python3.11 &> /dev/null; then
    echo "❌ Python 3.11+ not found!"
    echo ""
    echo "Install Python 3.11:"
    echo "  macOS: brew install python@3.11"
    echo "  Linux: sudo apt-get install python3.11"
    exit 1
fi

PYTHON_VERSION=$(python3.11 --version)
echo "✅ Found: $PYTHON_VERSION"

PIP_VERSION=$(pip3 --version)
echo "✅ Found: $PIP_VERSION"
echo ""

# ============================================================================
# STEP 2: Create Virtual Environment
# ============================================================================

echo "Step 2: Creating virtual environment..."

if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists"
    read -p "Delete and recreate? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3.11 -m venv venv
        echo "✅ Virtual environment created"
    fi
else
    python3.11 -m venv venv
    echo "✅ Virtual environment created"
fi

echo ""

# ============================================================================
# STEP 3: Activate Virtual Environment
# ============================================================================

echo "Step 3: Activating virtual environment..."

source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# ============================================================================
# STEP 4: Upgrade pip
# ============================================================================

echo "Step 4: Upgrading pip..."

python -m pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "✅ pip upgraded"
echo ""

# ============================================================================
# STEP 5: Install Dependencies
# ============================================================================

echo "Step 5: Installing Python dependencies..."
echo "This may take 2-3 minutes..."
echo ""

pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# ============================================================================
# STEP 6: Check PostgreSQL
# ============================================================================

echo "Step 6: Checking PostgreSQL..."

if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL not found!"
    echo ""
    echo "Install PostgreSQL 15+:"
    echo "  macOS: brew install postgresql@15"
    echo "  Linux (Ubuntu): sudo apt-get install postgresql postgresql-contrib"
    echo ""
    echo "Then start it:"
    echo "  macOS: brew services start postgresql@15"
    echo "  Linux: sudo systemctl start postgresql"
    exit 1
fi

PSQL_VERSION=$(psql --version)
echo "✅ Found: $PSQL_VERSION"
echo ""

# ============================================================================
# STEP 7: Check Redis
# ============================================================================

echo "Step 7: Checking Redis..."

if ! command -v redis-cli &> /dev/null; then
    echo "⚠️  Redis not found"
    echo ""
    echo "Install Redis:"
    echo "  macOS: brew install redis"
    echo "  Linux: sudo apt-get install redis-server"
    echo ""
    echo "Then start it:"
    echo "  macOS: brew services start redis"
    echo "  Linux: sudo systemctl start redis-server"
    echo ""
    echo "Continuing without Redis (some features may not work)..."
else
    REDIS_VERSION=$(redis-cli --version)
    echo "✅ Found: $REDIS_VERSION"
fi

echo ""

# ============================================================================
# STEP 8: Create .env Configuration
# ============================================================================

echo "Step 8: Creating .env configuration..."

if [ -f ".env" ]; then
    echo "✅ .env file already exists"
else
    cp .env.example .env
    echo "✅ .env file created from template"
fi

echo ""

# ============================================================================
# STEP 9: Create Database
# ============================================================================

echo "Step 9: Creating PostgreSQL database..."
echo ""

# Check if PostgreSQL is running
if ! psql -U postgres -c "SELECT 1" > /dev/null 2>&1; then
    echo "⚠️  PostgreSQL is not running or 'postgres' user not accessible"
    echo ""
    echo "Start PostgreSQL:"
    echo "  macOS: brew services start postgresql@15"
    echo "  Linux: sudo systemctl start postgresql"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create database and user
cat > /tmp/setup.sql << 'EOF'
CREATE USER IF NOT EXISTS trader WITH PASSWORD 'trader123';
CREATE DATABASE IF NOT EXISTS options_trading OWNER trader;
ALTER ROLE trader SET client_encoding TO 'utf8';
ALTER ROLE trader SET default_transaction_isolation TO 'read committed';
ALTER ROLE trader SET default_transaction_deferrable TO on;
ALTER ROLE trader SET default_timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE options_trading TO trader;
EOF

psql -U postgres -f /tmp/setup.sql 2>/dev/null || true
rm /tmp/setup.sql

echo "✅ Database and user created (or already exist)"
echo ""

# ============================================================================
# STEP 10: Initialize Database Schema
# ============================================================================

echo "Step 10: Initializing database schema..."
echo "This creates 20 tables and indexes..."
echo ""

python scripts/init_db.py

echo ""
echo "✅ Database schema initialized"
echo ""

# ============================================================================
# SUMMARY
# ============================================================================

echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""

echo "Next steps:"
echo ""
echo "1. Start PostgreSQL (if not already running):"
echo "   macOS: brew services start postgresql@15"
echo "   Linux: sudo systemctl start postgresql"
echo ""
echo "2. Start Redis (if not already running):"
echo "   macOS: brew services start redis"
echo "   Linux: sudo systemctl start redis-server"
echo ""
echo "3. Start the application:"
echo "   ./start-local.sh"
echo "   # OR manually:"
echo "   cd backend"
echo "   python main.py"
echo ""
echo "4. Test the API (in new terminal):"
echo "   curl http://localhost:8000/health"
echo ""
echo "5. View API documentation:"
echo "   http://localhost:8000/api/docs"
echo ""

echo "================================"
echo "Setup Complete! Ready to run."
echo "================================"

# Keep virtual environment activated for user
echo ""
echo "Virtual environment is activated. To deactivate later, type: deactivate"
