# ============================================================================
# START LOCAL DEVELOPMENT SERVER (Windows PowerShell)
# ============================================================================

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Starting AI Options Trading Platform" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: .\setup-windows.ps1" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Check PostgreSQL
Write-Host "Checking PostgreSQL..." -ForegroundColor Yellow
try {
    psql -U postgres -c "SELECT 1" > $null 2>&1
    Write-Host "✅ PostgreSQL is running" -ForegroundColor Green
} catch {
    Write-Host "❌ PostgreSQL is not running!" -ForegroundColor Red
    Write-Host "Please start PostgreSQL and try again" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Windows Services:" -ForegroundColor Gray
    Write-Host "  Services.msc → Find 'postgresql-x64-15' → Right-click → Start" -ForegroundColor Gray
    exit 1
}

Write-Host ""

# Check Redis (optional)
Write-Host "Checking Redis..." -ForegroundColor Yellow
try {
    redis-cli ping > $null 2>&1
    Write-Host "✅ Redis is running" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Redis is not running (optional)" -ForegroundColor Yellow
    Write-Host "   Some features may not work optimally" -ForegroundColor Gray
}

Write-Host ""

# Navigate to backend
Push-Location backend

# Run application
Write-Host "Starting FastAPI backend..." -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

python main.py

# If we get here, app exited
Pop-Location
Write-Host ""
Write-Host "Application stopped." -ForegroundColor Yellow
