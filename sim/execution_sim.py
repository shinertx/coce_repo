"""Quick smoke-test of TradeManager slippage / risk."""
from random import random
import pandas as pd
from src.execution.trade_manager import TradeManager

tm = TradeManager(
    10000,
    {"max_drawdown_pct": 20, "adv_cap_pct": 2, "var_confidence": 0.95, "corr_spike_thresh": 0.6},
)
series = pd.Series([1.0] * 120)
tm.execute_signal("SIM/USDT", random(), series, 100_000, series, pd.DataFrame({"SIM": series}), 0.02)
