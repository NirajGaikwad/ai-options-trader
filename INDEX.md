# Documentation Index - AI Options Trading Platform

Navigate the complete documentation for the platform.

---

## 📚 Quick Navigation

### For Getting Started
1. **[README.md](./README.md)** ← Start here
   - Project overview
   - Key features
   - Safety warnings
   - Quick links

2. **[QUICKSTART.md](./QUICKSTART.md)** ← Get running in 5 minutes
   - Docker setup
   - Local setup
   - API testing
   - Troubleshooting

3. **[SETUP.md](./SETUP.md)** ← Detailed installation guide
   - Prerequisites
   - Installation steps
   - Configuration
   - Database setup
   - First run checklist

### For Understanding the System
4. **[ARCHITECTURE.md](./ARCHITECTURE.md)** ← System design
   - High-level overview
   - Component architecture
   - Data flow
   - Design patterns
   - Scalability
   - Deployment targets

5. **[PHASE_1_SUMMARY.md](./PHASE_1_SUMMARY.md)** ← What's been built
   - Phase 1 completion status
   - Implemented features
   - Technology stack
   - File structure
   - Next actions

6. **[INDEX.md](./INDEX.md)** ← This file
   - Documentation roadmap
   - Search guide

---

## 📖 Documentation Structure

### Getting Started
```
README.md              ← Project overview & quick links
    ↓
QUICKSTART.md         ← 5-minute setup
    ↓
SETUP.md              ← Detailed guide (choose Option A or B)
    ↓
Run: http://localhost:8000/api/docs
```

### Understanding the System
```
ARCHITECTURE.md       ← How everything fits together
    ↓
Source Code           ← Implementation details
    ↓
API Documentation    ← Interactive at /api/docs
```

### Managing & Troubleshooting
```
SETUP.md → Troubleshooting section
    ↓
Logs: docker-compose logs -f backend
    ↓
Health: curl http://localhost:8000/health
```

---

## 📁 File Organization

### Root Level
```
README.md                 Project overview & safety warnings
SETUP.md                 Complete installation guide (50+ pages)
QUICKSTART.md            Fast setup in 5 minutes
ARCHITECTURE.md          System design & components
PHASE_1_SUMMARY.md       What's been built in Phase 1
INDEX.md                 This file
.env.example             Configuration template (150+ options)
requirements.txt         Python dependencies
docker-compose.yml      Service orchestration
```

### Backend Code (`backend/`)
```
main.py                 FastAPI application entry point
config/
  settings.py          Configuration management (Pydantic)
market_data/
  base.py              Market data provider interface
  simulator.py         Test data provider
db/
  models.py            Database schema (20 tables)
```

### Infrastructure (`docker/`)
```
Dockerfile             Application container image
prometheus.yml         Metrics configuration
```

### Scripts (`scripts/`)
```
init_db.py            Database initialization
backtest.py           Placeholder for backtesting
data_sync.py          Placeholder for data sync
```

---

## 🔍 How to Find Things

### "I want to..."

#### Get Started
→ Read [QUICKSTART.md](./QUICKSTART.md)

#### Understand the Architecture
→ Read [ARCHITECTURE.md](./ARCHITECTURE.md)

#### Set Up Locally
→ Read [SETUP.md](./SETUP.md) → Option B (Local Setup)

#### Set Up with Docker
→ Read [SETUP.md](./SETUP.md) → Option A (Docker Compose) OR [QUICKSTART.md](./QUICKSTART.md)

#### Configure the System
→ Edit `.env` file (template: `.env.example`)
→ Reference: [SETUP.md](./SETUP.md) → Configuration section

#### Add a New Feature
→ Study [ARCHITECTURE.md](./ARCHITECTURE.md)
→ Review `backend/` code structure
→ Check similar component for patterns

#### Debug an Issue
→ Check [SETUP.md](./SETUP.md) → Troubleshooting
→ View logs: `docker-compose logs -f backend`
→ Test health: `curl http://localhost:8000/health`

#### Access API Documentation
→ Run system
→ Open: http://localhost:8000/api/docs
→ Click "Try it out" on any endpoint

#### Monitor the System
→ Prometheus: http://localhost:9090
→ Grafana: http://localhost:3001
→ Logs: `docker-compose logs -f`

#### Deploy to Production
→ Read [SETUP.md](./SETUP.md) → Production Deployment section
→ Read [ARCHITECTURE.md](./ARCHITECTURE.md) → Production targets

#### Live Trading Setup (After Phase 11)
→ Read README.md → Safety Features
→ Complete all 11 phases
→ Paper trade 100+ trades
→ Backtest thoroughly
→ Pass all safety checks

---

## 🔐 Safety Documentation

### Critical Safety Topics

| Topic | Location |
|-------|----------|
| Safety Warnings | [README.md](./README.md) |
| Circuit Breakers | [ARCHITECTURE.md](./ARCHITECTURE.md) → Safety Features |
| Risk Management | [ARCHITECTURE.md](./ARCHITECTURE.md) → Risk Management Engine |
| Emergency Stop | [README.md](./README.md) → Safety Features |
| Configuration Defaults | `.env.example` |
| Safety Validation | [SETUP.md](./SETUP.md) → Safety Checklist |
| Live Trading Requirements | [README.md](./README.md) → Paper Trading Mode |

---

## 📊 Technical Documentation

### Database
- Schema: `backend/db/models.py`
- Tables: 20 tables across 6 categories
- Time-series: TimescaleDB hypertables
- Design: [ARCHITECTURE.md](./ARCHITECTURE.md) → Database Layer

### API
- Endpoints: 15+ REST + WebSocket
- Documentation: http://localhost:8000/api/docs
- Design: [ARCHITECTURE.md](./ARCHITECTURE.md) → API Design Patterns
- Implementation: `backend/main.py`

### Configuration
- Settings: `backend/config/settings.py`
- Template: `.env.example` (150+ options)
- Validation: Safety checks on startup
- Guide: [SETUP.md](./SETUP.md) → Configuration section

### Market Data
- Provider interface: `backend/market_data/base.py`
- Simulator: `backend/market_data/simulator.py`
- Design: [ARCHITECTURE.md](./ARCHITECTURE.md) → Market Data Layer

---

## 🚀 Development Phases

### Phase Roadmap
```
Phase 1 ✅  Market Data + Database + Dashboard API
Phase 2 📋  Technical Indicators & Charts
Phase 3 📋  Option Chain Analytics
Phase 4 📋  Signal Generation Engine
Phase 5 📋  Backtesting Engine
Phase 6 📋  Paper Trading Simulation
Phase 7 📋  News Intelligence + Sentiment
Phase 8 📋  Machine Learning Models
Phase 9 📋  Risk Management Engine (Advanced)
Phase 10 📋 Broker Integration
Phase 11 📋 Live Trading (After validation)
```

Status: See [PHASE_1_SUMMARY.md](./PHASE_1_SUMMARY.md)

---

## 🛠️ Common Commands

### Starting the System
```bash
# With Docker (recommended)
docker-compose up -d

# Without Docker (Linux/macOS)
python backend/main.py
```

### Testing
```bash
# Health check
curl http://localhost:8000/health

# Get NIFTY data
curl http://localhost:8000/api/market/index/NIFTY

# API docs
open http://localhost:8000/api/docs
```

### Debugging
```bash
# View logs
docker-compose logs -f backend

# Database connection
psql -U trader -h localhost -d options_trading

# Redis check
redis-cli ping
```

### Stopping
```bash
# Stop all services
docker-compose down

# Keep data
docker-compose stop
```

---

## 📝 Code Structure

### Main Application Flow
```
backend/main.py
├── FastAPI app initialization
├── Middleware configuration
├── Startup/shutdown lifecycle
├── API endpoints
│   ├── Market data endpoints
│   ├── Trading endpoints
│   └── Health endpoints
└── WebSocket manager
```

### Configuration Flow
```
.env file
    ↓
backend/config/settings.py
├── Pydantic BaseSettings
├── Environment variable loading
├── Validation
└── Default values
```

### Market Data Flow
```
Market Data Provider (Abstract)
├── connect()
├── get_index_snapshot()
├── get_option_chain()
├── get_candle()
└── subscribe_*()
    ↓
Simulator Provider (Implementation)
├── Realistic synthetic data
├── Random walk simulation
├── Black-Scholes option pricing
└── Greeks calculation
```

### Database Flow
```
SQLAlchemy ORM
    ↓
backend/db/models.py (20 tables)
├── Time-series (MarketSnapshot, Candle, OptionChainSnapshot)
├── Trading (Signal, Trade, Order)
├── Analytics (BacktestResult, MLModel)
└── Monitoring (SystemMetric, ErrorLog, AuditLog)
    ↓
PostgreSQL + TimescaleDB
├── Automatic compression
├── Efficient time-range queries
└── Hierarchical aggregation
```

---

## 🎓 Learning Path

### For Trading Platform Users
1. Read [README.md](./README.md) - Overview
2. Read [QUICKSTART.md](./QUICKSTART.md) - Get running
3. Use [SETUP.md](./SETUP.md) for reference
4. Access `/api/docs` for API testing
5. Monitor at Grafana (http://localhost:3001)

### For Software Engineers
1. Read [ARCHITECTURE.md](./ARCHITECTURE.md)
2. Review `backend/` code structure
3. Study `backend/main.py` for patterns
4. Review `backend/config/settings.py` for configuration
5. Check `backend/market_data/` for extensibility
6. Review `backend/db/models.py` for data design

### For DevOps/Infrastructure
1. Read `docker-compose.yml`
2. Review [SETUP.md](./SETUP.md) → Docker Compose section
3. Check `docker/Dockerfile`
4. Review monitoring stack
5. Plan deployment (see [ARCHITECTURE.md](./ARCHITECTURE.md) → Deployment)

### For System Designers
1. Read [ARCHITECTURE.md](./ARCHITECTURE.md)
2. Study component interactions
3. Review API design patterns
4. Study database schema
5. Plan for Phase 2+ extensions

---

## 🔗 External Resources

### Indian Market
- NSE: https://www.nseindia.com
- Zerodha: https://zerodha.com
- Kite API: https://kite.trade

### Technologies
- FastAPI: https://fastapi.tiangolo.com
- SQLAlchemy: https://sqlalchemy.org
- PostgreSQL: https://www.postgresql.org
- TimescaleDB: https://www.timescale.com
- Redis: https://redis.io

### Trading Concepts
- Options 101: Understanding calls and puts
- Greeks: Delta, gamma, theta, vega
- Technical Analysis: Indicators and patterns
- Risk Management: Position sizing and stops

---

## ❓ FAQ by Topic

### Installation
**Q: Which setup option should I use?**
A: Docker Compose (Option A) if you have Docker. Otherwise, Option B (Local).

**Q: How long does setup take?**
A: 5 minutes with Docker, 15 minutes locally.

**Q: Do I need real broker credentials to test?**
A: No. Use simulator mode for testing (default).

### Usage
**Q: How do I access the API?**
A: API docs at http://localhost:8000/api/docs (auto-generated Swagger UI)

**Q: Can I use this for live trading immediately?**
A: No. Must complete all phases and pass safety checks.

**Q: What data does the simulator provide?**
A: Realistic OHLCV candles, option chains, Greeks - all synthetic.

### Safety
**Q: What if something goes wrong?**
A: Emergency stop: `curl -X POST http://localhost:8000/api/trading/emergency-stop`

**Q: Is paper trading really the default?**
A: Yes. `PAPER_TRADING=true`, `LIVE_TRADING_ENABLED=false` always by default.

**Q: Can I accidentally lose real money?**
A: Not in Phase 1. Live trading is disabled and requires multiple explicit confirmations.

### Development
**Q: How do I add a new feature?**
A: Study ARCHITECTURE.md, find similar component, follow patterns.

**Q: Where are database queries?**
A: SQLAlchemy ORM models in `backend/db/models.py`.

**Q: How do I run tests?**
A: `pytest tests/` (test structure ready for Phase 2).

---

## 📞 Support

### Getting Help

| Issue | Solution |
|-------|----------|
| Installation problem | Read [SETUP.md](./SETUP.md) → Troubleshooting |
| API not responding | Run `curl http://localhost:8000/health` |
| Database error | Check PostgreSQL running: `psql -U postgres` |
| Docker issue | Run `docker-compose logs` |
| Code understanding | Read [ARCHITECTURE.md](./ARCHITECTURE.md) |
| Configuration | Edit `.env` and reference `.env.example` |

### Quick Links

| Resource | Link |
|----------|------|
| Main Project Docs | [README.md](./README.md) |
| API Documentation | http://localhost:8000/api/docs |
| System Architecture | [ARCHITECTURE.md](./ARCHITECTURE.md) |
| Setup Guide | [SETUP.md](./SETUP.md) |
| Quick Start | [QUICKSTART.md](./QUICKSTART.md) |
| Phase Status | [PHASE_1_SUMMARY.md](./PHASE_1_SUMMARY.md) |

---

## 📈 Roadmap

### Current Phase
- **Phase 1** ✅ Market Data + Database + API

### Upcoming
- **Phase 2** Technical Indicators
- **Phase 3** Option Chain Analytics
- **Phase 4** Signal Generation
- **Phase 5** Backtesting
- **Phase 6** Paper Trading Simulation
- **Phase 7** News Intelligence
- **Phase 8** Machine Learning
- **Phase 9** Advanced Risk Management
- **Phase 10** Broker Integration
- **Phase 11** Live Trading

See [PHASE_1_SUMMARY.md](./PHASE_1_SUMMARY.md) for details.

---

## ✅ Pre-Flight Checklist

Before using the platform:
- [ ] Read [README.md](./README.md) - Safety warnings
- [ ] Review [SETUP.md](./SETUP.md) or [QUICKSTART.md](./QUICKSTART.md)
- [ ] Run `docker-compose up -d` or local setup
- [ ] Verify health: `curl http://localhost:8000/health`
- [ ] Test API: Open http://localhost:8000/api/docs
- [ ] Check market data: Test NIFTY endpoint
- [ ] Confirm paper trading enabled
- [ ] Confirm live trading disabled
- [ ] Review configuration in `.env`

---

**Documentation Last Updated**: 2026-09-02  
**Total Pages**: 10+  
**Version**: 0.1.0-alpha  
**Status**: Complete for Phase 1 ✅
