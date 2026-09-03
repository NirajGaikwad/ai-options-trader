# ============================================================================
# AI OPTIONS TRADING PLATFORM - AUTOMATED SETUP (Windows PowerShell)
# ============================================================================

Write-Host "================================" -ForegroundColor Cyan
Write-Host "AI Options Trading Platform" -ForegroundColor Cyan
Write-Host "Automated Local Setup (Windows)" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================================
# STEP 1: Check Python
# ============================================================================

Write-Host "Step 1: Checking Python 3.11+..." -ForegroundColor Yellow

try {
    $pythonVersion = python3 --version 2>&1
    Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python 3.11+ not found!" -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Red
    exit 1
}

# Check pip
$pipVersion = pip --version
Write-Host "✅ Found: $pipVersion" -ForegroundColor Green
Write-Host ""

# ============================================================================
# STEP 2: Create Virtual Environment
# ============================================================================

Write-Host "Step 2: Creating virtual environment..." -ForegroundColor Yellow

if (Test-Path "venv") {
    Write-Host "⚠️  Virtual environment already exists" -ForegroundColor Yellow
    $response = Read-Host "Delete and recreate? (y/n)"
    if ($response -eq "y") {
        Remove-Item -Recurse -Force "venv"
        python3 -m venv venv
        Write-Host "✅ Virtual environment created" -ForegroundColor Green
    }
} else {
    python3 -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

Write-Host ""

# ============================================================================
# STEP 3: Activate Virtual Environment
# ============================================================================

Write-Host "Step 3: Activating virtual environment..." -ForegroundColor Yellow

& ".\venv\Scripts\Activate.ps1"
Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# ============================================================================
# STEP 4: Upgrade pip
# ============================================================================

Write-Host "Step 4: Upgrading pip..." -ForegroundColor Yellow

python -m pip install --upgrade pip setuptools wheel | Out-Null
Write-Host "✅ pip upgraded" -ForegroundColor Green
Write-Host ""

# ============================================================================
# STEP 5: Install Dependencies
# ============================================================================

Write-Host "Step 5: Installing Python dependencies..." -ForegroundColor Yellow
Write-Host "This may take 2-3 minutes..." -ForegroundColor Gray

pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host ""

# ============================================================================
# STEP 6: Check PostgreSQL
# ============================================================================

Write-Host "Step 6: Checking PostgreSQL..." -ForegroundColor Yellow

try {
    $psqlVersion = psql --version 2>&1
    Write-Host "✅ Found: $psqlVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ PostgreSQL not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install PostgreSQL 15+:" -ForegroundColor Yellow
    Write-Host "  1. Download: https://www.postgresql.org/download/windows/" -ForegroundColor Gray
    Write-Host "  2. Run installer" -ForegroundColor Gray
    Write-Host "  3. Remember the password for 'postgres' user" -ForegroundColor Gray
    Write-Host "  4. Re-run this script" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Alternative: Use WSL2 (Windows Subsystem for Linux)" -ForegroundColor Gray
    exit 1
}

Write-Host ""

# ============================================================================
# STEP 7: Check Redis
# ============================================================================

Write-Host "Step 7: Checking Redis..." -ForegroundColor Yellow

try {
    $redisVersion = redis-cli --version 2>&1
    Write-Host "✅ Found: $redisVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Redis not found" -ForegroundColor Yellow
    Write-Host "Installing Redis..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Option 1: Use Windows Subsystem for Linux (WSL2)" -ForegroundColor Gray
    Write-Host "  wsl" -ForegroundColor Gray
    Write-Host "  sudo apt-get install redis-server" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Option 2: Download Windows Redis release" -ForegroundColor Gray
    Write-Host "  https://github.com/microsoftarchive/redis/releases" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Option 3: Using Chocolatey (if installed)" -ForegroundColor Gray
    Write-Host "  choco install redis" -ForegroundColor Gray
    Write-Host ""
    Write-Host "For now, continuing without Redis (may cause issues)..." -ForegroundColor Yellow
}

Write-Host ""

# ============================================================================
# STEP 8: Create .env Configuration
# ============================================================================

Write-Host "Step 8: Creating .env configuration..." -ForegroundColor Yellow

if (Test-Path ".env") {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "✅ .env file created from template" -ForegroundColor Green
}

Write-Host ""

# ============================================================================
# STEP 9: Create Database
# ============================================================================

Write-Host "Step 9: Creating PostgreSQL database..." -ForegroundColor Yellow

$postgresPassword = Read-Host "Enter PostgreSQL 'postgres' user password"

# Create SQL commands
$sqlCommands = @"
CREATE USER trader WITH PASSWORD 'trader123';
CREATE DATABASE options_trading OWNER trader;
ALTER ROLE trader SET client_encoding TO 'utf8';
ALTER ROLE trader SET default_transaction_isolation TO 'read committed';
ALTER ROLE trader SET default_transaction_deferrable TO on;
ALTER ROLE trader SET default_timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE options_trading TO trader;
"@

# Write to temp file
$sqlFile = "temp_setup.sql"
Set-Content -Path $sqlFile -Value $sqlCommands

# Execute SQL
try {
    psql -U postgres -f $sqlFile
    Write-Host "✅ Database and user created" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Database may already exist or password incorrect" -ForegroundColor Yellow
}

# Clean up
Remove-Item $sqlFile

Write-Host ""

# ============================================================================
# STEP 10: Initialize Database Schema
# ============================================================================

Write-Host "Step 10: Initializing database schema..." -ForegroundColor Yellow
Write-Host "This creates 20 tables and indexes..." -ForegroundColor Gray

python scripts/init_db.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database schema initialized" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to initialize database" -ForegroundColor Red
    Write-Host "Check PostgreSQL is running and accessible" -ForegroundColor Red
}

Write-Host ""

# ============================================================================
# SUMMARY
# ============================================================================

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Green
Write-Host ""
Write-Host "1. Start PostgreSQL:" -ForegroundColor Yellow
Write-Host "   # If using Windows service, it should already be running" -ForegroundColor Gray
Write-Host "   # Or from Services app, start 'postgresql-x64-15'" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Start Redis (if installed):" -ForegroundColor Yellow
Write-Host "   redis-server" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Start the application:" -ForegroundColor Yellow
Write-Host "   ./start-local.ps1" -ForegroundColor Gray
Write-Host "   # OR manually:" -ForegroundColor Gray
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   python main.py" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Test the API (in new terminal):" -ForegroundColor Yellow
Write-Host "   curl http://localhost:8000/health" -ForegroundColor Gray
Write-Host ""
Write-Host "5. View API documentation:" -ForegroundColor Yellow
Write-Host "   http://localhost:8000/api/docs" -ForegroundColor Gray
Write-Host ""

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Setup Complete! Ready to run." -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
