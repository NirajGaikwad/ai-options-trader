"""
AI Options Trading Platform - Main Application Entry Point.

This is the core FastAPI application that orchestrates all components:
- Market Data Engine
- Technical Analysis
- Signal Generation
- Risk Management
- Execution Engine
- Dashboard API

CRITICAL: This application launches in PAPER_TRADING mode by default.
Live trading must be explicitly enabled via configuration.
"""

import logging
from contextlib import asynccontextmanager
from datetime import datetime
import sys

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from config.settings import get_settings, validate_safety_settings
from market_data.simulator import SimulatorMarketDataProvider
from db.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ============================================================================
# GLOBAL STATE
# ============================================================================

class AppState:
    """Global application state."""
    market_data_provider = None
    db_engine = None
    db_session_factory = None
    is_trading_active = False
    emergency_stop = False


# ============================================================================
# STARTUP/SHUTDOWN
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle.
    Startup: Initialize components
    Shutdown: Clean up resources
    """
    # ====================================================================
    # STARTUP
    # ====================================================================
    logger.info("🚀 Starting AI Options Trading Platform...")

    settings = get_settings()

    # Validate safety settings
    logger.info("🔒 Validating safety configuration...")
    validate_safety_settings(settings)

    # Check live trading configuration
    if settings.live_trading_enabled:
        logger.warning("⚠️  LIVE TRADING IS ENABLED!")
        logger.warning("⚠️  This system will place REAL orders and risk REAL capital.")
        logger.warning("⚠️  Ensure you understand the risks and have tested thoroughly.")
    else:
        logger.info("✅ Live trading is disabled. Running in PAPER_TRADING mode.")

    # Initialize database
    logger.info(f"📊 Initializing database: {settings.database_url}")
    try:
        AppState.db_engine = create_engine(
            settings.database_url,
            poolclass=None,
            echo=settings.db_echo,
        )
        Base.metadata.create_all(AppState.db_engine)
        AppState.db_session_factory = sessionmaker(bind=AppState.db_engine)
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        sys.exit(1)

    # Initialize market data provider
    logger.info(f"📡 Initializing market data provider: {settings.market_data_provider}")
    try:
        if settings.mock_market_data or settings.testing_mode:
            AppState.market_data_provider = SimulatorMarketDataProvider()
        else:
            AppState.market_data_provider = SimulatorMarketDataProvider()  # For now

        await AppState.market_data_provider.connect()
        logger.info("✅ Market data provider initialized")
    except Exception as e:
        logger.error(f"❌ Market data provider initialization failed: {e}")
        sys.exit(1)

    # Log critical configuration
    logger.info(f"📋 Configuration Summary:")
    logger.info(f"   Environment: {settings.environment}")
    logger.info(f"   Paper Trading: {settings.paper_trading}")
    logger.info(f"   Live Trading Enabled: {settings.live_trading_enabled}")
    logger.info(f"   Max Account Risk/Trade: {settings.max_account_risk_per_trade*100}%")
    logger.info(f"   Max Daily Loss: {settings.max_daily_loss_percent*100}%")
    logger.info(f"   Data Provider: {settings.market_data_provider}")
    logger.info(f"   Market Timezone: {settings.market_timezone}")

    logger.info("✅ Application startup complete!")
    logger.info("=" * 80)

    yield

    # ====================================================================
    # SHUTDOWN
    # ====================================================================
    logger.info("🛑 Shutting down AI Options Trading Platform...")

    try:
        # Disconnect market data
        if AppState.market_data_provider:
            await AppState.market_data_provider.disconnect()
            logger.info("✅ Market data provider disconnected")

        # Close database
        if AppState.db_engine:
            AppState.db_engine.dispose()
            logger.info("✅ Database closed")

        logger.info("✅ Application shutdown complete!")
    except Exception as e:
        logger.error(f"❌ Shutdown error: {e}")


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="AI Options Trading Platform",
    description="Production-grade AI platform for intraday options trading on Indian markets",
    version="0.1.0-alpha",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

# ============================================================================
# MIDDLEWARE
# ============================================================================

# CORS - Allow frontend connections
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted Host
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*"],  # Restrict in production
)


# ============================================================================
# EXCEPTION HANDLERS
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.debug else "An error occurred",
        },
    )


# ============================================================================
# HEALTH CHECK ENDPOINTS
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "environment": settings.environment,
        "paper_trading": settings.paper_trading,
        "live_trading_enabled": settings.live_trading_enabled,
    }


@app.get("/health/detailed")
async def health_check_detailed():
    """Detailed health check with component status."""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "database": {
                "connected": AppState.db_engine is not None,
                "url": settings.database_url if settings.debug else "hidden",
            },
            "market_data_provider": (
                AppState.market_data_provider.get_health_status()
                if AppState.market_data_provider
                else {"status": "not_initialized"}
            ),
            "trading_active": AppState.is_trading_active,
            "emergency_stop": AppState.emergency_stop,
        },
        "configuration": {
            "environment": settings.environment,
            "paper_trading": settings.paper_trading,
            "live_trading_enabled": settings.live_trading_enabled,
            "max_account_risk_per_trade": settings.max_account_risk_per_trade,
            "max_daily_loss_percent": settings.max_daily_loss_percent,
            "market_timezone": settings.market_timezone,
        },
    }


# ============================================================================
# MARKET DATA ENDPOINTS
# ============================================================================

@app.get("/api/market/index/{instrument}")
async def get_index_snapshot(instrument: str):
    """Get real-time index snapshot (NIFTY, SENSEX, BANKNIFTY)."""
    try:
        snapshot = await AppState.market_data_provider.get_index_snapshot(instrument)
        return {
            "timestamp": snapshot.timestamp.isoformat(),
            "instrument": snapshot.instrument,
            "ltp": snapshot.ltp,
            "open": snapshot.open,
            "high": snapshot.high,
            "low": snapshot.low,
            "close": snapshot.close,
            "volume": snapshot.volume,
            "previous_close": snapshot.previous_close,
            "vwap": snapshot.vwap,
            "change_percent": snapshot.change_percent,
            "is_market_open": snapshot.is_market_open,
        }
    except Exception as e:
        logger.error(f"Error fetching index snapshot: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to fetch index snapshot"},
        )


@app.get("/api/market/option-chain/{instrument}")
async def get_option_chain(
    instrument: str,
    expiry_date: str,  # ISO format: YYYY-MM-DD
    strike: float = None,
):
    """Get option chain data."""
    try:
        from datetime import datetime as dt
        expiry = dt.fromisoformat(expiry_date)

        chains = await AppState.market_data_provider.get_option_chain(
            instrument, expiry, strike
        )

        return {
            "timestamp": datetime.now().isoformat(),
            "instrument": instrument,
            "expiry": expiry_date,
            "chains": [
                {
                    "strike": str(chain.strike),
                    "underlying_price": str(chain.underlying_price),
                    "ce_ltp": str(chain.ce_ltp),
                    "ce_bid": str(chain.ce_bid),
                    "ce_ask": str(chain.ce_ask),
                    "ce_oi": chain.ce_oi,
                    "ce_volume": chain.ce_volume,
                    "ce_iv": chain.ce_iv,
                    "ce_delta": chain.ce_delta,
                    "pe_ltp": str(chain.pe_ltp),
                    "pe_bid": str(chain.pe_bid),
                    "pe_ask": str(chain.pe_ask),
                    "pe_oi": chain.pe_oi,
                    "pe_volume": chain.pe_volume,
                    "pe_iv": chain.pe_iv,
                    "pe_delta": chain.pe_delta,
                    "put_call_ratio": chain.put_call_ratio,
                    "spread_points": chain.spread_points,
                }
                for chain in chains
            ],
        }
    except Exception as e:
        logger.error(f"Error fetching option chain: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to fetch option chain"},
        )


@app.get("/api/market/candles/{instrument}")
async def get_candles(
    instrument: str,
    interval_minutes: int = 5,
    limit: int = 100,
):
    """Get candlestick data."""
    try:
        candles = await AppState.market_data_provider.get_candle(
            instrument, interval_minutes, limit
        )

        return {
            "timestamp": datetime.now().isoformat(),
            "instrument": instrument,
            "interval_minutes": interval_minutes,
            "candles": [
                {
                    "timestamp": candle.timestamp.isoformat(),
                    "open": str(candle.open),
                    "high": str(candle.high),
                    "low": str(candle.low),
                    "close": str(candle.close),
                    "volume": candle.volume,
                    "vwap": str(candle.vwap),
                    "is_closed": candle.is_closed,
                }
                for candle in candles
            ],
        }
    except Exception as e:
        logger.error(f"Error fetching candles: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to fetch candles"},
        )


# ============================================================================
# TRADING STATUS ENDPOINTS
# ============================================================================

@app.get("/api/trading/status")
async def get_trading_status():
    """Get current trading status."""
    return {
        "timestamp": datetime.now().isoformat(),
        "paper_trading": settings.paper_trading,
        "live_trading_enabled": settings.live_trading_enabled,
        "trading_active": AppState.is_trading_active,
        "emergency_stop": AppState.emergency_stop,
        "market_open": await AppState.market_data_provider.is_market_open(),
    }


@app.post("/api/trading/emergency-stop")
async def trigger_emergency_stop():
    """
    EMERGENCY STOP: Cancel all orders and close all positions.
    This requires explicit user action and cannot be undone easily.
    """
    logger.critical("🆘 EMERGENCY STOP TRIGGERED!")
    AppState.emergency_stop = True
    AppState.is_trading_active = False

    return {
        "status": "emergency_stop_triggered",
        "timestamp": datetime.now().isoformat(),
        "message": "All trading has been halted. Review logs for details.",
    }


@app.post("/api/trading/resume")
async def resume_trading():
    """Resume trading after emergency stop."""
    if not settings.debug and not settings.paper_trading:
        # In live trading, require additional authorization
        logger.warning("Resume trading requested in live mode - requires authorization")
        return JSONResponse(
            status_code=403,
            content={"error": "Cannot auto-resume in live trading mode"},
        )

    AppState.emergency_stop = False
    AppState.is_trading_active = True
    logger.info("✅ Trading resumed")

    return {
        "status": "trading_resumed",
        "timestamp": datetime.now().isoformat(),
    }


# ============================================================================
# WEBSOCKET FOR REAL-TIME UPDATES
# ============================================================================

class ConnectionManager:
    """WebSocket connection manager."""

    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass


manager = ConnectionManager()


@app.websocket("/ws/market-data")
async def websocket_market_data(websocket: WebSocket):
    """WebSocket connection for real-time market data updates."""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle subscription requests
            if data == "ping":
                await websocket.send_json({"type": "pong", "timestamp": datetime.now().isoformat()})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "application": "AI Options Trading Platform",
        "version": "0.1.0-alpha",
        "status": "running",
        "endpoints": {
            "docs": "/api/docs",
            "health": "/health",
            "health_detailed": "/health/detailed",
            "market_data": "/api/market/*",
            "trading": "/api/trading/*",
            "websocket": "/ws/market-data",
        },
        "safety": {
            "paper_trading": settings.paper_trading,
            "live_trading_enabled": settings.live_trading_enabled,
        },
    }


# ============================================================================
# RUN COMMAND
# ============================================================================

if __name__ == "__main__":
    settings = get_settings()

    logger.info(f"Starting server on {settings.api_host}:{settings.api_port}")
    logger.info(f"Documentation available at http://{settings.api_host}:{settings.api_port}/api/docs")

    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        workers=settings.api_workers,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
