#!/usr/bin/env python3
"""
Database initialization script.
Creates tables and initial data.
"""

import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from backend.db.models import Base
from backend.config.settings import get_settings


def create_timescale_hypertables(engine):
    """Create TimescaleDB hypertables for time-series data."""
    with engine.connect() as conn:
        # Enable TimescaleDB extension
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;"))

        # Create hypertable for market snapshots
        try:
            conn.execute(text("""
                SELECT create_hypertable('market_snapshots', 'timestamp', if_not_exists => TRUE);
            """))
            print("✅ Created hypertable: market_snapshots")
        except Exception as e:
            print(f"⚠️  market_snapshots hypertable: {e}")

        # Create hypertable for candles
        try:
            conn.execute(text("""
                SELECT create_hypertable('candles', 'timestamp', if_not_exists => TRUE);
            """))
            print("✅ Created hypertable: candles")
        except Exception as e:
            print(f"⚠️  candles hypertable: {e}")

        # Create hypertable for option chain snapshots
        try:
            conn.execute(text("""
                SELECT create_hypertable('option_chain_snapshots', 'timestamp', if_not_exists => TRUE);
            """))
            print("✅ Created hypertable: option_chain_snapshots")
        except Exception as e:
            print(f"⚠️  option_chain_snapshots hypertable: {e}")

        # Create hypertable for system metrics
        try:
            conn.execute(text("""
                SELECT create_hypertable('system_metrics', 'metric_timestamp', if_not_exists => TRUE);
            """))
            print("✅ Created hypertable: system_metrics")
        except Exception as e:
            print(f"⚠️  system_metrics hypertable: {e}")

        conn.commit()


def create_indexes(engine):
    """Create additional indexes for performance."""
    with engine.connect() as conn:
        indexes = [
            # Market snapshots
            "CREATE INDEX IF NOT EXISTS idx_market_snapshots_instrument_time ON market_snapshots(instrument, timestamp DESC);",
            "CREATE INDEX IF NOT EXISTS idx_market_snapshots_stale ON market_snapshots(is_stale) WHERE is_stale = true;",

            # Candles
            "CREATE INDEX IF NOT EXISTS idx_candles_complete ON candles(instrument, interval_minutes, timestamp DESC);",
            "CREATE INDEX IF NOT EXISTS idx_candles_pattern ON candles(pattern_type) WHERE pattern_type IS NOT NULL;",

            # Option chain
            "CREATE INDEX IF NOT EXISTS idx_option_chain_complete ON option_chain_snapshots(instrument, expiry_date, strike, timestamp DESC);",

            # Signals
            "CREATE INDEX IF NOT EXISTS idx_signals_status ON signals(was_traded, signal_type, signal_timestamp DESC);",
            "CREATE INDEX IF NOT EXISTS idx_signals_confidence ON signals(confidence_score DESC) WHERE was_traded = false;",

            # Trades
            "CREATE INDEX IF NOT EXISTS idx_trades_complete ON trades(status, trade_timestamp DESC);",
            "CREATE INDEX IF NOT EXISTS idx_trades_pnl ON trades(net_pnl) WHERE status IN ('CLOSED_PROFIT', 'CLOSED_LOSS');",

            # Orders
            "CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status, order_timestamp DESC);",

            # Portfolio
            "CREATE INDEX IF NOT EXISTS idx_portfolio_daily ON daily_portfolios(date DESC);",

            # News
            "CREATE INDEX IF NOT EXISTS idx_news_market_time ON news_items(market_affected, news_timestamp DESC);",
            "CREATE INDEX IF NOT EXISTS idx_news_sentiment ON news_items(sentiment, confidence DESC);",

            # Audit
            "CREATE INDEX IF NOT EXISTS idx_audit_complete ON audit_logs(action_timestamp DESC, action_type);",
        ]

        for idx_sql in indexes:
            try:
                conn.execute(text(idx_sql))
            except Exception as e:
                print(f"⚠️  Index creation: {e}")

        conn.commit()
        print("✅ Indexes created")


def seed_initial_data(engine):
    """Seed initial configuration data."""
    print("✅ Database initialized successfully")


def main():
    """Main initialization function."""
    print("=" * 80)
    print("AI OPTIONS TRADING PLATFORM - DATABASE INITIALIZATION")
    print("=" * 80)
    print()

    settings = get_settings()

    print(f"📊 Database URL: {settings.database_url}")
    print(f"🔒 TimescaleDB Enabled: {settings.timescale_enabled}")
    print()

    try:
        # Create engine
        print("🔄 Connecting to database...")
        engine = create_engine(settings.database_url)

        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful")

        # Create tables
        print("🔄 Creating tables...")
        Base.metadata.create_all(engine)
        print("✅ All tables created")

        # Create TimescaleDB hypertables
        if settings.timescale_enabled:
            print("🔄 Creating TimescaleDB hypertables...")
            create_timescale_hypertables(engine)

        # Create indexes
        print("🔄 Creating indexes...")
        create_indexes(engine)

        # Seed initial data
        print("🔄 Seeding initial data...")
        seed_initial_data(engine)

        print()
        print("=" * 80)
        print("✅ DATABASE INITIALIZATION COMPLETE")
        print("=" * 80)
        print()
        print("Next steps:")
        print("  1. Verify database with: psql -U trader -h localhost -d options_trading")
        print("  2. Start application with: python backend/main.py")
        print("  3. Access API docs at: http://localhost:8000/api/docs")
        print()

        return 0

    except Exception as e:
        print()
        print("=" * 80)
        print(f"❌ DATABASE INITIALIZATION FAILED")
        print("=" * 80)
        print(f"Error: {e}")
        print()
        print("Troubleshooting:")
        print(f"  1. Check database URL: {settings.database_url}")
        print("  2. Verify PostgreSQL is running")
        print("  3. Verify database exists: CREATE DATABASE options_trading;")
        print("  4. Verify user permissions: GRANT ALL ON DATABASE options_trading TO trader;")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
