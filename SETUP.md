# Setup Guide - AI Options Trading Platform

## ⚠️ CRITICAL SAFETY WARNINGS

1. **This system trades with REAL capital** when live trading is enabled
2. **Paper trading mode is enabled by default** - use this for testing
3. **You can lose 100% of your capital** - never trade with money you can't afford to lose
4. **Thoroughly backtest and paper trade** before enabling live trading
5. **Never share your broker credentials** - keep `.env` secure
6. **Monitor the system continuously** - automation doesn't eliminate risk
7. **Market conditions change unexpectedly** - always have a stop-loss
8. **Understand derivatives trading** - options are complex and risky

**By using this system, you acknowledge all risks and take full responsibility for your trading decisions.**

---

## System Requirements

- **OS**: Linux, macOS, or Windows 11 with WSL2
- **CPU**: 4+ cores recommended
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 50GB+ for historical data
- **Python**: 3.11+
- **Docker**: 24.0+ (for containerized deployment)
- **PostgreSQL**: 15+ (or use Docker)
- **Redis**: 7+ (or use Docker)

---

## Pre-Installation

### 1. System Dependencies

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3.11-venv \
    python3-pip \
    build-essential \
    libpq-dev \
    git \
    curl \
    postgresql-client \
    redis-tools
```

#### macOS
```bash
brew install python@3.11 postgresql redis git curl
```

#### Windows (WSL2)
```bash
# Install Windows Subsystem for Linux 2
wsl --install -d Ubuntu-22.04

# Then run Ubuntu/Debian commands above
```

### 2. Verify Installations
```bash
python3 --version          # Should be 3.11+
pip --version              # Should be 23+
docker --version           # Should be 24+
docker-compose --version   # Should be 2.0+
```

---

## Installation

### Option A: Docker Compose (Recommended for Production)

#### 1. Clone Repository
```bash
git clone <repo-url> ai-options-trader
cd ai-options-trader
```

#### 2. Copy and Configure Environment
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```bash
nano .env
```

Key settings to review:
- `PAPER_TRADING=true` (MUST be true initially)
- `LIVE_TRADING_ENABLED=false` (MUST be false initially)
- `DB_PASSWORD=` (Change to strong password)
- `REDIS_PASSWORD=` (Leave empty or set password)

#### 3. Start Services
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Check status
docker-compose ps
```

#### 4. Verify Installation
```bash
# Test API
curl http://localhost:8000/health

# Access documentation
# Open browser: http://localhost:8000/api/docs

# View Grafana
# Open browser: http://localhost:3001
# Login: admin / admin
```

#### 5. Initialize Database
```bash
# Run database migrations (when available)
docker-compose exec backend python scripts/init_db.py
```

---

### Option B: Local Development Setup

#### 1. Clone Repository
```bash
git clone <repo-url> ai-options-trader
cd ai-options-trader
```

#### 2. Create Python Virtual Environment
```bash
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate     # Windows
```

#### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Install and Start PostgreSQL
```bash
# macOS with Homebrew
brew services start postgresql

# Linux - PostgreSQL should auto-start
# OR manually start if needed
sudo systemctl start postgresql

# Verify running
psql --version
```

#### 5. Create Database
```bash
# Connect to PostgreSQL
psql -U postgres

# In PostgreSQL shell:
CREATE USER trader WITH PASSWORD 'change_me_in_production';
CREATE DATABASE options_trading OWNER trader;
ALTER ROLE trader SET client_encoding TO 'utf8';
ALTER ROLE trader SET default_transaction_isolation TO 'read committed';
ALTER ROLE trader SET default_transaction_deferrable TO on;
ALTER ROLE trader SET default_tzoneTO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE options_trading TO trader;
\q
```

#### 6. Install and Start Redis
```bash
# macOS
brew services start redis

# Linux
sudo systemctl start redis-server

# Verify running
redis-cli ping
# Should return: PONG
```

#### 7. Create `.env` File
```bash
cp .env.example .env
nano .env
```

#### 8. Run Application
```bash
# From project root with venv activated
cd backend
python main.py

# Or with Uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### 9. Access Application
- API Docs: http://localhost:8000/api/docs
- Health: http://localhost:8000/health
- Dashboard: http://localhost:3000 (if frontend setup)

---

## Configuration

### Environment Variables

All configuration is via `.env` file. Key sections:

#### Safety
```env
PAPER_TRADING=true              # Always start true
LIVE_TRADING_ENABLED=false      # Always start false
ENVIRONMENT=development         # development or production
```

#### Database
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=options_trading
DB_USER=trader
DB_PASSWORD=<strong-password>
```

#### Market Data
```env
MARKET_DATA_PROVIDER=simulator   # Use simulator for testing
MARKET_TIMEZONE=Asia/Kolkata
```

#### Trading Limits
```env
MAX_ACCOUNT_RISK_PER_TRADE=0.01  # 1% per trade
MAX_DAILY_LOSS_PERCENT=0.02      # 2% daily max loss
MAX_CONSECUTIVE_LOSSES=3         # Pause after 3 losses
MAX_TRADES_PER_DAY=10            # Max 10 trades/day
```

See `.env.example` for complete configuration options.

### Strategy Configuration

Strategies are enabled/disabled via `.env`:
```env
STRATEGY_VWAP_TREND_ENABLED=true
STRATEGY_OPENING_BREAKOUT_ENABLED=true
STRATEGY_SUPPORT_RESISTANCE_ENABLED=true
# ... etc
```

Adjust strategy weights for ensemble:
```env
STRATEGY_VWAP_WEIGHT=0.20
STRATEGY_OPENING_BREAKOUT_WEIGHT=0.15
# ... etc
```

---

## Broker Configuration

### Setting Up Zerodha (Example)

1. **Create Zerodha Account**
   - Visit https://kite.zerodha.com
   - Sign up and complete KYC

2. **Get API Credentials**
   - Log in to Zerodha Console
   - Go to Settings → API Consents
   - Generate API key
   - Note: API Key, Secret Key, User ID

3. **Configure Environment**
   ```env
   BROKER_NAME=zerodha
   ZERODHA_API_KEY=<your-api-key>
   ZERODHA_API_SECRET=<your-api-secret>
   ZERODHA_USER_ID=<your-user-id>
   ```

### Switching Data Providers

```env
MARKET_DATA_PROVIDER=zerodha      # For Zerodha WebSocket
MARKET_DATA_PROVIDER=simulator    # For testing/simulation
```

---

## First Run Checklist

- [ ] Read all safety warnings
- [ ] Set `PAPER_TRADING=true`
- [ ] Set `LIVE_TRADING_ENABLED=false`
- [ ] Database initialized and accessible
- [ ] Redis running and accessible
- [ ] Backend starts without errors
- [ ] API health check passes: `curl http://localhost:8000/health`
- [ ] Market data provider connected
- [ ] Dashboard loads at http://localhost:3000
- [ ] Papertrading mode confirmed

---

## Testing the Setup

### 1. API Health Check
```bash
curl http://localhost:8000/health
# Expected response:
# {
#   "status": "ok",
#   "timestamp": "...",
#   "paper_trading": true,
#   "live_trading_enabled": false
# }
```

### 2. Get Market Data
```bash
curl http://localhost:8000/api/market/index/NIFTY
```

### 3. Get Option Chain
```bash
curl "http://localhost:8000/api/market/option-chain/NIFTY?expiry_date=2024-03-28"
```

### 4. Check Trading Status
```bash
curl http://localhost:8000/api/trading/status
```

### 5. Access Documentation
Open browser: http://localhost:8000/api/docs

---

## Monitoring

### Logs

```bash
# With Docker
docker-compose logs -f backend

# Locally
tail -f logs/application.log

# Search for errors
grep ERROR logs/application.log

# Search for trades
grep SIGNAL logs/application.log
```

### Prometheus Metrics
- URL: http://localhost:9090
- Useful queries:
  ```
  # API response time
  histogram_quantile(0.95, http_request_duration_seconds)
  
  # Database connection pool
  db_connections_active
  
  # Market data latency
  market_data_latency_ms
  ```

### Grafana Dashboards
- URL: http://localhost:3001
- Default login: admin / admin
- Pre-built dashboards for trading metrics

---

## Database Management

### Backup Database
```bash
# With Docker
docker-compose exec postgres pg_dump -U trader options_trading > backup.sql

# Locally
pg_dump -U trader -h localhost options_trading > backup.sql
```

### Restore Database
```bash
# With Docker
docker-compose exec -T postgres psql -U trader options_trading < backup.sql

# Locally
psql -U trader -h localhost options_trading < backup.sql
```

### Connect to Database
```bash
# With Docker
docker-compose exec postgres psql -U trader -d options_trading

# Locally
psql -U trader -h localhost -d options_trading
```

---

## Troubleshooting

### Database Connection Error
```
Error: could not translate host name "postgres" to address
```
**Solution**: Ensure PostgreSQL is running and accessible.
- Docker: `docker-compose exec postgres psql -U trader -l`
- Local: `psql -U trader -h localhost -l`

### Redis Connection Error
```
Error: Connection refused [Errno 111]
```
**Solution**: Start Redis.
- Docker: Already running in compose
- Local: `redis-server` or `brew services start redis`

### Market Data Provider Error
```
Error: Failed to connect to market data provider
```
**Solution**:
- Check `MARKET_DATA_PROVIDER` setting
- For simulator: Should work without additional config
- For Zerodha: Verify API credentials in `.env`

### Port Already in Use
```
Address already in use
```
**Solution**: Kill process on port or use different port.
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or change port in .env
API_PORT=8001
```

### Permission Denied Errors
```bash
# Fix file permissions
chmod +x scripts/*.py
sudo chown -R $USER:$USER .
```

### Memory Issues
```bash
# Increase Docker memory allocation
# Docker Desktop → Settings → Resources → Memory: 8GB+
```

---

## Production Deployment

### Pre-Production Checklist

- [ ] Paper trading tested extensively (minimum 100 trades)
- [ ] Backtesting shows consistent profitability
- [ ] All risk limits are conservative
- [ ] Emergency stop procedures tested
- [ ] Broker credentials secured in secrets manager
- [ ] Database backups automated
- [ ] Monitoring and alerts configured
- [ ] 24/7 support plan in place
- [ ] Legal/compliance review done
- [ ] Capital preservation tested

### Production Configuration

1. **Set Environment**
   ```env
   ENVIRONMENT=production
   DEBUG=false
   LOG_LEVEL=INFO
   ```

2. **Enable Circuit Breakers**
   ```env
   CIRCUIT_BREAKER_ENABLED=true
   EMERGENCY_STOP_ENABLED=true
   ```

3. **Set Conservative Limits**
   ```env
   MAX_ACCOUNT_RISK_PER_TRADE=0.005  # 0.5% per trade
   MAX_DAILY_LOSS_PERCENT=0.01       # 1% daily max
   ```

4. **Enable Monitoring**
   ```env
   PROMETHEUS_ENABLED=true
   GRAFANA_ENABLED=true
   ```

5. **Backup Configuration**
   ```env
   BACKUP_ENABLED=true
   DATA_RETENTION_DAYS=365
   ```

---

## Support & Resources

### Documentation
- API Docs: http://localhost:8000/api/docs
- README: [README.md](./README.md)
- Architecture: [ARCHITECTURE.md](./ARCHITECTURE.md)

### Getting Help
- Check logs: `docker-compose logs -f backend`
- Test connection: `curl http://localhost:8000/health`
- Review error codes: See application logs
- GitHub Issues: Report bugs and request features

### Broker Support
- Zerodha: https://support.zerodha.com
- API Status: Check https://api.kite.trade

---

## Next Steps

1. **Complete Setup**: Follow installation steps above
2. **Paper Trading**: Run in paper trading mode for 1+ week
3. **Study Code**: Review signal generation logic
4. **Backtest**: Test strategies on historical data
5. **Live Trading**: Enable only after thorough testing

---

**Last Updated**: 2026-09-02  
**Version**: 0.1.0-alpha
