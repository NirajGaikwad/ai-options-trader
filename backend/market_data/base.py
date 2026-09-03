"""
Base market data provider interface.
All data providers must implement this interface.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class DataProvider(str, Enum):
    """Available data providers."""
    ZERODHA = "zerodha"
    BROKER_API = "broker_api"
    CSV_SIMULATOR = "csv_simulator"


@dataclass
class IndexSnapshot:
    """Real-time index snapshot."""
    timestamp: datetime
    instrument: str
    ltp: float
    open: float
    high: float
    low: float
    close: float
    volume: int
    previous_close: float
    vwap: float
    bid: float
    ask: float
    change_percent: float
    is_market_open: bool


@dataclass
class OptionChainData:
    """Single row of option chain data."""
    timestamp: datetime
    instrument: str
    strike: float
    expiry: datetime
    underlying_price: float

    # Call Data
    ce_ltp: float
    ce_bid: float
    ce_ask: float
    ce_bid_qty: int
    ce_ask_qty: int
    ce_volume: int
    ce_oi: int
    ce_oi_change: int
    ce_iv: float
    ce_delta: float
    ce_gamma: float
    ce_theta: float
    ce_vega: float

    # Put Data
    pe_ltp: float
    pe_bid: float
    pe_ask: float
    pe_bid_qty: int
    pe_ask_qty: int
    pe_volume: int
    pe_oi: int
    pe_oi_change: int
    pe_iv: float
    pe_delta: float
    pe_gamma: float
    pe_theta: float
    pe_vega: float

    # Metrics
    put_call_ratio: float
    oi_ratio: float
    spread_points: float


@dataclass
class CandleData:
    """OHLCV candle data."""
    timestamp: datetime
    instrument: str
    interval_minutes: int
    open: float
    high: float
    low: float
    close: float
    volume: int
    vwap: float
    is_closed: bool


class BaseMarketDataProvider(ABC):
    """
    Abstract base class for market data providers.
    Implement this to add new data sources.
    """

    def __init__(self):
        self.is_connected = False
        self.last_connection_time: Optional[datetime] = None
        self.connection_errors = 0

    @abstractmethod
    async def connect(self) -> bool:
        """Connect to data source."""
        pass

    @abstractmethod
    async def disconnect(self) -> bool:
        """Disconnect from data source."""
        pass

    @abstractmethod
    async def is_market_open(self) -> bool:
        """Check if market is currently open."""
        pass

    @abstractmethod
    async def get_index_snapshot(self, instrument: str) -> IndexSnapshot:
        """Get real-time index snapshot."""
        pass

    @abstractmethod
    async def get_option_chain(
        self,
        instrument: str,
        expiry: datetime,
        strike: Optional[float] = None,
    ) -> List[OptionChainData]:
        """
        Get option chain data.

        Args:
            instrument: NIFTY, SENSEX, BANKNIFTY
            expiry: Expiration date
            strike: Optional specific strike, if None return all strikes
        """
        pass

    @abstractmethod
    async def get_candle(
        self,
        instrument: str,
        interval_minutes: int,
        limit: int = 100,
    ) -> List[CandleData]:
        """
        Get candle data.

        Args:
            instrument: NIFTY, SENSEX, BANKNIFTY
            interval_minutes: 1, 3, 5, 15, 30, 60, 1440
            limit: Number of candles to fetch
        """
        pass

    @abstractmethod
    async def subscribe_index(
        self,
        instrument: str,
        callback,
    ) -> None:
        """Subscribe to real-time index updates."""
        pass

    @abstractmethod
    async def subscribe_option_chain(
        self,
        instrument: str,
        expiry: datetime,
        callback,
    ) -> None:
        """Subscribe to real-time option chain updates."""
        pass

    @abstractmethod
    async def unsubscribe_index(self, instrument: str) -> None:
        """Unsubscribe from index updates."""
        pass

    @abstractmethod
    async def unsubscribe_option_chain(
        self,
        instrument: str,
        expiry: datetime,
    ) -> None:
        """Unsubscribe from option chain updates."""
        pass

    @abstractmethod
    def get_health_status(self) -> Dict[str, Any]:
        """Get provider health status."""
        pass

    def _mark_connected(self):
        """Mark provider as connected."""
        self.is_connected = True
        self.last_connection_time = datetime.now()
        self.connection_errors = 0

    def _mark_disconnected(self, error: Optional[str] = None):
        """Mark provider as disconnected."""
        self.is_connected = False
        self.connection_errors += 1
        if error:
            print(f"❌ Data Provider Error: {error}")
