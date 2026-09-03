"""
Configuration management for AI Options Trading Platform.
Loads from environment variables with defaults.
"""

import os
from typing import Optional, List
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """Main application settings."""

    # ========================================================================
    # APPLICATION MODE
    # ========================================================================
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    log_level: str = Field(default="DEBUG", env="LOG_LEVEL")

    # CRITICAL SAFETY DEFAULTS
    paper_trading: bool = Field(default=True, env="PAPER_TRADING")
    live_trading_enabled: bool = Field(default=False, env="LIVE_TRADING_ENABLED")
    trading_mode: str = Field(default="PAPER", env="TRADING_MODE")

    @validator("live_trading_enabled")
    def validate_live_trading(cls, v: bool, values: dict):
        """Ensure live trading is explicitly enabled."""
        if v and not os.getenv("LIVE_TRADING_ENABLED") == "true":
            raise ValueError(
                "Live trading can only be enabled by setting LIVE_TRADING_ENABLED=true. "
                "This is a safety measure. Never bypass this."
            )
        return v

    # ========================================================================
    # DATABASE CONFIGURATION
    # ========================================================================
    db_host: str = Field(default="localhost", env="DB_HOST")
    db_port: int = Field(default=5432, env="DB_PORT")
    db_name: str = Field(default="options_trading", env="DB_NAME")
    db_user: str = Field(default="trader", env="DB_USER")
    db_password: str = Field(default="", env="DB_PASSWORD")
    db_pool_size: int = Field(default=10, env="DB_POOL_SIZE")
    db_max_overflow: int = Field(default=20, env="DB_MAX_OVERFLOW")
    db_echo: bool = Field(default=False, env="DB_ECHO")

    # TimescaleDB
    timescale_enabled: bool = Field(default=True, env="TIMESCALE_ENABLED")
    timescale_chunk_interval: str = Field(default="1 day", env="TIMESCALE_CHUNK_INTERVAL")

    @property
    def database_url(self) -> str:
        """Construct database URL."""
        return (
            f"postgresql://{self.db_user}:{self.db_password}@"
            f"{self.db_host}:{self.db_port}/{self.db_name}"
        )

    # ========================================================================
    # REDIS CONFIGURATION
    # ========================================================================
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_db: int = Field(default=0, env="REDIS_DB")
    redis_password: str = Field(default="", env="REDIS_PASSWORD")
    redis_pool_size: int = Field(default=10, env="REDIS_POOL_SIZE")

    @property
    def redis_url(self) -> str:
        """Construct Redis URL."""
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    # ========================================================================
    # MARKET DATA CONFIGURATION
    # ========================================================================
    market_data_provider: str = Field(default="zerodha", env="MARKET_DATA_PROVIDER")
    data_feed_type: str = Field(default="websocket", env="DATA_FEED_TYPE")

    # Market Hours (Asia/Kolkata)
    market_timezone: str = Field(default="Asia/Kolkata", env="MARKET_TIMEZONE")
    market_open_time: str = Field(default="09:15", env="MARKET_OPEN_TIME")
    market_close_time: str = Field(default="15:30", env="MARKET_CLOSE_TIME")
    pre_market_start: str = Field(default="09:00", env="PRE_MARKET_START")
    pre_market_end: str = Field(default="09:15", env="PRE_MARKET_END")
    post_market_start: str = Field(default="15:30", env="POST_MARKET_START")
    post_market_end: str = Field(default="16:00", env="POST_MARKET_END")

    # Data Freshness
    data_stale_threshold_seconds: int = Field(default=10, env="DATA_STALE_THRESHOLD_SECONDS")
    data_validation_enabled: bool = Field(default=True, env="DATA_VALIDATION_ENABLED")

    # Instruments
    nifty_symbol: str = Field(default="NIFTY50", env="NIFTY_SYMBOL")
    nifty_index_symbol: str = Field(default="NIFTY%2050", env="NIFTY_INDEX_SYMBOL")
    sensex_symbol: str = Field(default="SENSEX", env="SENSEX_SYMBOL")
    sensex_index_symbol: str = Field(default="BSE%20SENSEX", env="SENSEX_INDEX_SYMBOL")
    banknifty_symbol: str = Field(default="BANKNIFTY", env="BANKNIFTY_SYMBOL")

    # Candle Intervals
    candle_intervals: List[str] = Field(default="1,3,5,15,30,60,1D", env="CANDLE_INTERVALS")

    @validator("candle_intervals", pre=True)
    def parse_candle_intervals(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",")]
        return v

    # ========================================================================
    # DATA PROVIDER - ZERODHA
    # ========================================================================
    zerodha_api_key: str = Field(default="", env="ZERODHA_API_KEY")
    zerodha_api_secret: str = Field(default="", env="ZERODHA_API_SECRET")
    zerodha_user_id: str = Field(default="", env="ZERODHA_USER_ID")
    zerodha_password: str = Field(default="", env="ZERODHA_PASSWORD")

    # ========================================================================
    # BROKER CONFIGURATION
    # ========================================================================
    broker_name: str = Field(default="zerodha", env="BROKER_NAME")
    broker_api_key: str = Field(default="", env="BROKER_API_KEY")
    broker_api_secret: str = Field(default="", env="BROKER_API_SECRET")
    broker_user_id: str = Field(default="", env="BROKER_USER_ID")
    broker_password: str = Field(default="", env="BROKER_PASSWORD")
    broker_api_timeout: int = Field(default=30, env="BROKER_API_TIMEOUT")
    broker_retry_count: int = Field(default=3, env="BROKER_RETRY_COUNT")
    broker_retry_delay: int = Field(default=1, env="BROKER_RETRY_DELAY")

    # ========================================================================
    # TRADING CONFIGURATION
    # ========================================================================
    # Account Risk Management
    max_account_risk_per_trade: float = Field(default=0.01, env="MAX_ACCOUNT_RISK_PER_TRADE")
    max_daily_loss_percent: float = Field(default=0.02, env="MAX_DAILY_LOSS_PERCENT")
    max_daily_profit_percent: float = Field(default=0.05, env="MAX_DAILY_PROFIT_PERCENT")
    max_consecutive_losses: int = Field(default=3, env="MAX_CONSECUTIVE_LOSSES")
    max_trades_per_day: int = Field(default=10, env="MAX_TRADES_PER_DAY")
    max_open_positions: int = Field(default=2, env="MAX_OPEN_POSITIONS")

    # Position Sizing
    position_sizing_method: str = Field(default="kelly", env="POSITION_SIZING_METHOD")
    kelly_fraction: float = Field(default=0.25, env="KELLY_FRACTION")

    # Order Execution
    max_slippage_percent: float = Field(default=0.5, env="MAX_SLIPPAGE_PERCENT")
    max_spread_percent: float = Field(default=1.0, env="MAX_SPREAD_PERCENT")
    min_liquidity_oi: int = Field(default=10000, env="MIN_LIQUIDITY_OI")

    # Entry/Exit Timing
    cooldown_after_loss_minutes: int = Field(default=15, env="COOLDOWN_AFTER_LOSS_MINUTES")
    cooldown_after_win_minutes: int = Field(default=5, env="COOLDOWN_AFTER_WIN_MINUTES")
    max_holding_time_minutes: int = Field(default=240, env="MAX_HOLDING_TIME_MINUTES")
    market_close_square_off_time: str = Field(default="15:25", env="MARKET_CLOSE_SQUARE_OFF_TIME")

    # Stop Loss & Targets
    default_stop_loss_type: str = Field(default="atr", env="DEFAULT_STOP_LOSS_TYPE")
    default_stop_loss_atr_multiplier: float = Field(default=2.0, env="DEFAULT_STOP_LOSS_ATR_MULTIPLIER")
    default_risk_reward_ratio: float = Field(default=2.0, env="DEFAULT_RISK_REWARD_RATIO")

    # News Event Blackout
    news_blackout_enabled: bool = Field(default=True, env="NEWS_BLACKOUT_ENABLED")
    news_blackout_minutes_before: int = Field(default=30, env="NEWS_BLACKOUT_MINUTES_BEFORE")
    major_event_blackout_minutes: int = Field(default=30, env="MAJOR_EVENT_BLACKOUT_MINUTES")

    # ========================================================================
    # STRATEGY CONFIGURATION
    # ========================================================================
    strategy_vwap_trend_enabled: bool = Field(default=True, env="STRATEGY_VWAP_TREND_ENABLED")
    strategy_opening_breakout_enabled: bool = Field(default=True, env="STRATEGY_OPENING_BREAKOUT_ENABLED")
    strategy_support_resistance_enabled: bool = Field(default=True, env="STRATEGY_SUPPORT_RESISTANCE_ENABLED")
    strategy_breakout_retest_enabled: bool = Field(default=True, env="STRATEGY_BREAKOUT_RETEST_ENABLED")
    strategy_momentum_enabled: bool = Field(default=True, env="STRATEGY_MOMENTUM_ENABLED")
    strategy_option_chain_enabled: bool = Field(default=True, env="STRATEGY_OPTION_CHAIN_ENABLED")
    strategy_multiframe_enabled: bool = Field(default=True, env="STRATEGY_MULTIFRAME_ENABLED")

    # Confidence Thresholds
    min_trade_confidence: int = Field(default=75, env="MIN_TRADE_CONFIDENCE")
    min_trade_liquidity_score: int = Field(default=85, env="MIN_TRADE_LIQUIDITY_SCORE")
    min_trade_risk_reward: float = Field(default=1.5, env="MIN_TRADE_RISK_REWARD")

    # ========================================================================
    # TECHNICAL INDICATORS
    # ========================================================================
    rsi_period: int = Field(default=14, env="RSI_PERIOD")
    macd_fast: int = Field(default=12, env="MACD_FAST")
    macd_slow: int = Field(default=26, env="MACD_SLOW")
    macd_signal: int = Field(default=9, env="MACD_SIGNAL")
    ema_fast: int = Field(default=9, env="EMA_FAST")
    ema_medium: int = Field(default=20, env="EMA_MEDIUM")
    ema_trend_1: int = Field(default=50, env="EMA_TREND_1")
    ema_trend_2: int = Field(default=100, env="EMA_TREND_2")
    ema_trend_3: int = Field(default=200, env="EMA_TREND_3")
    atr_period: int = Field(default=14, env="ATR_PERIOD")
    bollinger_period: int = Field(default=20, env="BOLLINGER_PERIOD")
    bollinger_std_dev: float = Field(default=2.0, env="BOLLINGER_STD_DEV")
    adx_period: int = Field(default=14, env="ADX_PERIOD")

    # ========================================================================
    # API CONFIGURATION
    # ========================================================================
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_workers: int = Field(default=4, env="API_WORKERS")
    api_timeout: int = Field(default=30, env="API_TIMEOUT")
    api_rate_limit_enabled: bool = Field(default=True, env="API_RATE_LIMIT_ENABLED")
    api_rate_limit_requests_per_minute: int = Field(default=60, env="API_RATE_LIMIT_REQUESTS_PER_MINUTE")

    # CORS
    cors_origins: List[str] = Field(default="http://localhost:3000,http://localhost:3001", env="CORS_ORIGINS")
    cors_allow_credentials: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")

    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",")]
        return v

    # ========================================================================
    # FRONTEND CONFIGURATION
    # ========================================================================
    frontend_host: str = Field(default="0.0.0.0", env="FRONTEND_HOST")
    frontend_port: int = Field(default=3000, env="FRONTEND_PORT")
    frontend_api_url: str = Field(default="http://localhost:8000", env="FRONTEND_API_URL")
    frontend_ws_url: str = Field(default="ws://localhost:8000", env="FRONTEND_WS_URL")

    # ========================================================================
    # MONITORING & LOGGING
    # ========================================================================
    prometheus_enabled: bool = Field(default=True, env="PROMETHEUS_ENABLED")
    prometheus_port: int = Field(default=9090, env="PROMETHEUS_PORT")
    grafana_enabled: bool = Field(default=True, env="GRAFANA_ENABLED")
    grafana_port: int = Field(default=3001, env="GRAFANA_PORT")
    grafana_admin_password: str = Field(default="admin", env="GRAFANA_ADMIN_PASSWORD")

    log_file_path: str = Field(default="./logs", env="LOG_FILE_PATH")
    log_max_size_mb: int = Field(default=100, env="LOG_MAX_SIZE_MB")
    log_backup_count: int = Field(default=10, env="LOG_BACKUP_COUNT")
    log_format: str = Field(default="json", env="LOG_FORMAT")
    structured_logging_enabled: bool = Field(default=True, env="STRUCTURED_LOGGING_ENABLED")

    # ========================================================================
    # SECURITY
    # ========================================================================
    jwt_secret_key: str = Field(default="change_me_in_production", env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_expiration_hours: int = Field(default=24, env="JWT_EXPIRATION_HOURS")
    internal_api_key: str = Field(default="", env="INTERNAL_API_KEY")

    # ========================================================================
    # EMERGENCY CONTROLS
    # ========================================================================
    emergency_stop_enabled: bool = Field(default=False, env="EMERGENCY_STOP_ENABLED")
    circuit_breaker_enabled: bool = Field(default=True, env="CIRCUIT_BREAKER_ENABLED")
    circuit_breaker_error_threshold: int = Field(default=5, env="CIRCUIT_BREAKER_ERROR_THRESHOLD")
    circuit_breaker_timeout_seconds: int = Field(default=300, env="CIRCUIT_BREAKER_TIMEOUT_SECONDS")

    max_india_vix: float = Field(default=50, env="MAX_INDIA_VIX")
    min_liquidity_for_trade: bool = Field(default=True, env="MIN_LIQUIDITY_FOR_TRADE")

    # ========================================================================
    # DEVELOPMENT & TESTING
    # ========================================================================
    testing_mode: bool = Field(default=False, env="TESTING_MODE")
    mock_broker: bool = Field(default=False, env="MOCK_BROKER")
    mock_market_data: bool = Field(default=False, env="MOCK_MARKET_DATA")
    seed_data_on_start: bool = Field(default=False, env="SEED_DATA_ON_START")

    # ========================================================================
    # NOTIFICATIONS
    # ========================================================================
    notifications_enabled: bool = Field(default=True, env="NOTIFICATIONS_ENABLED")
    notification_email_enabled: bool = Field(default=False, env="NOTIFICATION_EMAIL_ENABLED")
    notification_email_to: str = Field(default="", env="NOTIFICATION_EMAIL_TO")
    notification_slack_enabled: bool = Field(default=False, env="NOTIFICATION_SLACK_ENABLED")
    notification_slack_webhook: str = Field(default="", env="NOTIFICATION_SLACK_WEBHOOK")
    notification_telegram_enabled: bool = Field(default=False, env="NOTIFICATION_TELEGRAM_ENABLED")
    notification_telegram_token: str = Field(default="", env="NOTIFICATION_TELEGRAM_TOKEN")
    notification_telegram_chat_id: str = Field(default="", env="NOTIFICATION_TELEGRAM_CHAT_ID")

    alert_on_new_signal: bool = Field(default=True, env="ALERT_ON_NEW_SIGNAL")
    alert_on_large_loss: bool = Field(default=True, env="ALERT_ON_LARGE_LOSS")
    alert_on_system_error: bool = Field(default=True, env="ALERT_ON_SYSTEM_ERROR")
    alert_on_data_issue: bool = Field(default=True, env="ALERT_ON_DATA_ISSUE")

    # ========================================================================
    # DATA RETENTION
    # ========================================================================
    data_retention_days: int = Field(default=365, env="DATA_RETENTION_DAYS")
    backup_enabled: bool = Field(default=True, env="BACKUP_ENABLED")
    backup_interval_hours: int = Field(default=24, env="BACKUP_INTERVAL_HOURS")

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


def validate_safety_settings(settings: Settings) -> None:
    """Validate critical safety settings."""
    errors = []

    # Check live trading is disabled by default
    if settings.live_trading_enabled and not settings.paper_trading:
        errors.append("Live trading enabled without paper trading. This is dangerous!")

    # Check maximum risk per trade
    if settings.max_account_risk_per_trade > 0.05:  # 5% max per trade
        errors.append("Max account risk per trade > 5%. This is too risky!")

    # Check daily loss limit
    if settings.max_daily_loss_percent > 0.10:  # 10% max daily loss
        errors.append("Max daily loss > 10%. This is too risky!")

    # Check data freshness
    if settings.data_stale_threshold_seconds > 60:
        errors.append("Data stale threshold > 60 seconds. May lead to stale data trades!")

    # Check emergency stop in production
    if settings.environment == "production" and not settings.circuit_breaker_enabled:
        errors.append("Circuit breaker disabled in production!")

    if errors:
        print("\n❌ CONFIGURATION WARNINGS:\n")
        for error in errors:
            print(f"  ⚠️  {error}")
        print()


if __name__ == "__main__":
    settings = get_settings()
    print("✅ Configuration loaded successfully!")
    print(f"Environment: {settings.environment}")
    print(f"Paper Trading: {settings.paper_trading}")
    print(f"Live Trading Enabled: {settings.live_trading_enabled}")
    print(f"Database: {settings.database_url}")
    validate_safety_settings(settings)
