"""
Database models for the AI Options Trading Platform.
Uses SQLAlchemy ORM with PostgreSQL + TimescaleDB.
"""

from datetime import datetime, timezone
from enum import Enum
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime,
    Text, Enum as SQLEnum, ForeignKey, Index, UniqueConstraint,
    Numeric, TIMESTAMP
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# ============================================================================
# ENUMS
# ============================================================================

class InstrumentType(str, Enum):
    NIFTY = "NIFTY"
    SENSEX = "SENSEX"
    BANKNIFTY = "BANKNIFTY"


class OptionType(str, Enum):
    CALL = "CE"
    PUT = "PE"


class SignalType(str, Enum):
    BUY_CE = "BUY_CE"
    BUY_PE = "BUY_PE"
    HOLD = "HOLD"
    NO_TRADE = "NO_TRADE"


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    OPEN = "OPEN"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class OrderType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class MarketRegime(str, Enum):
    STRONG_BULLISH_TREND = "STRONG_BULLISH_TREND"
    WEAK_BULLISH_TREND = "WEAK_BULLISH_TREND"
    STRONG_BEARISH_TREND = "STRONG_BEARISH_TREND"
    WEAK_BEARISH_TREND = "WEAK_BEARISH_TREND"
    SIDEWAYS = "SIDEWAYS"
    HIGH_VOLATILITY = "HIGH_VOLATILITY"
    LOW_VOLATILITY = "LOW_VOLATILITY"
    BREAKOUT = "BREAKOUT"
    BREAKDOWN = "BREAKDOWN"
    UNCERTAIN = "UNCERTAIN"


class TradeStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED_PROFIT = "CLOSED_PROFIT"
    CLOSED_LOSS = "CLOSED_LOSS"
    CLOSED_BREAKEVEN = "CLOSED_BREAKEVEN"
    CANCELLED = "CANCELLED"


class SentimentType(str, Enum):
    VERY_BULLISH = "VERY_BULLISH"
    BULLISH = "BULLISH"
    NEUTRAL = "NEUTRAL"
    BEARISH = "BEARISH"
    VERY_BEARISH = "VERY_BEARISH"


# ============================================================================
# MARKET DATA MODELS
# ============================================================================

class MarketSnapshot(Base):
    """
    Real-time market snapshot for indices.
    Uses TimescaleDB hypertable for time-series data.
    """
    __tablename__ = "market_snapshots"

    id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP, index=True, nullable=False)
    instrument = Column(SQLEnum(InstrumentType), nullable=False, index=True)

    # OHLCV
    open = Column(Numeric(10, 2), nullable=False)
    high = Column(Numeric(10, 2), nullable=False)
    low = Column(Numeric(10, 2), nullable=False)
    close = Column(Numeric(10, 2), nullable=False)
    volume = Column(Integer)

    # Additional Data
    ltp = Column(Numeric(10, 2), nullable=False)  # Last Traded Price
    previous_close = Column(Numeric(10, 2))
    vwap = Column(Numeric(10, 2))
    change_percent = Column(Float)
    bid = Column(Numeric(10, 2))
    ask = Column(Numeric(10, 2))

    # Data Quality
    is_stale = Column(Boolean, default=False)
    data_freshness_seconds = Column(Integer)  # Time since last update

    # Metadata
    data_provider = Column(String(50))
    data_source = Column(String(100))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index('idx_snapshot_time_instrument', 'timestamp', 'instrument'),
    )


class Candle(Base):
    """
    OHLCV candlestick data across multiple timeframes.
    Uses TimescaleDB hypertable for efficient time-series storage.
    """
    __tablename__ = "candles"

    id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP, index=True, nullable=False)
    instrument = Column(SQLEnum(InstrumentType), nullable=False, index=True)
    interval_minutes = Column(Integer, nullable=False, index=True)  # 1, 5, 15, 60, 1440

    # OHLCV
    open = Column(Numeric(10, 2), nullable=False)
    high = Column(Numeric(10, 2), nullable=False)
    low = Column(Numeric(10, 2), nullable=False)
    close = Column(Numeric(10, 2), nullable=False)
    volume = Column(Integer)

    # Additional Metrics
    vwap = Column(Numeric(10, 2))
    typical_price = Column(Numeric(10, 2))
    volume_weighted_close = Column(Numeric(10, 2))

    # Candle Pattern Detection
    pattern_type = Column(String(50))  # doji, hammer, etc.
    pattern_strength = Column(Float)

    # Data Quality
    is_closed = Column(Boolean, default=False)
    data_provider = Column(String(50))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index('idx_candle_time_instrument_interval', 'timestamp', 'instrument', 'interval_minutes'),
        UniqueConstraint('timestamp', 'instrument', 'interval_minutes', name='uq_candle_time_instrument_interval'),
    )


class OptionChainSnapshot(Base):
    """
    Real-time option chain data for a specific strike and expiry.
    Uses TimescaleDB hypertable.
    """
    __tablename__ = "option_chain_snapshots"

    id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP, index=True, nullable=False)
    instrument = Column(SQLEnum(InstrumentType), nullable=False, index=True)
    expiry_date = Column(DateTime, nullable=False, index=True)
    strike = Column(Numeric(10, 2), nullable=False, index=True)

    # CALL (CE) Data
    ce_ltp = Column(Numeric(10, 4))
    ce_bid = Column(Numeric(10, 4))
    ce_ask = Column(Numeric(10, 4))
    ce_bid_qty = Column(Integer)
    ce_ask_qty = Column(Integer)
    ce_volume = Column(Integer)
    ce_oi = Column(Integer)
    ce_oi_change = Column(Integer)
    ce_iv = Column(Float)
    ce_delta = Column(Float)
    ce_gamma = Column(Float)
    ce_theta = Column(Float)
    ce_vega = Column(Float)

    # PUT (PE) Data
    pe_ltp = Column(Numeric(10, 4))
    pe_bid = Column(Numeric(10, 4))
    pe_ask = Column(Numeric(10, 4))
    pe_bid_qty = Column(Integer)
    pe_ask_qty = Column(Integer)
    pe_volume = Column(Integer)
    pe_oi = Column(Integer)
    pe_oi_change = Column(Integer)
    pe_iv = Column(Float)
    pe_delta = Column(Float)
    pe_gamma = Column(Float)
    pe_theta = Column(Float)
    pe_vega = Column(Float)

    # Underlying Data
    underlying_price = Column(Numeric(10, 2))

    # Option Chain Metrics
    spread_points = Column(Numeric(10, 4))
    put_call_ratio = Column(Float)
    oi_ratio_call_put = Column(Float)
    moneyness = Column(String(20))  # ATM, ITM, OTM

    # Data Quality
    is_stale = Column(Boolean, default=False)
    data_freshness_seconds = Column(Integer)
    data_provider = Column(String(50))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index('idx_option_chain_time_instrument_expiry_strike',
              'timestamp', 'instrument', 'expiry_date', 'strike'),
    )


# ============================================================================
# TRADING MODELS
# ============================================================================

class Signal(Base):
    """
    AI-generated trading signal.
    Record of all signals with reasons, confidence, and performance tracking.
    """
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True)
    signal_timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    signal_type = Column(SQLEnum(SignalType), nullable=False)

    # Instrument Details
    instrument = Column(SQLEnum(InstrumentType), nullable=False)
    option_type = Column(SQLEnum(OptionType))  # CE or PE
    strike = Column(Numeric(10, 2))
    expiry_date = Column(DateTime)

    # Price Levels
    entry_price = Column(Numeric(10, 4), nullable=False)
    stop_loss = Column(Numeric(10, 4), nullable=False)
    target_1 = Column(Numeric(10, 4))
    target_2 = Column(Numeric(10, 4))
    target_3 = Column(Numeric(10, 4))
    trailing_stop = Column(Numeric(10, 4))

    # Signal Quality
    confidence_score = Column(Float)  # 0-100
    risk_reward_ratio = Column(Float)
    liquidity_score = Column(Float)  # 0-100
    technical_score = Column(Float)  # 0-100
    option_chain_score = Column(Float)  # 0-100

    # Market Context
    market_regime = Column(SQLEnum(MarketRegime))
    market_sentiment = Column(SQLEnum(SentimentType))
    india_vix = Column(Float)
    news_sentiment_score = Column(Integer)  # -100 to +100

    # Analysis Data
    rsi = Column(Float)
    macd = Column(Float)
    macd_signal = Column(Float)
    ema_9 = Column(Numeric(10, 2))
    ema_20 = Column(Numeric(10, 2))
    ema_50 = Column(Numeric(10, 2))
    atr = Column(Numeric(10, 4))
    adx = Column(Float)
    vwap = Column(Numeric(10, 2))

    # Option Chain Analysis
    oi_call = Column(Integer)
    oi_put = Column(Integer)
    oi_change_call = Column(Integer)
    oi_change_put = Column(Integer)
    iv_call = Column(Float)
    iv_put = Column(Float)

    # Decision Factors
    factors_passed = Column(Text)  # JSON list of factors that passed
    factors_failed = Column(Text)  # JSON list of factors that failed
    reasoning = Column(Text)  # AI explanation

    # Expected Holding
    expected_holding_minutes = Column(Integer)
    strategy_name = Column(String(100))

    # Signal Status
    was_traded = Column(Boolean, default=False)
    trade_id = Column(Integer, ForeignKey('trades.id'))

    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index('idx_signal_timestamp_instrument', 'signal_timestamp', 'instrument'),
    )


class Trade(Base):
    """
    Executed trade record - paper or live.
    Complete audit trail of entry, exit, P&L.
    """
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    trade_timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # Trade Details
    signal_id = Column(Integer, ForeignKey('signals.id'))
    instrument = Column(SQLEnum(InstrumentType), nullable=False)
    option_type = Column(SQLEnum(OptionType), nullable=False)
    strike = Column(Numeric(10, 2), nullable=False)
    expiry_date = Column(DateTime, nullable=False)

    # Execution
    entry_price = Column(Numeric(10, 4), nullable=False)
    entry_time = Column(DateTime)
    entry_quantity = Column(Integer, nullable=False)
    entry_order_id = Column(String(100))

    exit_price = Column(Numeric(10, 4))
    exit_time = Column(DateTime)
    exit_reason = Column(String(200))
    exit_order_id = Column(String(100))

    # Stops and Targets
    stop_loss = Column(Numeric(10, 4), nullable=False)
    target_1 = Column(Numeric(10, 4))
    target_2 = Column(Numeric(10, 4))
    target_hit = Column(String(20))  # "TARGET_1", "TARGET_2", "STOP_LOSS"

    # Costs
    entry_brokerage = Column(Numeric(10, 4))
    exit_brokerage = Column(Numeric(10, 4))
    total_brokerage = Column(Numeric(10, 4))
    stt = Column(Numeric(10, 4))  # Securities Transaction Tax
    gst = Column(Numeric(10, 4))
    other_charges = Column(Numeric(10, 4))
    total_charges = Column(Numeric(10, 4))

    # P&L Calculation
    gross_pnl = Column(Numeric(12, 4))  # Before costs
    net_pnl = Column(Numeric(12, 4))   # After costs
    pnl_percent = Column(Float)
    premium_paid = Column(Numeric(10, 4))
    max_profit = Column(Numeric(12, 4))
    max_loss = Column(Numeric(12, 4))
    realized_max_profit = Column(Numeric(12, 4))
    realized_max_loss = Column(Numeric(12, 4))

    # Risk Metrics
    initial_risk = Column(Numeric(10, 4))
    risk_reward = Column(Float)
    account_risk_percent = Column(Float)

    # Trade Status
    status = Column(SQLEnum(TradeStatus), default=TradeStatus.OPEN)
    holding_minutes = Column(Integer)
    is_paper_trade = Column(Boolean, default=True)

    # Analysis
    strategy_name = Column(String(100))
    market_regime_at_entry = Column(SQLEnum(MarketRegime))
    market_regime_at_exit = Column(SQLEnum(MarketRegime))

    # Metadata
    notes = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    signal = relationship("Signal", backref="trades")

    __table_args__ = (
        Index('idx_trade_timestamp_instrument', 'trade_timestamp', 'instrument'),
        Index('idx_trade_status', 'status'),
    )


class Order(Base):
    """
    Individual order record (can be multiple per trade).
    """
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    order_timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # Order Details
    trade_id = Column(Integer, ForeignKey('trades.id'))
    broker_order_id = Column(String(100), unique=True)
    order_type = Column(SQLEnum(OrderType), nullable=False)  # BUY or SELL

    # Instrument
    instrument = Column(SQLEnum(InstrumentType), nullable=False)
    option_type = Column(SQLEnum(OptionType), nullable=False)
    strike = Column(Numeric(10, 2), nullable=False)
    expiry_date = Column(DateTime, nullable=False)

    # Quantity and Price
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 4), nullable=False)
    filled_quantity = Column(Integer, default=0)
    average_fill_price = Column(Numeric(10, 4))

    # Status
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, index=True)
    rejection_reason = Column(String(500))

    # Execution Details
    execution_time = Column(DateTime)
    slippage_points = Column(Numeric(10, 4))
    slippage_percent = Column(Float)

    # Metadata
    strategy_name = Column(String(100))
    is_paper_order = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    trade = relationship("Trade", backref="orders")

    __table_args__ = (
        Index('idx_order_timestamp', 'order_timestamp'),
        Index('idx_order_status', 'status'),
    )


# ============================================================================
# PORTFOLIO & P&L MODELS
# ============================================================================

class DailyPortfolio(Base):
    """
    Daily portfolio snapshot for tracking equity curve and performance.
    """
    __tablename__ = "daily_portfolios"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, index=True, nullable=False, unique=True)

    # Capital
    starting_capital = Column(Numeric(15, 2))
    current_capital = Column(Numeric(15, 2))
    available_capital = Column(Numeric(15, 2))
    used_capital = Column(Numeric(15, 2))

    # P&L
    daily_pnl = Column(Numeric(12, 4))
    cumulative_pnl = Column(Numeric(12, 4))
    daily_pnl_percent = Column(Float)
    cumulative_pnl_percent = Column(Float)

    # Positions
    open_positions_count = Column(Integer)
    trades_executed = Column(Integer)
    winning_trades = Column(Integer)
    losing_trades = Column(Integer)

    # Risk
    max_drawdown = Column(Float)
    current_drawdown = Column(Float)
    win_rate_percent = Column(Float)
    profit_factor = Column(Float)  # Total winners / Total losers

    # Performance
    sharpe_ratio = Column(Float)
    sortino_ratio = Column(Float)
    return_percent = Column(Float)

    # Limits Tracking
    max_loss_limit = Column(Numeric(12, 4))
    max_loss_hit = Column(Boolean, default=False)
    max_profit_hit = Column(Boolean, default=False)

    # Metadata
    is_paper_trading = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index('idx_portfolio_date', 'date'),
    )


# ============================================================================
# NEWS & SENTIMENT MODELS
# ============================================================================

class NewsItem(Base):
    """
    News items impacting markets.
    """
    __tablename__ = "news_items"

    id = Column(Integer, primary_key=True)
    news_timestamp = Column(DateTime, nullable=False, index=True)
    publication_timestamp = Column(DateTime, index=True)

    # Content
    title = Column(String(500), nullable=False)
    summary = Column(Text)
    source = Column(String(100), nullable=False)
    source_url = Column(String(500))

    # Classification
    topic = Column(String(100))
    market_affected = Column(String(100))  # NIFTY, SENSEX, GLOBAL, etc.
    sentiment = Column(SQLEnum(SentimentType), nullable=False)
    confidence = Column(Float)

    # Impact Assessment
    expected_impact = Column(String(50))  # HIGH, MEDIUM, LOW
    actual_impact = Column(String(50))
    impact_direction = Column(String(20))  # BULLISH, BEARISH, NEUTRAL

    # Reliability
    source_reliability = Column(Integer)  # 0-100
    is_verified = Column(Boolean, default=False)

    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index('idx_news_timestamp', 'news_timestamp'),
        Index('idx_news_market', 'market_affected'),
    )


class EconomicEvent(Base):
    """
    Scheduled economic events that may impact trading.
    """
    __tablename__ = "economic_events"

    id = Column(Integer, primary_key=True)
    event_datetime = Column(DateTime, nullable=False, index=True)
    timezone = Column(String(50), default="Asia/Kolkata")

    # Event Details
    event_name = Column(String(200), nullable=False)
    country = Column(String(50))
    importance = Column(String(20))  # HIGH, MEDIUM, LOW
    forecast = Column(String(200))
    previous = Column(String(200))
    actual = Column(String(200))

    # Impact
    expected_volatility = Column(String(20))
    market_affected = Column(String(100))

    # Blackout Configuration
    blackout_minutes_before = Column(Integer, default=30)
    blackout_minutes_after = Column(Integer, default=30)

    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index('idx_event_datetime', 'event_datetime'),
    )


# ============================================================================
# SYSTEM MONITORING MODELS
# ============================================================================

class SystemMetric(Base):
    """
    System health and performance metrics.
    """
    __tablename__ = "system_metrics"

    id = Column(Integer, primary_key=True)
    metric_timestamp = Column(TIMESTAMP, index=True, nullable=False)

    # System Health
    cpu_percent = Column(Float)
    memory_percent = Column(Float)
    disk_percent = Column(Float)

    # Data Feed
    data_feed_status = Column(String(20))  # CONNECTED, DISCONNECTED, STALE
    last_data_timestamp = Column(DateTime)
    data_latency_ms = Column(Integer)
    missing_candles = Column(Integer)

    # Broker
    broker_status = Column(String(20))  # CONNECTED, DISCONNECTED
    broker_latency_ms = Column(Integer)

    # Database
    db_connection_count = Column(Integer)
    db_query_latency_ms = Column(Float)

    # Trading
    active_signals = Column(Integer)
    active_trades = Column(Integer)
    pending_orders = Column(Integer)

    # Error Tracking
    error_count = Column(Integer, default=0)
    warning_count = Column(Integer, default=0)

    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index('idx_metric_timestamp', 'metric_timestamp'),
    )


class ErrorLog(Base):
    """
    Error and exception logging.
    """
    __tablename__ = "error_logs"

    id = Column(Integer, primary_key=True)
    error_timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # Error Details
    error_type = Column(String(100), nullable=False)
    error_message = Column(Text, nullable=False)
    stack_trace = Column(Text)
    error_level = Column(String(20))  # ERROR, CRITICAL, WARNING

    # Context
    component = Column(String(100))  # market_data, signal, execution, etc.
    user_action = Column(String(200))

    # Resolution
    is_resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text)

    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index('idx_error_timestamp', 'error_timestamp'),
        Index('idx_error_type', 'error_type'),
    )


class AuditLog(Base):
    """
    Complete audit trail for all critical actions.
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    action_timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # Action Details
    action_type = Column(String(100), nullable=False)  # ORDER_PLACED, TRADE_OPENED, POSITION_CLOSED, etc.
    entity_type = Column(String(100))  # Signal, Trade, Order
    entity_id = Column(Integer)

    # Before/After State
    before_state = Column(Text)  # JSON
    after_state = Column(Text)  # JSON
    change_details = Column(Text)  # Human readable

    # User Info
    user_id = Column(String(100))
    user_action = Column(String(200))  # Manual vs Automatic

    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index('idx_audit_timestamp', 'action_timestamp'),
        Index('idx_audit_entity', 'entity_type', 'entity_id'),
    )


# ============================================================================
# ML/BACKTESTING MODELS
# ============================================================================

class BacktestResult(Base):
    """
    Results from a backtest run.
    """
    __tablename__ = "backtest_results"

    id = Column(Integer, primary_key=True)
    backtest_timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # Backtest Parameters
    strategy_name = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    initial_capital = Column(Numeric(15, 2), nullable=False)

    # Performance Metrics
    total_trades = Column(Integer)
    winning_trades = Column(Integer)
    losing_trades = Column(Integer)
    win_rate = Column(Float)
    profit_factor = Column(Float)
    average_win = Column(Numeric(12, 4))
    average_loss = Column(Numeric(12, 4))
    expectancy = Column(Numeric(12, 4))

    # Returns
    total_return_percent = Column(Float)
    cagr = Column(Float)
    sharpe_ratio = Column(Float)
    sortino_ratio = Column(Float)
    max_drawdown = Column(Float)
    recovery_factor = Column(Float)

    # Risk Metrics
    average_holding_time_minutes = Column(Float)
    largest_win = Column(Numeric(12, 4))
    largest_loss = Column(Numeric(12, 4))
    consecutive_losses = Column(Integer)

    # Costs
    total_brokerage = Column(Numeric(12, 4))
    total_stt = Column(Numeric(12, 4))
    total_taxes = Column(Numeric(12, 4))
    total_slippage = Column(Numeric(12, 4))

    # Configuration
    config = Column(Text)  # JSON with all parameters

    # Notes
    notes = Column(Text)

    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index('idx_backtest_timestamp', 'backtest_timestamp'),
    )


class MLModel(Base):
    """
    Trained ML models for signal prediction.
    """
    __tablename__ = "ml_models"

    id = Column(Integer, primary_key=True)
    model_timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # Model Info
    model_name = Column(String(100), nullable=False, unique=True)
    model_type = Column(String(50), nullable=False)  # xgboost, lightgbm, neural
    model_version = Column(String(20))

    # Training Data
    training_start_date = Column(DateTime)
    training_end_date = Column(DateTime)
    training_samples = Column(Integer)
    validation_samples = Column(Integer)
    test_samples = Column(Integer)

    # Performance
    training_accuracy = Column(Float)
    validation_accuracy = Column(Float)
    test_accuracy = Column(Float)
    f1_score = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    auc_roc = Column(Float)

    # Trading Performance
    backtest_sharp = Column(Float)
    backtest_win_rate = Column(Float)
    backtest_profit_factor = Column(Float)

    # Model Storage
    model_file_path = Column(String(500))
    model_features = Column(Text)  # JSON list
    model_hyperparameters = Column(Text)  # JSON

    # Status
    is_active = Column(Boolean, default=False)
    is_deprecated = Column(Boolean, default=False)
    last_used = Column(DateTime)

    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index('idx_model_timestamp', 'model_timestamp'),
    )
