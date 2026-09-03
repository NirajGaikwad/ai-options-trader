# Quick Start Guide - AI Options Trading Platform

Get up and running in 5 minutes with the simulator (no broker needed).

## ⚠️ Important

- **Paper Trading Only**: This setup runs in paper trading mode (simulated trades)
- **No Real Capital**: No real money is at risk
- **Simulator Data**: Uses realistic but synthetic market data
- **Testing Only**: For development and learning purposes

---

## Prerequisites

- Docker & Docker Compose (recommended)
- OR Python 3.11+, PostgreSQL, Redis

---

## Option 1: Docker Compose (5 Minutes)

### Step 1: Clone Repository
```bash
git clone <repo-url>
cd ai-options-trader
```

### Step 2: Copy Environment Template
```bash
cp .env.example .env

# Verify critical settings
grep PAPER_TRADING .env
grep LIVE_TRADING_ENABLED .env

# Output should show:
# PAPER_TRADING=true
# LIVE_TRADING_ENABLED=false
```

### Step 3: Start All Services
```bash
docker-compose up -d

# Wait for services to start (~30 seconds)
sleep 30

# Check status
docker-compose ps

# Should show: postgres, redis, backend, prometheus, grafana, frontend all running
```

### Step 4: Verify Installation
```bash
# Check API health
curl http://localhost:8000/health

# Should return:
# {
#   "status": "ok",
#   "paper_trading": true,
#   "live_trading_enabled": false
# }

# Check logs
docker-compose logs backend | tail -20
```

### Step 5: Access Dashboard

**API Documentation**
```
http://localhost:8000/api/docs
```

**Frontend Dashboard** (if built)
```
http://localhost:3000
```

**Prometheus Metrics**
```
http://localhost:9090
```

**Grafana Dashboards**
```
http://localhost:3001
Login: admin / admin
```

---

## Option 2: Local Setup (Without Docker)

### Step 1: Install Python
```bash
# Check Python version
python3 --version  # Should be 3.11+

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate     # Windows
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Start PostgreSQL
```bash
# macOS
brew services start postgresql

# Linux
sudo systemctl start postgresql

# Windows (if installed)
# Start from Services or command line
```

### Step 4: Create Database
```bash
psql -U postgres

# In PostgreSQL:
CREATE USER trader WITH PASSWORD 'trader123';
CREATE DATABASE options_trading OWNER trader;
\q
```

### Step 5: Start Redis
```bash
# macOS
brew services start redis

# Linux
sudo systemctl start redis-server

# Verify running
redis-cli ping
# Should return: PONG
```

### Step 6: Initialize Database
```bash
python scripts/init_db.py
```

### Step 7: Run Application
```bash
cd backend
python main.py

# Should show:
# ✅ Application startup complete!
# INFO: Uvicorn running on http://0.0.0.0:8000
```

### Step 8: Access API
```
http://localhost:8000/api/docs
```

---

## Testing the API

### Get Market Data
```bash
# Get NIFTY 50 snapshot
curl http://localhost:8000/api/market/index/NIFTY | jq '.'

# Output example:
# {
#   "timestamp": "2024-03-15T10:30:00",
#   "instrument": "NIFTY",
#   "ltp": 23456.78,
#   "open": 23400.0,
#   "high": 23500.0,
#   "low": 23350.0,
#   "volume": 2500000,
#   "change_percent": 0.24
# }
```

### Get Option Chain
```bash
# Get option chain for NIFTY
# Expiry date format: YYYY-MM-DD
curl "http://localhost:8000/api/market/option-chain/NIFTY?expiry_date=2024-03-28" | jq '.' | head -50

# Returns: ATM and nearby strikes with calls & puts
```

### Get Candlestick Data
```bash
# Get 5-minute candles
curl "http://localhost:8000/api/market/candles/NIFTY?interval_minutes=5&limit=20" | jq '.'

# Returns: Recent 20 five-minute candles
```

### Check Trading Status
```bash
curl http://localhost:8000/api/trading/status | jq '.'

# Output:
# {
#   "paper_trading": true,
#   "live_trading_enabled": false,
#   "trading_active": false,
#   "emergency_stop": false
# }
```

---

## Interactive API Testing

### Option 1: Swagger UI (Recommended)
```
http://localhost:8000/api/docs

Click "Try it out" on any endpoint
```

### Option 2: Command Line with jq
```bash
# Pretty print JSON
curl -s http://localhost:8000/api/market/index/NIFTY | jq '.'

# Extract specific field
curl -s http://localhost:8000/api/market/index/NIFTY | jq '.ltp'

# Filter results
curl -s "http://localhost:8000/api/market/option-chain/NIFTY?expiry_date=2024-03-28" | \
  jq '.chains[] | select(.strike > 23000) | {strike, ce_ltp, pe_ltp}'
```

### Option 3: Python Script
```python
import requests
import json

# Base URL
api_url = "http://localhost:8000"

# Get NIFTY snapshot
response = requests.get(f"{api_url}/api/market/index/NIFTY")
nifty_data = response.json()

print(f"NIFTY LTP: {nifty_data['ltp']}")
print(f"Volume: {nifty_data['volume']}")
print(f"Change: {nifty_data['change_percent']}%")

# Get option chain
response = requests.get(
    f"{api_url}/api/market/option-chain/NIFTY",
    params={"expiry_date": "2024-03-28"}
)
options = response.json()

print(f"\nFound {len(options['chains'])} strikes")
for chain in options['chains'][:3]:  # First 3 strikes
    print(f"Strike {chain['strike']}: CE={chain['ce_ltp']}, PE={chain['pe_ltp']}")
```

---

## Next Steps

### 1. Explore API Documentation
- Open http://localhost:8000/api/docs
- Try different endpoints
- Read parameter descriptions

### 2. Study the Codebase
```bash
# Key files to review:
cat backend/main.py              # Main application
cat backend/market_data/base.py  # Data provider interface
cat backend/config/settings.py   # Configuration
cat backend/db/models.py         # Database schema
```

### 3. Review Simulator Data
The simulator generates realistic:
- NIFTY 50 & SENSEX candles
- Option chain with Greeks
- Realistic spreads and OI
- Volume patterns

### 4. Check Logs
```bash
# Docker
docker-compose logs -f backend

# Local
tail -f logs/application.log
```

### 5. Monitor Metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001

---

## Stopping Services

### Docker
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (careful - removes data!)
docker-compose down -v

# View logs before stopping
docker-compose logs -f backend
```

### Local
```bash
# Stop API (Ctrl+C in terminal)

# Stop services
brew services stop redis
brew services stop postgresql

# Or stop all
brew services stop --all
```

---

## Troubleshooting

### Services Not Starting
```bash
# Check Docker
docker --version
docker-compose ps

# Check logs
docker-compose logs backend

# Restart
docker-compose restart backend
```

### Connection Refused
```bash
# Database
psql -U trader -h localhost -d options_trading

# Redis
redis-cli ping

# API
curl http://localhost:8000/health
```

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Or change port in .env
API_PORT=8001
```

### Database Issues
```bash
# Drop and recreate
docker-compose exec postgres dropdb -U trader options_trading
docker-compose exec postgres createdb -U trader options_trading

# Re-initialize
python scripts/init_db.py
```

---

## Safety Checklist

Before proceeding to Phase 2:

- [ ] API responds to all endpoints
- [ ] Market data is updating
- [ ] Database is storing data
- [ ] Paper trading is confirmed enabled
- [ ] Live trading is confirmed disabled
- [ ] No errors in logs
- [ ] Familiar with emergency stop procedure
- [ ] Read all safety warnings in README

---

## Common API Patterns

### Market Data (Real-time)
```bash
# Index
GET /api/market/index/{instrument}

# Option Chain
GET /api/market/option-chain/{instrument}?expiry_date=2024-03-28

# Candles
GET /api/market/candles/{instrument}?interval_minutes=5&limit=100
```

### Trading Status
```bash
# Status
GET /api/trading/status

# Emergency Stop
POST /api/trading/emergency-stop

# Resume
POST /api/trading/resume
```

### Health
```bash
# Quick check
GET /health

# Detailed check
GET /health/detailed
```

---

## What's Running

| Service | Port | Purpose |
|---------|------|---------|
| Backend API | 8000 | Core trading engine |
| Frontend | 3000 | Web dashboard |
| PostgreSQL | 5432 | Historical data |
| Redis | 6379 | Caching & queue |
| Prometheus | 9090 | Metrics collection |
| Grafana | 3001 | Visualization |

---

## Next Phase

After verifying this quick start works:

1. **Phase 1 Complete**: Data engine + API running ✅
2. **Phase 2 (Next)**: Technical indicators & charts
3. **Phase 3**: Option chain analytics
4. **Phase 4**: Signal generation
5. **Phase 5**: Backtesting engine
6. **Phase 6**: Paper trading simulation
7. **Phase 7**: News intelligence
8. **Phase 8**: Machine learning
9. **Phase 9**: Risk management
10. **Phase 10**: Broker integration
11. **Phase 11**: Live trading

---

## Key Files

| File | Purpose |
|------|---------|
| `.env` | Configuration |
| `backend/main.py` | API application |
| `backend/db/models.py` | Database schema |
| `backend/config/settings.py` | Settings |
| `backend/market_data/simulator.py` | Test data |
| `requirements.txt` | Dependencies |
| `docker-compose.yml` | Containerization |
| `SETUP.md` | Full setup guide |
| `README.md` | Project overview |

---

## Support

- **API Docs**: http://localhost:8000/api/docs
- **Logs**: `docker-compose logs -f backend`
- **Health**: http://localhost:8000/health
- **Issues**: Check application logs for errors

---

**Happy Trading! Remember: Paper Trading First! 📊**
