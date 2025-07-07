from __future__ import annotations
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict
import pandas as pd
from ..execution.slippage import sqrt_slippage
from ..risk_guardrails.liquidity_limits import adv_cap_check
from ..risk_guardrails.orderbook_depth import executable_size
from ..risk_guardrails.max_drawdown import DrawdownTracker
from ..risk_guardrails.var_check import hist_var_check
from ..risk_guardrails.corr_spike import CorrSpikeSentinel
from ..state.persistence import save_state, load_state
from ..utils.logging_utils import setup_logging
from .ccxt_router import CcxtRouter

setup_logging()
logger = logging.getLogger(__name__)


@dataclass
class Trade:
    """Executed trade record."""

    ts: str
    symbol: str
    side: str
    size: float
    price: float
    confidence: float
    risk: str
    slip_bps: float


@dataclass
class SpotPosition:
    symbol: str
    size: float
    entry: float


class TradeManager:
    """Handle order placement and risk checks."""

    def __init__(self, capital_usd: float, risk_cfg: Dict[str, float]) -> None:
        """Create a new manager with ``capital_usd`` and risk parameters."""

        self.capital, self.risk_cfg = capital_usd, risk_cfg
        self.router = CcxtRouter()
        self.drawdown = DrawdownTracker(capital_usd)
        self.sentinel = CorrSpikeSentinel(threshold=risk_cfg["corr_spike_thresh"])
        self.stop_loss_pct = risk_cfg.get("stop_loss_pct", 0.0)
        self.positions: Dict[str, SpotPosition] = {}
        state = load_state()
        if state and "equity_curve" in state:
            self.drawdown.equity_curve = state["equity_curve"]

    def _persist(self) -> None:
        save_state({"equity_curve": self.drawdown.equity_curve})

    def _check_stop_loss(self, symbol: str, price: float) -> None:
        if self.stop_loss_pct <= 0:
            return
        pos = self.positions.get(symbol)
        if not pos:
            return
        if price <= pos.entry * (1 - self.stop_loss_pct / 100):
            try:
                self.router.place_order(symbol, "sell", pos.size, price)
                self.drawdown.update([price / pos.entry - 1])
                stop = Trade(
                    ts=datetime.now(tz=timezone.utc).isoformat(timespec="seconds"),
                    symbol=symbol,
                    side="SELL",
                    size=pos.size,
                    price=price,
                    confidence=0.0,
                    risk="STOP_LOSS",
                    slip_bps=0.0,
                )
                logger.info(stop.__dict__)
            except Exception as exc:
                logger.error("Stop-loss order failed %s", exc)
            del self.positions[symbol]
            self._persist()

    def monitor_position(self, symbol: str, price: float) -> None:
        """Check open ``symbol`` position on each new tick."""

        self._check_stop_loss(symbol, price)

    def execute_signal(
        self,
        symbol: str,
        proba: float,
        price_series: pd.Series,
        adv_usd: float,
        btc_series: pd.Series,
        alt_df: pd.DataFrame,
        weight: float,
    ) -> Trade | None:
        """Execute a buy signal if risk checks pass."""

        if not self.sentinel.check(btc_series, alt_df):
            logger.warning("Corr-sentinel tripped")
            return None

        price = price_series.iloc[-1]
        self.monitor_position(symbol, price)

        order_usd = max(self.capital * weight, 0)
        if order_usd == 0:
            return None

        size = order_usd / price
        adv_cap = adv_usd * self.risk_cfg["adv_cap_pct"] / 100 / price
        size = min(size, adv_cap)

        depth_pct = self.risk_cfg.get("depth_impact_pct", 1.0)
        try:
            book = self.router.client.fetch_order_book(symbol)
            depth_cap = executable_size(book, "buy", depth_pct)
            size = min(size, depth_cap)
        except Exception as exc:  # pragma: no cover - network errors
            logger.warning("orderbook fetch failed %s", exc)

        order_usd = size * price
        slip_frac = sqrt_slippage(order_usd, adv_usd)
        price_exec = price * (1 + slip_frac)

        risk_pass = all(
            [
                adv_cap_check(order_usd, adv_usd, cap_pct=self.risk_cfg["adv_cap_pct"]),
                hist_var_check(
                    price_series.pct_change().dropna(),
                    self.risk_cfg["var_confidence"],
                    self.risk_cfg.get("var_floor", -0.03),
                ),
                self.drawdown.within_limit(self.risk_cfg["max_drawdown_pct"]),
            ]
        )
        tag = "PASS" if risk_pass else "FAIL"

        trade = Trade(
            ts=datetime.now(tz=timezone.utc).isoformat(timespec="seconds"),
            symbol=symbol,
            side="BUY",
            size=size,
            price=price_exec,
            confidence=proba,
            risk=tag,
            slip_bps=slip_frac * 10_000,
        )
        logger.info(trade.__dict__)
        if risk_pass:
            try:
                # pass explicit execution price to enforce slippage bounds
                self.router.place_order(symbol, "buy", size, price_exec)
                self.drawdown.update([price_exec / price - 1])
                self.positions[symbol] = SpotPosition(symbol, size, price_exec)
            except Exception as exc:
                logger.error("Order failed %s", exc)
            self._persist()
            return trade
        return None
