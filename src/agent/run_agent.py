from __future__ import annotations
import argparse, logging
from datetime import datetime, timedelta
import pandas as pd, yaml

from ..alpha.arima_filter import arima_signal
from ..alpha.features import build_feature_frame
from ..alpha.model import PumpClassifier
from ..data_ingest.price_loader import PriceLoader
from ..data_ingest.social_scraper import SocialScraper
from ..network_analysis.consensus import ConsensusClusters
from ..portfolio.hrp_allocator import cluster_aware_hrp
from ..portfolio.representatives import pick_representatives
from ..risk_guardrails.turnover import TurnoverLimiter
from ..universe.filter import UniverseFilter
from ..utils.logging_utils import setup_logging
from ..execution.trade_manager import TradeManager

setup_logging()
logger = logging.getLogger(__name__)

def load_cfg(path: str):
    with open(path) as f:
        return yaml.safe_load(f)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["sim"], default="sim")
    p.add_argument("--config", default="config/base.yaml")
    args = p.parse_args()
    cfg = load_cfg(args.config)

    pl = PriceLoader()
    social = SocialScraper()
    pump = PumpClassifier()
    pump.load_or_train()

    uf = UniverseFilter(
        min_adv_usd=cfg["risk"]["min_adv_usd"],
        min_mcap_usd=cfg["risk"]["min_mcap_usd"],
    )
    symbols = uf.filter(cfg["universe"]["symbols"])

    consensus = ConsensusClusters(window=30, threshold=cfg["model"]["consensus_thr"])
    turnover = TurnoverLimiter(cap_pct_nav=cfg["risk"]["turnover_cap_pct"])
    capital = cfg["capital_usd"]
    tm = TradeManager(capital, cfg["risk"])

    end = datetime.utcnow()
    start = end - timedelta(days=120)

    price_series, vol_series, sentiment, adv_map = {}, {}, {}, {}
    for sym in symbols:
        df = pl.load(sym, start, end, "1d")
        price_series[sym] = df["c"]
        vol_series[sym] = df["v"]
        adv_map[sym] = (df["c"] * df["v"]).mean()
        sentiment[sym] = social.polarity(social.fetch_recent(sym))

    price_df = pd.DataFrame(price_series)
    volume_df = pd.DataFrame(vol_series)
    dates = price_df.index.unique()

    for i in range(60, len(dates)):  # walk-forward
        slice_df = price_df.iloc[: i + 1]
        corr_now = slice_df.pct_change().iloc[-30:].corr()
        stable_clusters = consensus.update(corr_now)
        reps = pick_representatives(stable_clusters, adv_map)

        returns = slice_df[reps].pct_change().dropna()
        weights = cluster_aware_hrp(returns, stable_clusters, cfg["risk"]["cluster_cap"])
        weights = turnover.limit(weights)

        feats = build_feature_frame(slice_df[reps], stable_clusters, volume_df[reps], sentiment)
        proba = pump.predict_proba(feats)

        btc = slice_df["BTC/USDT"].pct_change().dropna() if "BTC/USDT" in slice_df else pd.Series()

        for sym in reps:
            if proba.get(sym, 0) < cfg["model"]["min_confidence"]:
                continue
            series_vals = slice_df[sym].tail(60).tolist()
            if not arima_signal(series_vals, tuple(cfg["model"]["arima_order"]), 0.5):
                continue
            tm.execute_signal(
                sym,
                proba[sym],
                slice_df[sym],
                adv_map[sym],
                btc,
                slice_df[reps],
                weights.get(sym, 0),
            )

if __name__ == "__main__":
    main()
