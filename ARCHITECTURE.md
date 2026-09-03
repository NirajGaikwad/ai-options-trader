# Architecture - AI Options Trading Platform

## System Overview

High-level architecture for the AI Options Trading Platform:

```
┌─────────────────────────────────────────────────────────────────┐
│                     FRONTEND (React Dashboard)                   │
│              Charts, P&L, Signals, Portfolio Views              │
└──────────────────────────┬──────────────────────────────────────┘
                           │ WebSocket / REST
┌──────────────────────────┴──────────────────────────────────────┐
│                      FASTAPI BACKEND (Port 8000)                 │
├──────────────────────────────────────────────────────────────────┤
│  API Layer                                                        │
│  • Market Data Endpoints          • Trading Endpoints            │
│  • Option Chain Endpoints         • Portfolio Endpoints          │
│  • Health & Status Endpoints      • WebSocket Manager            │
├──────────────────────────────────────────────────────────────────┤
│  Core Trading Engine                                             │
│  • Signal Generation Engine       • Risk Management Engine       │
│  • Technical Analysis Engine      • Position Management          │
│  • Option Chain Analytics         • Order Execution Engine       │
│  • Price Action Engine            • Portfolio Tracker            │
│  • Market Regime Detection        • Trade Journal               │
├──────────────────────────────────────────────────────────────────┤
│  Market Data Layer                                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Market Data Provider Interface (Abstract Base)          │   │
│  └──────────────┬──────────────────────────────────────────┘   │
│                 │                                                 │
│     ┌───────────┼────────────────────────┐                      │
│     │           │                        │                      │
│  ┌──▼───┐  ┌───▼──────┐  ┌──────────┐   │                     │
│  │Zerodha   Broker     CSV       Simulator                      │
│  │Provider  API        Data       (Testing)                     │
│  └────────────────────────────────────────┘                     │
├──────────────────────────────────────────────────────────────────┤
│  Data & Services Layer                                           │
│  • Database (PostgreSQL + TimescaleDB)                          │
│  • Cache (Redis)                                                │
│  • Task Queue (Celery)                                          │
│  • News Intelligence                                            │
│  • ML Models                                                    │
└────────────────┬─────────────────────────────────────────────────┘
                 │
┌────────────────┴─────────────────────────────────────────────────┐
│              INFRASTRUCTURE & MONITORING                          │
├──────────────────────────────────────────────────────────────────┤
│  • Prometheus (Metrics)  • Grafana (Dashboards)                 │
│  • Structured Logging    • Error Tracking                       │
│  • Docker Compose        • Health Checks                        │
│  • Backup & Restore      • Alert Management                     │
└──────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. API Layer

**FastAPI Application** (`backend/main.py`)

Responsibilities:
- HTTP REST endpoints for all operations
- WebSocket connections for real-time data
- Request validation and error handling
- CORS and security middleware
- Health checks and status endpoints

Key Endpoints:
```
GET  /health
GET  /api/market/index/{instrument}
GET  /api/market/option-chain/{instrument}
GET  /api/market/candles/{instrument}
GET  /api/trading/status
POST /api/trading/emergency-stop
WS   /ws/market-data
```

---

### 2. Market Data Layer

**Provider Architecture** (`backend/market_data/`)

Abstract base class defines interface:
```python
class BaseMarketDataProvider(ABC):
    async def connect() -> bool
    async def get_index_snapshot() -> IndexSnapshot
    async def get_option_chain() -> List[OptionChainData]
    async def get_candle() -> List[CandleData]
    async def subscribe_index()
    async def subscribe_option_chain()
```

Implementations:

| Provider | Purpose | Status |
|----------|---------|--------|
| SimulatorProvider | Testing & demo | ✅ Built |
| ZerodhaProvider | Live data | 📋 Planned |
| BrokerAPIProvider | Generic broker | 📋 Planned |
| CSVDataProvider | Backtesting | 📋 Planned |

**Data Freshness Validation**:
- Timestamp checks against stale threshold
- Automatic NO_TRADE decision if data is stale
- Connection status monitoring
- Latency tracking

---

### 3. Database Layer

**PostgreSQL + TimescaleDB** (`backend/db/models.py`)

Time-series optimized schema:

```python
# Core Tables
MarketSnapshot          # Real-time index data (hypertable)
Candle                  # OHLCV data (hypertable)
OptionChainSnapshot     # Option chain data (hypertable)

# Trading Tables
Signal                  # AI signals with reasoning
Trade                   # Executed trades with P&L
Order                   # Individual orders
DailyPortfolio          # Daily equity curve

# Analytics Tables
BacktestResult          # Backtest results
MLModel                 # Trained ML models
SystemMetric            # Performance metrics (hypertable)

# News & Events
NewsItem                # News articles
EconomicEvent           # Calendar events

# Audit
AuditLog                # Complete action history
ErrorLog                # Error tracking
```

**TimescaleDB Features**:
- Automatic data compression
- Efficient time-range queries
- Hierarchical aggregation
- Continuous aggregates for fast dashboards

---

### 4. Technical Analysis Engine

**Indicators** (`backend/indicators/`)

Core indicators:

| Category | Indicators |
|----------|-----------|
| Trend | EMA 9/20/50/100/200, SMA, Supertrend |
| Momentum | RSI, MACD, Stochastic, ROC |
| Volatility | ATR, Bollinger Bands, India VIX |
| Volume | Volume, Relative Volume, OBV, VWAP |
| Structure | Support/Resistance, Market Structure |

Multi-timeframe analysis:
- 1-minute (scalping confirmations)
- 3-minute (entry timing)
- 5-minute (primary analysis)
- 15-minute (trend confirmation)
- 30-minute (support/resistance)
- 1-hour (market context)
- Daily (macro view)

---

### 5. Signal Generation Engine

**Multi-Strategy Ensemble** (`backend/strategies/`)

Flow:
```
Market Data
    ↓
Strategy 1 → Score (0-100)
Strategy 2 → Score (0-100)
Strategy 3 → Score (0-100)
Strategy 4 → Score (0-100)
    ↓
Ensemble Aggregation
    ↓
False Signal Filter
    ↓
Risk/Reward Check
    ↓
Liquidity Check
    ↓
Trade Decision (BUY_CE, BUY_PE, HOLD, NO_TRADE)
    ↓
Risk Management Engine
    ↓
Execution Engine
```

Strategies:
1. **VWAP Trend**: Price action around VWAP
2. **Opening Range**: First hour breakout patterns
3. **Support/Resistance**: Reversal at key levels
4. **Breakout Retest**: Entry after retest
5. **Momentum**: Strong directional moves
6. **Option Chain**: OI and IV analysis
7. **Multi-Timeframe**: Confluence across frames

---

### 6. Risk Management Engine

**Position Sizing & Risk Controls** (`backend/risk/`)

Position Sizing:
```
Position Size = Risk Amount / (Entry - Stop Loss)
Risk Amount = Account Capital × Max Risk %
```

Daily Limits:
```
Daily Loss Limit = Capital × Max Daily Loss %
Daily Profit Limit = Capital × Max Daily Profit %
Max Consecutive Losses = N trades
Max Trades/Day = N
Max Open Positions = N
```

Entry Validation:
- Risk/reward ratio check
- Liquidity score check
- Spread validation
- OI check
- Confidence threshold

---

### 7. Option Chain Analytics

**OI & Greeks Analysis** (`backend/option_chain/`)

Calculations:
```
Highest Call OI (resistance level)
Highest Put OI (support level)
Put-Call Ratio (bullish/bearish indicator)
OI Buildup (fresh positions)
Short Covering (reduction in shorts)
IV Skew (volatility pattern)
Max Pain (theoretical level)
```

Integration with price action:
- Combine OI with volume
- Integrate with technical levels
- Track OI changes for momentum
- Detect possible exhaustion

---

### 8. Execution Engine

**Order Placement & Management** (`backend/execution/`)

Pre-Execution Checks:
```python
✓ Signal validation
✓ Market status check
✓ Capital available check
✓ Risk limits check
✓ Liquidity check
✓ Data freshness check
✓ Duplicate order prevention
```

Order Management:
- Place order
- Monitor status
- Handle partial fills
- Track slippage
- Record execution
- Update position
- Start monitoring

---

### 9. Portfolio Management

**P&L Tracking & Reporting** (`backend/portfolio/`)

Real-time Tracking:
- Capital & available margin
- Open positions with MTM
- Unrealized P&L
- Realized P&L
- Greeks exposure
- Drawdown metrics

Daily Reports:
- Win rate
- Profit factor
- Consecutive wins/losses
- Average holding time
- Sharpe ratio
- Max drawdown

---

### 10. Backtesting Engine

**Historical Simulation** (`backend/backtesting/`)

Features:
```
Walk-forward validation
Transaction costs (STT, brokerage, GST)
Slippage simulation
Position sizing
Risk management
Equity curve
Drawdown analysis
```

Output Metrics:
- Total return, CAGR, Sharpe
- Win rate, profit factor
- Max drawdown, recovery
- Average holding time
- Winning vs losing trades

---

### 11. Machine Learning

**Prediction Models** (`backend/ml/`)

Models:
- XGBoost (primary)
- LightGBM (fast)
- Random Forest (interpretability)

Features:
- Technical indicators
- Option chain metrics
- Volume analysis
- Market regime
- News sentiment
- Time-of-day features

Output:
- Probability of up move
- Probability of down move
- Expected return
- Volatility forecast

Important: ML predictions are combined with technical analysis, not used standalone.

---

### 12. News & Sentiment

**Intelligence System** (`backend/news/`)

Data Sources:
- Reuters, Bloomberg, CNBC
- Economic calendar
- Corporate announcements
- Government releases

Sentiment Analysis:
```
VERY_BULLISH    (+100 to +60)
BULLISH         (+60 to +20)
NEUTRAL         (-20 to +20)
BEARISH         (-60 to -20)
VERY_BEARISH    (-100 to -60)
```

Event Handling:
- Pre-event blackout period
- Post-event monitoring
- Impact assessment
- VIX monitoring

---

### 13. Market Regime Detection

**Classification Engine** (`backend/market_regime/`)

Regimes:
```
STRONG_BULLISH_TREND      → Prefer CE
WEAK_BULLISH_TREND        → Conservative CE
STRONG_BEARISH_TREND      → Prefer PE
WEAK_BEARISH_TREND        → Conservative PE
SIDEWAYS                  → Avoid directional
HIGH_VOLATILITY           → Reduce size
LOW_VOLATILITY            → Look for breakout
BREAKOUT                  → Entry opportunity
BREAKDOWN                 → Caution
UNCERTAIN                 → NO TRADE
```

Calculation:
- ADX (trend strength)
- ATR (volatility)
- VWAP alignment
- EMA structure
- RSI levels
- Volume analysis
- Option chain metrics

---

## Data Flow

### Real-Time Trading Flow
```
Market Data Provider
    ↓
Data Validation (Freshness, Completeness)
    ↓
Technical Analysis (All Timeframes)
    ↓
Signal Generation (Multiple Strategies)
    ↓
Risk Assessment
    ↓
False Signal Filter
    ↓
Risk Management
    ↓
Order Execution
    ↓
Position Monitoring
    ↓
Trade Journal (Database)
    ↓
Portfolio Update
    ↓
Alert Generation
    ↓
Dashboard Update
```

### Backtesting Flow
```
Historical Data
    ↓
Replay Market Events
    ↓
Generate Signals
    ↓
Execute Orders (Simulated)
    ↓
Track P&L
    ↓
Generate Report
    ↓
Performance Analysis
```

---

## Configuration

**Settings Hierarchy**:
1. `.env` file (environment variables)
2. Pydantic BaseSettings (validation)
3. Default values in settings.py
4. Runtime overrides

**Configuration Categories**:
```
APPLICATION       (debug, environment)
DATABASE          (PostgreSQL connection)
REDIS             (caching)
MARKET_DATA       (provider, symbols)
TRADING_CONFIG    (risk limits)
STRATEGIES        (weights, thresholds)
INDICATORS        (periods, parameters)
BROKER_CONFIG     (API credentials)
MONITORING        (logging, alerts)
SECURITY          (JWT, encryption)
```

---

## Safety Features

### 1. Circuit Breaker
```python
If errors_in_window > threshold:
    → System enters CIRCUIT_OPEN state
    → New trades rejected
    → Existing positions monitored
    → Manual intervention required
```

### 2. Emergency Stop
```python
GET /api/trading/emergency-stop
→ Cancel all pending orders
→ Stop new trade generation
→ Monitor existing positions
→ Log all decisions
→ Alert user
```

### 3. Data Validation
```python
If data_stale > threshold:
    → Reject signal
    → Log warning
    → Continue monitoring
If data_missing:
    → NO_TRADE
    → Alert user
If broker_disconnected:
    → NO_TRADE
    → Attempt reconnect
```

### 4. Daily Limits
```python
If daily_loss >= threshold:
    → Trading halted
    → Positions held
    → Email/SMS alert
```

---

## Scalability Considerations

### Horizontal Scaling
- Stateless API tier (multiple backend instances)
- Database connection pooling
- Redis for distributed caching
- Task queue (Celery) for async processing

### Vertical Scaling
- TimescaleDB compression for data
- Materialized views for dashboards
- Caching of expensive calculations
- Efficient indexing on time-series

### Performance Optimization
- Candle data batching
- Option chain pre-processing
- Signal caching
- Query optimization
- Connection pooling

---

## Deployment Targets

### Development
- Docker Compose locally
- Single-server deployment
- SQLite for testing
- Simulator data provider

### Staging
- Kubernetes with Docker
- PostgreSQL database
- Redis clustering
- Limited broker credentials
- Mock trading

### Production
- Kubernetes multi-node
- PostgreSQL replication
- Redis Sentinel
- Real broker credentials
- Comprehensive monitoring
- Automated backups

---

## API Design Patterns

### REST Endpoints
```
GET     /api/resource              # List/read
GET     /api/resource/{id}         # Get one
POST    /api/resource              # Create
PUT     /api/resource/{id}         # Update
DELETE  /api/resource/{id}         # Delete
POST    /api/resource/action       # Custom action
```

### WebSocket Messages
```
{
  "type": "market_data" | "signal" | "trade" | "error",
  "timestamp": "ISO8601",
  "data": {...}
}
```

### Error Responses
```json
{
  "error": "error_code",
  "message": "Human readable message",
  "details": {...},
  "timestamp": "ISO8601"
}
```

---

## Testing Strategy

### Unit Tests
- Individual indicator calculations
- Risk calculations
- Position sizing
- Data validation

### Integration Tests
- Full signal → trade flow
- Database operations
- Cache operations
- API endpoints

### Backtesting
- Strategy performance
- Risk metrics
- Walk-forward validation

### Paper Trading
- 100+ trades minimum
- Real-time monitoring
- Risk limit validation

---

## Monitoring & Alerts

**Key Metrics**:
- API response time
- Data feed latency
- Database query performance
- Memory/CPU usage
- Error rates
- Trade metrics (win rate, max drawdown)

**Alert Triggers**:
- Data feed disconnected
- Broker connection lost
- Daily loss limit hit
- Emergency stop triggered
- System error rate high
- Database slow
- Memory usage high

**Dashboards**:
- Real-time trading
- Portfolio P&L
- System health
- Data quality
- Risk metrics
- Performance analysis

---

## Next Phases

| Phase | Component | Status |
|-------|-----------|--------|
| 1 | Market Data + API | ✅ In Progress |
| 2 | Technical Indicators | 📋 Planned |
| 3 | Option Chain Analytics | 📋 Planned |
| 4 | Signal Engine | 📋 Planned |
| 5 | Backtesting | 📋 Planned |
| 6 | Paper Trading | 📋 Planned |
| 7 | News Intelligence | 📋 Planned |
| 8 | ML Models | 📋 Planned |
| 9 | Risk Management | 📋 Planned |
| 10 | Broker Integration | 📋 Planned |
| 11 | Live Trading | 📋 Planned |

---

## Key Design Principles

1. **Never Trust Single Data Source**: Validate from multiple sources
2. **Fail Safe**: Default to NO_TRADE if any system fails
3. **Explainability**: Every decision must be traceable
4. **Risk First**: Risk management before profit optimization
5. **Automation-Aware**: Always allow manual override
6. **Event-Driven**: React to data changes, don't poll
7. **Immutable Audit Trail**: Complete record of all actions
8. **Configurable Everything**: Never hard-code trading parameters
9. **Paper First**: Always test with simulated capital
10. **Continuous Monitoring**: Watch the watchdog

---

**Last Updated**: 2026-09-02  
**Version**: 0.1.0-alpha
