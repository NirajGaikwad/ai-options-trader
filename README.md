# AI-Powered Intraday Options Trading Platform

Production-grade AI platform for intraday trading on Indian market options (NIFTY 50 & SENSEX).

## ⚠️ CRITICAL SAFETY NOTES

- **Paper Trading Mode**: Platform launches in `PAPER_TRADING=true` by default
- **Live Trading Disabled**: `LIVE_TRADING_ENABLED=false` by default
- **No Profit Guarantee**: This system maximizes risk-adjusted returns but never guarantees profits
- **Full Capital Risk**: Live trading can result in total capital loss
- **Requires Activation**: Live trading must be explicitly enabled via configuration after passing paper-trading validation

## Architecture Phases

- **Phase 1** (Current): Market Data + Database + Real-Time Dashboard
- **Phase 2**: Charts and Technical Indicators
- **Phase 3**: Option-Chain Analytics
- **Phase 4**: Signal Engine
- **Phase 5**: Backtesting Engine
- **Phase 6**: Paper Trading with Complete Simulation
- **Phase 7**: News Intelligence + Sentiment Analysis
- **Phase 8**: Machine Learning Models
- **Phase 9**: Risk Management Engine
- **Phase 10**: Broker Integration
- **Phase 11**: Live Trading (After Validation)

## Tech Stack

- **Backend**: Python 3.11+ with FastAPI
- **Database**: PostgreSQL + TimescaleDB
- **Cache**: Redis
- **Frontend**: React 18 with Next.js
- **Charts**: TradingView Lightweight Charts
- **ML**: scikit-learn, XGBoost, LightGBM
- **Monitoring**: Prometheus + Grafana
- **Containers**: Docker + Docker Compose
- **Task Scheduling**: APScheduler

## Quick Start

See [SETUP.md](./SETUP.md) for detailed installation and configuration.

```bash
# 1. Clone and setup
git clone <repo>
cd ai-options-trader

# 2. Copy configuration
cp .env.example .env

# 3. Start services
docker-compose up -d

# 4. Initialize database
python scripts/init_db.py

# 5. Access dashboard
# http://localhost:3000
```

## Project Structure

```
ai-options-trader/
├── backend/                    # Python FastAPI backend
│   ├── api/                   # REST API endpoints
│   ├── market_data/          # Market data engine
│   ├── indicators/           # Technical indicators
│   ├── option_chain/         # Option chain analytics
│   ├── strategies/           # Trading strategies
│   ├── signals/              # Signal generation
│   ├── news/                 # News intelligence
│   ├── ml/                   # Machine learning
│   ├── risk/                 # Risk management
│   ├── execution/            # Order execution
│   ├── brokers/              # Broker adapters
│   ├── portfolio/            # P&L tracking
│   ├── backtesting/          # Backtesting engine
│   ├── db/                   # Database models
│   ├── config/               # Configuration
│   ├── monitoring/           # Logging & monitoring
│   └── main.py              # Application entry
│
├── frontend/                  # React frontend
│   ├── pages/                # Next.js pages
│   ├── components/           # React components
│   ├── hooks/                # Custom hooks
│   ├── lib/                  # Utilities
│   └── styles/               # CSS/styling
│
├── database/                  # Database migrations
│   └── migrations/           # SQL migrations
│
├── tests/                     # Test suite
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── backtesting/          # Backtest tests
│
├── scripts/                   # Utility scripts
│   ├── init_db.py           # Database initialization
│   ├── backtest.py          # Backtesting runner
│   └── data_sync.py         # Data synchronization
│
├── config/                    # Configuration templates
│   ├── development.yaml      # Dev configuration
│   ├── production.yaml       # Prod configuration
│   └── strategies.yaml       # Strategy configuration
│
├── docker/                    # Docker files
│   ├── Dockerfile           # Application container
│   └── docker-compose.yml   # Service orchestration
│
├── .env.example              # Environment template
├── requirements.txt          # Python dependencies
└── SETUP.md                 # Detailed setup guide
```

## Core Principles

1. **Never Force a Trade**: System actively identifies situations to NOT trade
2. **Capital Preservation**: Maximum account risk per trade is configurable (default 0.5-1%)
3. **Multi-Factor Scoring**: All signals must pass technical, risk, and liquidity checks
4. **Risk-Adjusted Returns**: Optimization focuses on Sharpe/Sortino ratios, not trade count
5. **Event-Driven Architecture**: Real-time data triggers analysis without polling
6. **Explainability**: Every trade includes detailed reasoning and risk factors
7. **Comprehensive Testing**: All components tested before production use

## Configuration

All sensitive data uses environment variables:

```env
# Database
DB_HOST=postgres
DB_PORT=5432
DB_NAME=options_trading
DB_USER=trader
DB_PASSWORD=<secure-password>

# Trading
PAPER_TRADING=true
LIVE_TRADING_ENABLED=false
MAX_ACCOUNT_RISK_PER_TRADE=0.01  # 1%
MAX_DAILY_LOSS_PERCENT=0.02      # 2%

# Broker (when enabled)
BROKER_API_KEY=<key>
BROKER_API_SECRET=<secret>
BROKER_NAME=your-broker

# News & Sentiment
NEWS_API_KEY=<key>
NEWS_PROVIDERS=reuters,bloomberg,ft

# Market Data
MARKET_DATA_PROVIDER=zerodha  # configurable
NIFTY_SYMBOLS=NIFTY,BANKNIFTY
SENSEX_SYMBOLS=SENSEX,NIFTYJR
```

## Safety Features

- **Emergency Stop**: Global kill-switch for all trading
- **Circuit Breakers**: Automatic pause during abnormal conditions
- **Daily Limits**: Configurable max daily loss, max trades, max consecutive losses
- **Data Validation**: Rejects stale or invalid data
- **Broker Failure Handling**: Graceful degradation if broker unavailable
- **Position Reconciliation**: Continuous verification of order status

## Monitoring

- **Prometheus Metrics**: Real-time system metrics
- **Grafana Dashboards**: Visual monitoring
- **Structured Logs**: JSON logging for analysis
- **Event Audit Trail**: Complete record of all decisions and trades
- **Health Checks**: Broker, data feed, database connectivity status

## Important Notes

### Data Freshness

- All signals require fresh data (configurable stale threshold, default 10 seconds)
- Stale data automatically triggers NO_TRADE decision

### Timezone

- All timestamps in **Asia/Kolkata (IST)**
- Market hours: 09:15 - 15:30 IST (Monday-Friday)
- Honors exchange holidays from official calendar

### Transaction Costs

- All backtests include: brokerage, STT, GST, exchange charges, stamp duty, slippage
- Realistic cost modeling improves backtest accuracy

### Paper Trading

- Matches live trading behavior exactly
- Records all signals, orders, fills, P&L
- Required minimum sample size before live trading enabled

## Development Status

| Phase | Status | Completion |
|-------|--------|------------|
| Phase 1 | In Progress | 30% |
| Market Data | In Progress | 40% |
| Database | In Progress | 40% |
| Dashboard | In Progress | 20% |
| Phase 2+ | Planned | - |

## Support & Debugging

1. **Data Issues**: Check `docker logs backend` and `/logs/data.log`
2. **API Issues**: Check `docker logs api` for FastAPI errors
3. **Database**: `psql -h localhost -U trader -d options_trading`
4. **Redis**: `redis-cli`

## Roadmap

- [x] Project structure
- [x] Configuration management
- [x] Database schema
- [x] Market data adapters
- [x] Real-time WebSocket
- [ ] Technical indicators (Phase 2)
- [ ] Charts and visualization
- [ ] Option chain analytics (Phase 3)
- [ ] Signal engine (Phase 4)
- [ ] ML models (Phase 8)
- [ ] Full backtesting
- [ ] Live trading (Phase 11)

## Legal Disclaimer

This system is for educational and authorized trading purposes only. Users are responsible for:
- Compliance with local regulations
- Understanding derivatives risks
- Maintaining adequate capital reserves
- Monitoring all trading activity
- Complying with broker terms and conditions

This system does not guarantee profits and can result in substantial losses.

---

**Last Updated**: 2026-09-02  
**Maintainer**: AI Trading Platform Team
