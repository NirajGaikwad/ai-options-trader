"""
Simulator market data provider for testing and paper trading.
Generates realistic synthetic market data.
"""

import asyncio
import random
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import math

from .base import (
    BaseMarketDataProvider,
    IndexSnapshot,
    OptionChainData,
    CandleData,
)


class SimulatorMarketDataProvider(BaseMarketDataProvider):
    """
    Simulates market data for testing.
    Generates realistic OHLCV candles and option chain data.
    """

    def __init__(self):
        super().__init__()
        self.subscriptions = {}
        self.market_open = True

        # Starting prices
        self.nifty_price = 23500.0
        self.sensex_price = 77500.0
        self.price_history = {}

    async def connect(self) -> bool:
        """Connect simulator."""
        self._mark_connected()
        print("✅ Simulator market data provider connected")
        return True

    async def disconnect(self) -> bool:
        """Disconnect simulator."""
        self.is_connected = False
        return True

    async def is_market_open(self) -> bool:
        """Check if market is open (simulated)."""
        return self.market_open

    async def get_index_snapshot(self, instrument: str) -> IndexSnapshot:
        """Generate realistic index snapshot."""
        if instrument.upper() == "NIFTY":
            base_price = self.nifty_price
        elif instrument.upper() == "SENSEX":
            base_price = self.sensex_price
        else:
            raise ValueError(f"Unknown instrument: {instrument}")

        # Add random movement
        movement = random.uniform(-0.5, 0.5)
        new_price = base_price * (1 + movement / 100)

        # Store for history
        if instrument not in self.price_history:
            self.price_history[instrument] = []
        self.price_history[instrument].append(new_price)

        high = max(self.price_history[instrument][-20:])
        low = min(self.price_history[instrument][-20:])

        return IndexSnapshot(
            timestamp=datetime.now(),
            instrument=instrument,
            ltp=new_price,
            open=base_price,
            high=high,
            low=low,
            close=new_price,
            volume=random.randint(1000000, 5000000),
            previous_close=base_price,
            vwap=(high + low + new_price) / 3,
            bid=new_price - 1,
            ask=new_price + 1,
            change_percent=(new_price - base_price) / base_price * 100,
            is_market_open=True,
        )

    async def get_option_chain(
        self,
        instrument: str,
        expiry: datetime,
        strike: Optional[float] = None,
    ) -> List[OptionChainData]:
        """Generate realistic option chain data."""
        index_snapshot = await self.get_index_snapshot(instrument)
        underlying_price = index_snapshot.ltp

        # Generate strikes around ATM
        if strike:
            strikes = [strike]
        else:
            strikes = [
                underlying_price - 500,
                underlying_price - 250,
                underlying_price,
                underlying_price + 250,
                underlying_price + 500,
            ]

        chains = []
        for strike_price in strikes:
            # Calculate option prices using simplified Black-Scholes
            days_to_expiry = max(1, (expiry - datetime.now()).days)
            time_to_expiry = days_to_expiry / 365

            # Call option
            call_price = self._black_scholes_call(
                underlying_price, strike_price, time_to_expiry
            )
            put_price = self._black_scholes_put(
                underlying_price, strike_price, time_to_expiry
            )

            chain = OptionChainData(
                timestamp=datetime.now(),
                instrument=instrument,
                strike=strike_price,
                expiry=expiry,
                underlying_price=underlying_price,
                # Call Data
                ce_ltp=call_price,
                ce_bid=call_price - 0.1,
                ce_ask=call_price + 0.1,
                ce_bid_qty=random.randint(100, 1000),
                ce_ask_qty=random.randint(100, 1000),
                ce_volume=random.randint(1000, 10000),
                ce_oi=random.randint(100000, 1000000),
                ce_oi_change=random.randint(-50000, 50000),
                ce_iv=0.25 + random.uniform(-0.05, 0.05),  # ~25% IV
                ce_delta=self._calculate_delta(underlying_price, strike_price, time_to_expiry),
                ce_gamma=0.001,
                ce_theta=-0.05,
                ce_vega=0.15,
                # Put Data
                pe_ltp=put_price,
                pe_bid=put_price - 0.1,
                pe_ask=put_price + 0.1,
                pe_bid_qty=random.randint(100, 1000),
                pe_ask_qty=random.randint(100, 1000),
                pe_volume=random.randint(1000, 10000),
                pe_oi=random.randint(100000, 1000000),
                pe_oi_change=random.randint(-50000, 50000),
                pe_iv=0.25 + random.uniform(-0.05, 0.05),
                pe_delta=-self._calculate_delta(underlying_price, strike_price, time_to_expiry),
                pe_gamma=0.001,
                pe_theta=-0.05,
                pe_vega=0.15,
                # Metrics
                put_call_ratio=random.uniform(0.8, 1.5),
                oi_ratio=random.uniform(0.8, 1.5),
                spread_points=0.2,
            )
            chains.append(chain)

        return chains

    async def get_candle(
        self,
        instrument: str,
        interval_minutes: int,
        limit: int = 100,
    ) -> List[CandleData]:
        """Generate realistic candle data."""
        index_snapshot = await self.get_index_snapshot(instrument)
        current_price = index_snapshot.ltp

        candles = []
        current_time = datetime.now()

        for i in range(limit, 0, -1):
            candle_time = current_time - timedelta(minutes=interval_minutes * i)

            # Generate realistic OHLC
            open_price = current_price * (1 + random.uniform(-0.5, 0.5) / 100)
            close_price = open_price * (1 + random.uniform(-1, 1) / 100)
            high = max(open_price, close_price) * (1 + abs(random.uniform(0, 1)) / 100)
            low = min(open_price, close_price) * (1 - abs(random.uniform(0, 1)) / 100)

            candle = CandleData(
                timestamp=candle_time,
                instrument=instrument,
                interval_minutes=interval_minutes,
                open=open_price,
                high=high,
                low=low,
                close=close_price,
                volume=random.randint(100000, 500000),
                vwap=(high + low + close_price) / 3,
                is_closed=(i < limit),
            )
            candles.append(candle)

            current_price = close_price

        return candles

    async def subscribe_index(
        self,
        instrument: str,
        callback,
    ) -> None:
        """Subscribe to simulated index updates."""
        self.subscriptions[f"index_{instrument}"] = callback

        # Simulate real-time updates
        async def simulate_updates():
            while self.is_connected:
                snapshot = await self.get_index_snapshot(instrument)
                await callback(snapshot)
                await asyncio.sleep(random.uniform(1, 5))

        asyncio.create_task(simulate_updates())

    async def subscribe_option_chain(
        self,
        instrument: str,
        expiry: datetime,
        callback,
    ) -> None:
        """Subscribe to simulated option chain updates."""
        key = f"option_{instrument}_{expiry.isoformat()}"
        self.subscriptions[key] = callback

        # Simulate real-time updates
        async def simulate_updates():
            while self.is_connected and key in self.subscriptions:
                chains = await self.get_option_chain(instrument, expiry)
                for chain in chains:
                    await callback(chain)
                await asyncio.sleep(random.uniform(2, 10))

        asyncio.create_task(simulate_updates())

    async def unsubscribe_index(self, instrument: str) -> None:
        """Unsubscribe from index updates."""
        key = f"index_{instrument}"
        if key in self.subscriptions:
            del self.subscriptions[key]

    async def unsubscribe_option_chain(
        self,
        instrument: str,
        expiry: datetime,
    ) -> None:
        """Unsubscribe from option chain updates."""
        key = f"option_{instrument}_{expiry.isoformat()}"
        if key in self.subscriptions:
            del self.subscriptions[key]

    def get_health_status(self) -> Dict[str, Any]:
        """Get simulator health status."""
        return {
            "provider": "simulator",
            "is_connected": self.is_connected,
            "subscriptions": len(self.subscriptions),
            "market_open": self.market_open,
            "nifty_price": self.nifty_price,
            "sensex_price": self.sensex_price,
        }

    # ========================================================================
    # HELPER METHODS
    # ========================================================================

    @staticmethod
    def _black_scholes_call(S: float, K: float, T: float, r: float = 0.05, sigma: float = 0.25) -> float:
        """Simplified Black-Scholes for call option price."""
        from math import log, sqrt, exp
        from scipy.stats import norm

        d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)

        call = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
        return max(0.05, call)  # Minimum premium

    @staticmethod
    def _black_scholes_put(S: float, K: float, T: float, r: float = 0.05, sigma: float = 0.25) -> float:
        """Simplified Black-Scholes for put option price."""
        from math import log, sqrt, exp
        from scipy.stats import norm

        d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)

        put = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        return max(0.05, put)  # Minimum premium

    @staticmethod
    def _calculate_delta(S: float, K: float, T: float, r: float = 0.05, sigma: float = 0.25) -> float:
        """Calculate delta for option pricing."""
        from math import log, sqrt
        from scipy.stats import norm

        if T <= 0:
            return 1.0 if S >= K else 0.0

        d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
        return norm.cdf(d1)
